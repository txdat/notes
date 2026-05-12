# Idempotency

## Problem

In distributed systems, network failures and retries cause the same request to arrive more than once. Without protection, a retry can:
- Create a duplicate booking, payment, or reservation
- Double-charge a customer
- Produce duplicate notifications
- Leave external systems in inconsistent state

## What Makes a Request Idempotent

An operation is **idempotent** if executing it multiple times with the same input produces the same result as executing it once. Safe HTTP methods (`GET`, `HEAD`) are naturally idempotent. State-mutating operations (`POST`, `PATCH`) are not — they require explicit deduplication.

Two types of idempotency:
- **Natural** — the operation's semantics prevent duplication (e.g. `INSERT ... ON CONFLICT DO NOTHING`, unique constraints, `DELETE WHERE id = ?`)
- **Key-based** — client supplies a unique key; server deduplicates by storing and replaying the first response

## Two-Phase Key-Based Protocol

Atomic-book implements key-based idempotency via `idempotency-lib`, using a two-phase atomic store backed by PostgreSQL.

### Phases

**Phase 1 — Pre-check (before executing)**
```sql
INSERT INTO idempotency_keys (key, fingerprint, status, expires_at)
VALUES (?, ?, 'PROCESSING', ?)
ON CONFLICT (key) DO NOTHING
RETURNING *
```
- **Row inserted** (`RETURNING *` is non-empty) → this is a first-time request; proceed with execution
- **Conflict** (`RETURNING *` is empty) → key exists; continue to phase 1b

**Phase 1b — Conflict resolution**
```sql
SELECT * FROM idempotency_keys WHERE key = ? FOR UPDATE
```
`FOR UPDATE` blocks until any in-flight request on the same key commits — then switch on status:

| Status | Action |
|---|---|
| `PROCESSING` | throw `IdempotencyConflictException` → HTTP 409 |
| `COMPLETED` + fingerprint matches | deserialise `result_json` → return cached response |
| `COMPLETED` + fingerprint mismatch | throw `IdempotencyKeyReusedException` → HTTP 422 |

**Phase 2 — Complete (after executing)**
```sql
UPDATE idempotency_keys SET status = 'COMPLETED', result_json = ?
WHERE key = ?
```

The entire pre-check is `@Transactional(propagation = REQUIRED)`, so the INSERT and the follow-up SELECT-FOR-UPDATE share the same transaction. No application-level lock is needed.

### Flow Diagram

```
Client                         Service                         DB
  │                               │                             │
  │── POST /bookings ────────────→│                             │
  │   Idempotency-Key: abc-123    │                             │
  │                               │── INSERT ... ON CONFLICT ──→│
  │                               │   DO NOTHING RETURNING *    │
  │                               │←── row returned ────────────│  (first time)
  │                               │                             │
  │                               │── execute saga ────────────→│
  │                               │                             │
  │                               │── UPDATE status=COMPLETED ─→│
  │←── 201 Created ───────────────│                             │
  │                               │                             │
  │   (network failure, retry)    │                             │
  │                               │                             │
  │── POST /bookings ────────────→│                             │
  │   Idempotency-Key: abc-123    │                             │
  │                               │── INSERT ... ON CONFLICT ──→│
  │                               │   DO NOTHING RETURNING *    │
  │                               │←── empty (conflict) ────────│
  │                               │── SELECT FOR UPDATE ────────→│
  │                               │←── status=COMPLETED ────────│
  │←── 201 Created (cached) ──────│  (deserialised from DB)     │
```

### Concurrent Duplicate Requests

Both requests arrive simultaneously before either has completed:

```
Request A: INSERT → wins, gets row back → proceeds to execute
Request B: INSERT → conflict → SELECT FOR UPDATE → blocks (waits for A's txn)

  A commits → B unblocks
    If A still PROCESSING: B throws IdempotencyConflictException (409)
    If A completed: B returns cached result
```

There is no wait/retry loop — the client receives a 409 and is expected to poll or retry after a delay.

---

## Domain Model

```java
// idempotency-lib: IdempotencyRecord.java
record IdempotencyRecord(
    String key,          // client-supplied key (PK)
    String fingerprint,  // SHA-256 hex of serialised request body
    IdempotencyStatus status,  // PROCESSING | COMPLETED
    String resultJson,   // null while PROCESSING; serialised response when COMPLETED
    Instant createdAt,
    Instant expiresAt    // TTL for cleanup (default 24h)
)
```

No synthetic `id` column — `key` is the primary key.

### Status Enum

| Status | Meaning |
|---|---|
| `PROCESSING` | Request is in-flight; concurrent duplicates get 409 |
| `COMPLETED` | Response stored; all future duplicates get cached response |

There is no `FAILED` status. If the saga throws, the `PROCESSING` row stays and is cleaned up by TTL expiry. A retry after failure will hit the `PROCESSING` → 409 path briefly, then after the row expires (24h), the next retry will insert a fresh row and re-execute.

---

## Fingerprint

The fingerprint is a **SHA-256 hex digest of the Jackson-serialised request body**:

```java
byte[] bytes = MessageDigest
    .getInstance("SHA-256")
    .digest(objectMapper.writeValueAsString(command).getBytes(UTF_8));
// → 64-char lowercase hex string
```

**Purpose:** detect key reuse with a different payload. When a `COMPLETED` record is found, `preCheck` compares fingerprints. If they differ, it throws `IdempotencyKeyReusedException` (422) instead of returning the cached response. This prevents a client from accidentally reusing a key with a modified request and silently receiving a stale response.

**What triggers a mismatch:**
- Client changed the request body but reused the key
- Serialisation is non-deterministic (e.g. map key ordering); use Jackson with a consistent `ObjectMapper` config

---

## DB Schema

```sql
CREATE TABLE idempotency_keys (
    key         VARCHAR(255)  PRIMARY KEY,
    fingerprint VARCHAR(64)   NOT NULL,              -- SHA-256 hex, always 64 chars
    status      VARCHAR(20)   NOT NULL DEFAULT 'PROCESSING',
    result_json TEXT,                                -- null until COMPLETED
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now(),
    expires_at  TIMESTAMPTZ   NOT NULL               -- set on INSERT, used by cleanup
);

CREATE INDEX idx_idempotency_keys_expires_at ON idempotency_keys (expires_at);
```

Index on `expires_at` serves the hourly cleanup query.

---

## Library Integration (`idempotency-lib`)

Auto-configures via `IdempotencyAutoConfiguration`:

```java
@Configuration
@EnableScheduling
@ConditionalOnClass(DSLContext.class)
@ConditionalOnProperty(name = "idempotency.enabled",
    havingValue = "true", matchIfMissing = true)   // enabled by default
```

All beans are `@ConditionalOnMissingBean` — override any by providing your own.

**Config properties:**

| Property | Default | Meaning |
|---|---|---|
| `idempotency.enabled` | `true` | Disable entirely by setting `false` |
| `idempotency.ttl-hours` | `24` | How long a completed record is retained |
| `idempotency.cleanup.interval-ms` | `3600000` (1h) | How often expired rows are deleted |

**Adopting in a service:**
1. Add `idempotency-lib` Maven dependency
2. Add `"classpath:db/idempotency"` to `FlywayConfig` migration locations
3. Use a separate `flyway_schema_history_idempotency` table to avoid V1 collision with service migrations
4. Inject `IdempotencyService` into the application service (not the controller)
5. Pass `idempotencyKey` from the controller down through the port/in interface method signature

```java
// Controller — extract header and pass down
@PostMapping
public ApiResponse<CreateBookingResponse> create(
        @RequestHeader("Idempotency-Key") String idempotencyKey,
        @Valid @RequestBody CreateBookingRequest request) {
    return ApiResponse.success(createBooking.create(request, idempotencyKey));
}

// Port/in interface — key is part of the use-case signature
interface CreateBooking {
    CreateBookingResponse create(CreateBookingRequest request, String idempotencyKey);
}

// Application service — wrap execution with pre-check / complete
@Service
class CreateBookingService implements CreateBooking {

    public CreateBookingResponse create(CreateBookingRequest request, String idempotencyKey) {
        String fingerprint = idempotencyService.computeFingerprint(request);

        Optional<CreateBookingResponse> cached =
            idempotencyService.preCheck(idempotencyKey, fingerprint, CreateBookingResponse.class);
        if (cached.isPresent()) return cached.get();   // short-circuit, return cached

        // ... execute saga ...

        idempotencyService.complete(idempotencyKey, response);
        return response;
    }
}
```

**Services that use it in atomic-book:**

| Service | Use cases protected |
|---|---|
| `booking-service` | `CreateBooking` |
| `inventory-service` | `ReserveSlot` |
| `ledger-service` | `Hold`, `Capture`, `Refund`, `Release`, `Topup` |

`identity-service` does not use the library — auth endpoints are naturally idempotent by domain semantics (login always issues new tokens; register rejects duplicates via unique constraint).

---

## Cleanup

Expired rows are deleted on a scheduled basis:

```java
@Scheduled(fixedRateString = "${idempotency.cleanup.interval-ms:3600000}")
void cleanupExpired() {
    store.deleteExpired();
    // DELETE FROM idempotency_keys WHERE expires_at < now()
}
```

`fixedRate` is correct here (not `fixedDelay`) — the delete is fast and idempotent; no overlap risk.

---

## Ports & Adapters

```
application/IdempotencyService              ← concrete service (preCheck, complete, computeFingerprint)
port/out/IdempotencyStore                   ← port interface (tryInsertProcessing, findByKey, complete, deleteExpired)
adapter/out/IdempotencyStoreJooqAdapter     ← jOOQ impl (INSERT ON CONFLICT, SELECT FOR UPDATE, UPDATE, DELETE)
config/IdempotencyAutoConfiguration         ← Spring auto-config + @EnableScheduling
```

---

## Gotchas

**No `FAILED` status** — a failed request leaves a `PROCESSING` row until TTL expires (24h). A client that retries immediately after a 500 will get a 409 until the row expires. For short-lived operations, consider a shorter TTL or explicitly deleting the row on failure (not currently implemented in the lib).

**Fingerprint depends on serialisation stability** — if the `ObjectMapper` produces non-deterministic output (e.g. unordered maps), two identical logical requests may hash to different fingerprints. Always use a consistently configured `ObjectMapper`; avoid `Map.of()` for objects with many fields (insertion-ordered but worth being explicit).

**`idempotencyKey` must flow through the port/in interface** — the lib registers no HTTP filter. The controller must extract the header and pass it as a parameter all the way to the application service. Never inject `HttpServletRequest` into an application service to read the header directly — that violates hexagonal layering.

**Null/blank key → idempotency skipped** — `preCheck` returns `Optional.empty()` immediately on a null or blank key. This allows optional idempotency (callers without a key get no protection) but means the endpoint is unsafe under retries if the client doesn't supply a key.

**Flyway V1 collision** — `idempotency-lib`, `outbox-lib`, and the service each ship a `V1` migration. Always configure three separate `Flyway` beans pointing to distinct `flyway_schema_history_<name>` tables, with `baselineOnMigrate(true)` + `baselineVersion("0")` on secondary beans.

**`@Transactional` propagation** — `preCheck` uses `REQUIRED`, so it joins the caller's transaction if one exists. If the caller is not `@Transactional`, `preCheck` starts its own. The INSERT + SELECT-FOR-UPDATE must complete in the same transaction; never call `preCheck` and `complete` in separate transactions.

**Key reuse across different operations** — the key namespace is global within a service. If two different endpoints could receive the same key value from the client, fingerprint mismatch detection provides the safety net (422 rather than silently returning the wrong cached response).

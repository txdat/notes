# Saga Pattern

## Problem

A business operation that spans multiple services (e.g. booking a slot, reserving a coupon, holding funds) cannot use a distributed ACID transaction. If any step fails mid-way, previously committed steps in other services must be explicitly undone.

## Solution

A **saga** is a sequence of local transactions. Each step performs a local write and publishes an event (or calls the next service). On failure, **compensating transactions** undo prior steps in reverse order.

Two coordination styles:
- **Choreography** — each service reacts to events from other services (no central coordinator)
- **Orchestration** — a single service drives the saga, calling others sequentially and handling compensation centrally

Atomic-book uses **orchestration** via `booking-service` as the saga coordinator.

---

## Choreography vs Orchestration (In-Depth)

### How Choreography Works

Each service listens to domain events and reacts by executing its local step, then emitting the next event. No service knows the full flow — the saga emerges from the chain of events.

```
BookingRequested
  ↓ (fraud-service listens)
FraudCheckPassed / FraudCheckFailed
  ↓ (promo-service listens on FraudCheckPassed)
PromoReserved / PromoReserveFailed
  ↓ (inventory-service listens on PromoReserved)
InventoryReserved / InventoryReserveFailed
  ↓ (booking-service listens on InventoryReserved)
BookingCreated (DB write + ledger hold)
  ↓ (payment-service listens on BookingCreated)
PaymentCaptured / PaymentFailed
```

Compensation is also event-driven. On failure, a service emits a compensating event (`InventoryReserveFailed`) which triggers upstream services to roll back.

```
InventoryReserveFailed
  ↓ (promo-service listens)
PromoRolledBack
  ↓ (fraud-service doesn't need compensation)
BookingFailed (terminal)
```

Each service owns a slice of the saga and is fully decoupled — it only knows its upstream trigger event and its downstream success/failure events.

### How Orchestration Works

A central coordinator (orchestrator) drives every step synchronously (or asynchronously), decides the next step, and handles all compensation logic in one place.

```
BookingController
  → CreateBookingService (orchestrator)
      1. call FraudServiceClient.evaluate()
      2. call PromoServiceClient.reserve()
      3. call InventoryServiceClient.reserveSlot()
      4. call ReservationWriter.write()  ← @Transactional
      5. call LedgerServiceClient.holdFunds()
      6. call PromoServiceClient.commit()
      on any failure: compensate in reverse
```

The orchestrator explicitly knows the full sequence and all compensation paths. Downstream services expose simple request/response APIs — they don't know they're in a saga.

---

### Comparison

| Dimension | Choreography | Orchestration |
|---|---|---|
| **Coupling** | Loose — services only know event contracts | Tighter — orchestrator knows all downstream APIs |
| **Flow visibility** | Implicit — must trace events across logs | Explicit — entire flow is readable in one class |
| **Debugging** | Hard — distributed trace required to follow a saga | Easy — stack trace and logs are in one service |
| **Compensation** | Distributed — each service handles its own rollback on a compensating event | Centralized — orchestrator runs all rollbacks in one place |
| **Single point of failure** | None — any service failure is isolated | Orchestrator is the SPOF; if it crashes mid-saga, state may be inconsistent |
| **Saga state** | Distributed across services (each holds its own state) | Usually implicit in the orchestrator's DB row (e.g. `Reservation.status=PENDING`) |
| **Service contracts** | Event-based — producers emit, consumers filter | RPC-based — orchestrator calls a specific API on a specific service |
| **Adding a new step** | Add a new listener; no other service changes needed | Must modify orchestrator code; potentially update compensation logic |
| **Testing** | Harder — must simulate event chains | Easier — orchestrator logic is a single unit under test |
| **Cyclic dependencies** | Less likely — services don't call each other | Possible — orchestrator imports all downstream port interfaces |
| **Latency** | Higher if each step waits for an event round-trip through Kafka | Lower for synchronous steps (direct HTTP/gRPC calls); higher if event-driven |
| **Throughput** | Higher — steps can overlap across multiple saga instances via event parallelism | Sequential steps within a single saga; parallelism requires explicit branching |
| **Operational burden** | More Kafka topics, more consumer groups, more event schema governance | One service owns the flow; fewer moving parts per saga |

---

### When to Use Each

**Choose choreography when:**
- Services are truly independent and owned by separate teams; no team should own the "booking flow"
- The saga is long-running and steps may take minutes/hours (e.g. waiting for a human approval step)
- You want each service to be deployable and scalable independently without coordinating on flow changes
- Individual steps are idempotent and self-contained (no complex rollback chains)
- You already have strong event schema governance (schema registry, versioning)

**Choose orchestration when:**
- The saga is short-lived and latency-sensitive (all steps complete in < 1s under normal conditions)
- Compensation logic is complex and dependent on which step failed — centralising it is safer than distributing it
- The full flow needs to be readable and auditable in one place (compliance, ops debugging)
- Downstream services are utility-style (inventory, ledger) rather than domain-owning services
- You want synchronous error propagation — the caller gets an error back immediately on failure

**Atomic-book uses orchestration** because:
1. The booking flow is latency-sensitive (user is waiting for a confirmation)
2. Compensation is non-trivial (LIFO order, `safeXxx` wrappers, ledger/promo interactions)
3. Downstream services (fraud, promo, inventory, ledger) are utility APIs, not domain owners
4. The full saga lives in one class (`CreateBookingService`), making it easy to audit and test

---

### What Choreography Would Look Like in Atomic-Book

Each service would consume and emit typed Kafka events. The booking flow would be driven by:

```
[booking-service] emit BookingRequested
  → [fraud-service] consume BookingRequested
    → emit FraudCheckPassed {bookingId, userId, subtotal, couponCodes, slotId}
      → [promo-service] consume FraudCheckPassed
        → emit PromoReserved {bookingId, batchId, discountedSubtotal}
          → [inventory-service] consume PromoReserved
            → emit SlotReserved {bookingId, reservationId, supplierId}
              → [booking-service] consume SlotReserved
                → DB write + emit BookingCreated
                  → [ledger-service] consume BookingCreated
                    → emit FundsHeld {bookingId, holdId}
                      → [promo-service] consume FundsHeld
                        → emit PromoCommitted {bookingId, batchId}
                          → [booking-service] consume PromoCommitted
                            → UPDATE status=CONFIRMED
```

Compensation chain on `SlotReserveFailed`:
```
[inventory-service] emit SlotReserveFailed
  → [promo-service] consume SlotReserveFailed → emit PromoRolledBack
    → [booking-service] consume PromoRolledBack → UPDATE status=FAILED, notify user
```

**Problems this introduces:**
- The booking flow is now spread across 6 services and ~12 Kafka topics
- A single saga instance requires tracing events across all 6 services to debug
- Each service must be idempotent on its trigger event (Kafka at-least-once delivery)
- Schema changes to any event require coordinating consumers across multiple teams
- The compensation chain must be fully implemented in every participant — a missing handler leaves resources leaked
- Cyclic consumption: booking-service both initiates and reacts to multiple events (`SlotReserved`, `PromoCommitted`)

This is why atomic-book chose orchestration for this particular flow.

---

## Booking Saga (atomic-book)

### Coordinator

`CreateBookingService` — implements `CreateBooking` port/in.  
Deliberately **not `@Transactional`** — HTTP calls to downstream services must not hold a DB connection open. DB write is delegated to `ReservationWriter` (a sibling `@Transactional` service).

### Steps & Compensation Map

```
                                              On failure, compensate:
Step 1: Validate price quote                  (nothing — nothing allocated yet)
Step 2: Fraud check (gRPC)                    (nothing)
Step 3: Reserve promo/coupon (HTTP)           (nothing)
Step 4: Reserve inventory slot (HTTP)         → rollback promo (step 3)
Step 5: Validate cancellation policy (DB)     → release inventory (step 4)
                                              → rollback promo (step 3)
Step 6: Atomic DB write + outbox event        → release inventory (step 4)
                                              → rollback promo (step 3)
Step 7: Hold funds in ledger (HTTP)           → release inventory (step 4)
                                              → rollback promo (step 3)
Step 8: Commit promo batch (HTTP)             (swallowed — batch expires naturally)
```

### Step Details

**Step 1 — Quote validation**
- Port/out: `PriceQuoteRepository.findById(quoteId)`
- Failures: `QuoteNotFoundException`, `QuoteExpiredException`, `QuoteAlreadyUsedException`

**Step 2 — Fraud check**
- Port/out: `FraudServiceClient.evaluate(userId, subtotal)` → `FraudDecision(decision, score)`
- Failure: `FraudBlockedException` if `decision == "BLOCK"`
- Current impl: `FraudServiceStub` always returns `ALLOW/0` (`@ConditionalOnMissingBean(name = "fraudGrpcClient")`)
- Injection point for real gRPC adapter: provide a bean named `fraudGrpcClient`

**Step 3 — Promo reservation** _(conditional: only if coupons present)_
- Port/out: `PromoServiceClient.reserve(userId, couponCodes, subtotal, slotId, null)`
- Returns `PromoReservationResult(batchId, totalDiscount, discountedSubtotal)`
- Failure: `CouponReservationFailedException`

**Step 4 — Inventory slot reservation**
- Port/out: `InventoryServiceClient.reserveSlot(slotId, bookingId, qty, expiresAt)`
- Returns `SlotReservationResult(reservationId, supplierId)`
- TTL: `booking.reservation.ttl-minutes` (default 15 min) — slot auto-releases on expiry
- Failure: `SlotUnavailableException`
- **Compensation:** `safeRollbackPromo(promoBatchId)`

**Step 5 — Cancellation policy validation**
- Port/out: `CancellationPolicyRepository.findById(policyId)`
- Failures: `PolicyNotFoundException`, `PolicyNotActiveException`
- **Compensation:** `safeReleaseInventory(inventoryReservationId)` → `safeRollbackPromo(promoBatchId)`

**Step 6 — Atomic DB write**
- Delegated to `ReservationWriter.writeReservation()` (`@Transactional`):
  - `quoteRepository.markUsed(quoteId)` — idempotency guard (prevents double-booking on retry)
  - `reservationRepository.save(Reservation)` — status `PENDING`
  - `outboxEventRepository.save(BookingCreated)` — outbox in same transaction
- Failure: `QuoteAlreadyUsedException` (race), any DB exception
- **Compensation:** `safeReleaseInventory` → `safeRollbackPromo`

**Step 7 — Ledger fund hold**
- Port/out: `LedgerServiceClient.holdFunds(userId, reservationId, originalSubtotal)`
- Holds pre-discount amount
- Failure: `LedgerServiceException`
- **Compensation:** `safeReleaseInventory` → `safeRollbackPromo`
- Note: the `PENDING` reservation row is **not** DB-rolled-back here — it expires via the TTL sweeper

**Step 8 — Promo batch commit** _(conditional)_
- Port/out: `PromoServiceClient.commit(batchId, reservationId)`
- Failure: silently swallowed — batch expires naturally if commit fails

### Compensation Pattern

All compensation calls use a `safeXxx` wrapper:

```java
private void safeReleaseInventory(UUID inventoryReservationId) {
    try {
        inventoryServiceClient.releaseSlot(inventoryReservationId);
    } catch (Exception e) {
        log.warn("Failed to release inventory reservation {}: {}", inventoryReservationId, e.getMessage());
    }
}
```

- Never re-throws — a failed compensation doesn't mask the original failure
- Logs at `warn` level for observability
- **Order is innermost-last** — always release inventory before rolling back promo (LIFO)

### Rate Limiting (Pre-saga guard)

`FlashSaleRateLimitFilter` — HTTP filter applied before the saga entry point:
- Matches: `POST /api/v1/bookings` only
- Redis key: `rate_limit:booking:{userId}`, 60-second window
- Default: `booking.rate-limit.flash-sale.requests-per-minute=5`
- Mechanism: Redis INCR + TTL sentinel (atomic, one round-trip); returns HTTP 429 with `RATE_LIMITED`

### Saga State

**No dedicated saga state table.** The `Reservation` row with `status=PENDING` is the implicit saga state.

| Status | Meaning |
|---|---|
| `PENDING` | Saga in progress or ledger hold step failed (awaiting expiry) |
| `CONFIRMED` | Saga completed successfully |
| `CANCELLED` | Cancelled by user or system |
| `MANUAL_REVIEW` | Cancellation failed after retries exhausted (ops intervention needed) |

If a compensation call fails mid-rollback, the `PENDING` reservation expires via the **inventory TTL sweeper**, which calls `compensate()` on the inventory port to restore available qty.

### Event Emission

All saga lifecycle events go through the **outbox pattern**, not direct Kafka sends:

| Event | Emitted by | Transaction boundary |
|---|---|---|
| `BookingCreated` | `ReservationWriter.writeReservation()` | Same `@Transactional` as reservation INSERT |
| `BookingConfirmed` | `ConfirmBookingService.confirm()` | Same `@Transactional` as status UPDATE |
| `BookingCancelled` | `CancelBookingService.cancel()` | Same `@Transactional` as status UPDATE |
| `RefundFailed` | `CancelBookingService.cancel()` | Same `@Transactional` as status UPDATE |

Consumers (e.g. `notification-service`) subscribe to these Kafka topics and react independently.

---

## Payment State Machine (payment-service)

Payment-service implements its own internal saga as a state machine:

```
INITIATED ──→ AUTHORIZED ──→ CAPTURED ──→ REFUNDED
                   │               │
                   └──→ CANCELLED  └──→ CANCELLED
                   └──→ FAILED     └──→ FAILED
```

Transitions are guarded by status checks in application services:

```java
// CapturePaymentService
if (payment.getStatus() != AUTHORIZED) throw new InvalidPaymentStateException();
gateway.capture(gatewayRef, amount, currency);
paymentWriter.updateStatus(paymentId, CAPTURED);  // @Transactional + outbox event
```

All transitions write an outbox event inside the same `@Transactional` call (`PaymentWriter`):

| Transition | Outbox event |
|---|---|
| `INITIATED → AUTHORIZED` | `PaymentAuthorized` |
| `AUTHORIZED → CAPTURED` | `PaymentCaptured` |
| `CAPTURED → REFUNDED` | `PaymentRefunded` |
| `* → CANCELLED` | `PaymentCancelled` |
| `* → FAILED` | `PaymentFailed` |

`InitiatePaymentService` and `CapturePaymentService` are **not** `@Transactional` themselves — they call the external gateway (Stripe HTTP) outside any DB transaction to avoid holding a connection open. The `@Transactional` boundary is in `PaymentWriter` (the sibling write service), which is called after the gateway responds.

---

## Hexagonal Wiring

```
adapter/in/web/BookingController
  → port/in/CreateBooking
    → application/service/CreateBookingService         (orchestrator, no @Transactional)
        → port/out/FraudServiceClient                  (gRPC adapter)
        → port/out/PromoServiceClient                  (HTTP adapter)
        → port/out/InventoryServiceClient              (HTTP adapter)
        → port/out/CancellationPolicyRepository        (jOOQ adapter)
        → application/service/ReservationWriter        (@Transactional DB write + outbox)
        → port/out/LedgerServiceClient                 (HTTP adapter)
```

The coordinator (`CreateBookingService`) never calls adapters directly — all downstream calls go through port/out interfaces.

---

## Gotchas

**No `@Transactional` on the saga orchestrator** — HTTP calls to downstream services must not be wrapped in a DB transaction (holds a connection for the duration of all HTTP round-trips). Extract DB writes to a sibling `@Transactional` service.

**Compensation order is LIFO** — always compensate in reverse order of acquisition. Releasing inventory before rolling back a promo batch is safe; the reverse risks leaving a committed coupon against a released slot.

**`safeXxx` wrappers are mandatory** — a compensation failure must not propagate as a new exception; the caller needs to see the original failure.

**DB reservation row is not compensated on ledger failure** — the `PENDING` row stays alive and expires via TTL sweeper. This is intentional: the sweeper handles cleanup asynchronously, avoiding a synchronous DB write in an error path that already has the original exception.

**`quoteRepository.markUsed()` is the idempotency guard** — on retry after a transient failure at step 6, the re-attempt will hit `QuoteAlreadyUsedException` if the first attempt actually committed. Upstream must treat this as a conflict (409), not a server error (500).

**Promo commit failure is silently swallowed** — step 8 failure is non-fatal by design: the promo batch has a TTL and will expire. If exact coupon accounting matters, a compensating event flow or a reconciliation job is needed.

**`FraudServiceStub` always returns `ALLOW`** — the real gRPC fraud adapter is not yet wired. Wire it by providing a Spring bean named `fraudGrpcClient` that implements `FraudServiceClient`; the `@ConditionalOnMissingBean(name = "fraudGrpcClient")` stub will yield automatically.

**`MANUAL_REVIEW` status requires ops intervention** — `CancelBookingService` sets this when the ledger refund retries exhaust. No automated compensation runs after this point; an ops agent must resolve manually.

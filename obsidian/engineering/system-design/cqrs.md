# CQRS (Command Query Responsibility Segregation)

## Core Idea

Separate the **write model** (commands that mutate state) from the **read model** (queries that return data). Each side is optimized independently.

```
Client
  ├── Command ──→ Write Model (normalised DB, domain logic)
  │                   ↓ (event / projection)
  └── Query  ──→ Read Model  (denormalised, query-optimised view)
```

Without CQRS, one model serves both purposes — normalized for integrity, but often slow or awkward to query (many joins, aggregate computations, cross-table lookups). CQRS lets the read side be shaped exactly for its consumers without compromising the write side.

---

## Commands vs Queries

| | Command | Query |
|---|---|---|
| **Intent** | Mutate state | Read state |
| **Return** | Void or minimal acknowledgement | Data |
| **Examples** | `CreateBooking`, `CapturePayment` | `GetBookingSummary`, `ListUserReservations` |
| **Side effects** | Yes — DB writes, events | No |
| **Idempotency** | Must be handled explicitly | Naturally safe to repeat |

The split is not just architectural — it enforces that query paths never accidentally trigger side effects, and command paths are never polluted with read-optimisation concerns.

---

## Projections

A **projection** is how the read model is built and kept in sync with the write model. Two approaches:

### Inline Projection (Synchronous)

The read model is updated **in the same DB transaction** as the write:

```java
@Transactional
void createBooking(CreateBookingCommand cmd) {
    Reservation reservation = reservationRepository.save(...);  // write model
    bookingSummaryView.upsert(BookingSummaryRow.from(reservation)); // read model — same txn
}
```

```
BEGIN TRANSACTION
  INSERT INTO reservations …          ← write model
  UPSERT INTO booking_summary_view …  ← read model (inline)
COMMIT
```

**Properties:**
- Read model is **immediately consistent** — the moment the command commits, the query side reflects it
- Both writes are atomic — if the command rolls back, the read model also rolls back
- Write path must know about the read model's schema — coupling between write and read sides
- Adding a new read model requires changing the write path

### Async Projection (Event-Driven)

The write side emits events (via outbox); a separate consumer updates the read model asynchronously:

```
BEGIN TRANSACTION
  INSERT INTO reservations …        ← write model
  INSERT INTO outbox_events …       ← event relay
COMMIT

[OutboxPoller] → Kafka → [ProjectionConsumer]
                              → UPSERT INTO booking_summary_view …
```

**Properties:**
- Read model is **eventually consistent** — lags behind the write model by the delivery latency
- Write path is decoupled from read model schema — multiple projections can consume the same event
- Adding a new read model requires a new consumer, no write path change
- Consumers must be idempotent (at-least-once delivery)

### Comparison

| | Inline Projection | Async Projection |
|---|---|---|
| **Consistency** | Immediate (same transaction) | Eventual (delivery lag) |
| **Atomicity** | Same txn — rollback cleans both | Separate txn — failure leaves them out of sync until retry |
| **Write path coupling** | Tight — write service knows read schema | Loose — write service only emits an event |
| **Multiple read models** | Each requires a write path change | Each is a new independent consumer |
| **Infrastructure** | None beyond the DB | Message broker + consumer |
| **Failure recovery** | Automatic (transaction rollback) | Consumer retry / dead-letter queue |
| **Query freshness** | Always up-to-date | May lag under load or failures |
| **Operational complexity** | Low | Higher (broker, consumers, lag monitoring) |

### When to Use Each

**Inline projection** is appropriate when:
- The read model is tightly owned by the same service as the write model
- Query freshness is critical (user expects to see their change immediately)
- The projection is simple (one or two extra writes)
- You want to avoid event broker infrastructure for a purely local concern

**Async projection** is appropriate when:
- Multiple independent consumers need to build their own views of the same event
- The projection belongs to a different service or bounded context
- Eventual consistency is acceptable (e.g. analytics dashboards, activity feeds)
- You want to decouple the write service from all downstream read concerns

---

## Relation to Event Sourcing

CQRS and Event Sourcing are different concepts that are often combined but don't require each other:

| | CQRS | Event Sourcing |
|---|---|---|
| **What it separates** | Read model from write model | Current state from event history |
| **Storage** | Separate tables/DBs for read and write | Events are the source of truth; current state is derived |
| **Projections** | Build read model from write model | Build any view by replaying events |
| **Can be used alone** | Yes — plain CQRS without event sourcing | Yes — event sourcing without separate read model |

**Event sourcing with CQRS**: events are the write model; projections (inline or async) build read models by replaying or streaming events. The outbox pattern fits naturally here — events are published from the event store to Kafka, consumers build projections.

**CQRS without event sourcing** (more common): normal write model (mutable DB rows); separate read model updated via inline projection or async projection. Atomic-book leans toward this.

---

## Relation to Outbox

The outbox pattern is the **infrastructure bridge** between the write side and async projections:

```
Write Side                    Outbox                    Read Side
──────────                    ──────                    ─────────
INSERT reservation     →   INSERT outbox_event   →   [Poller/CDC]
(same transaction)                                    → Kafka
                                                      → ProjectionConsumer
                                                          → UPSERT read model
```

- Without the outbox, publishing an event directly to Kafka inside a transaction is unsafe (broker call can fail after DB commits)
- The outbox makes async projections **reliable** — the event is guaranteed to be delivered if the transaction committed
- The idempotency requirement on consumers mirrors the at-least-once delivery guarantee of the outbox

Inline projection and the outbox write share the same mechanism — **atomic co-write in one transaction** — but serve different goals:

| | Outbox write | Inline projection write |
|---|---|---|
| **Target** | `outbox_events` relay table | Read model / view table |
| **Consumer** | External services via Kafka | Same service's query layer |
| **Consistency** | Eventual (after broker delivery) | Immediate |

---

## In Atomic-Book

Atomic-book does not implement explicit CQRS — each service queries the same normalized tables it writes to. However, several patterns in the codebase are natural precursors:

**Write and read on the same model (current state):**
- `BookingController` calls `CreateBookingService` (command) and `GetBookingService` (query) — the query reads directly from `reservations`
- No separate read table; joins are done at query time via jOOQ

**Patterns that point toward CQRS:**

| Current pattern | If CQRS were applied |
|---|---|
| `reservations` table queried with joins | `booking_summary_view` table updated inline or via event |
| `payment-service` queries payments by user | Async projection into `user_payment_history` consumer |
| Notification-service subscribes to `BookingConfirmed` Kafka events | Already an async projection — updates notification state from write-side events |
| Ledger double-entry writes | Natural fit for event sourcing; `account_balance_view` as a projection |

**`notification-service` is the closest to async CQRS** in the system: it consumes `BookingConfirmed`, `PaymentCaptured`, etc. events from Kafka (published via outbox) and builds its own send-queue state. The write side (booking/payment) emits events; notification-service projects them into dispatch records. This is async projection across a service boundary.

---

## Read Model Design Patterns

### Denormalised Summary Table

Pre-join data that is frequently queried together:

```sql
-- Write model (normalised)
reservations(id, user_id, slot_id, status, created_at)
slots(id, name, supplier_id)
payments(id, reservation_id, amount, status)

-- Read model (denormalised, inline-projected or async-projected)
booking_summary(
  reservation_id, user_id,
  slot_name, supplier_id,
  payment_amount, payment_status,
  reservation_status, created_at
)
```

### Aggregate View

Pre-compute aggregates that would require expensive GROUP BY at query time:

```sql
account_balance(account_id, current_balance, hold_amount, last_updated_at)
-- updated inline on every hold/capture/release in ledger-service
```

### Time-Series / Event Log View

Append-only table ordered by time for activity feeds or audit logs:

```sql
user_activity_log(id, user_id, event_type, summary, occurred_at)
-- appended via async projection from domain events
```

---

## Gotchas

**Inline projection increases transaction size** — every write transaction now does more work. Under high write throughput, this can increase lock contention and transaction duration. Profile before adding inline projections to hot paths.

**Async projection lag is observable** — the user creates a booking and immediately queries their booking list; the inline-projected summary may not appear if it's async. Design the UI to handle this (optimistic updates, loading states, eventual refresh).

**Projection schema changes require coordination** — for async projections, changing the read model schema requires updating the consumer and potentially replaying historical events. For inline projections, it requires a write path change.

**Event replay for new projections** — when adding a new async projection, you need historical events to build the initial state. The outbox table only holds recent unpublished events; for full history, event sourcing or a separate event log is needed.

**Avoid fat read models** — a projection that mirrors the entire write model defeats the purpose. Project only the fields the query actually needs.

# Transactional Outbox Pattern

## Problem

In distributed systems, writing to a database and publishing a message to a broker (Kafka, RabbitMQ) are two separate operations. A crash between them causes:
- DB write committed, event never published → downstream out-of-sync
- Event published, DB write rolled back → phantom event with no backing state

## Solution

Write the event into an `outbox_events` table **in the same DB transaction** as the domain write. A separate process reliably polls and publishes the outbox rows to the broker. The broker delivery is decoupled from the domain write.

```
[Service] ──── @Transactional ────────────────────────────────┐
                  ├── INSERT INTO reservations …              │
                  └── INSERT INTO outbox_events …             │
            ──────────────────────────────────────────────────┘
                                   ↓ (commit)
[OutboxPoller] ── FOR UPDATE SKIP LOCKED ──→ Kafka ──→ Consumer
```

## Event Model

```java
// outbox-lib: OutboxEvent.java
@Value @Builder
class OutboxEvent {
    UUID id;
    UUID aggregateId;      // root entity (e.g. reservationId)
    String aggregateType;  // e.g. "Reservation", "Payment"
    String eventType;      // e.g. "BookingCreated", "PaymentCaptured"
    String payload;        // JSON string
    Instant createdAt;
    Instant publishedAt;   // null until dispatched
}
```

## DB Schema

```sql
CREATE TABLE outbox_events (
  id             UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_id   UUID        NOT NULL,
  aggregate_type VARCHAR(100) NOT NULL,
  event_type     VARCHAR(200) NOT NULL,
  payload        JSONB       NOT NULL,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  published_at   TIMESTAMPTZ           -- NULL until published
);

-- Partial index: only unpublished rows; poller query hits this exactly
CREATE INDEX idx_outbox_unpublished ON outbox_events (created_at)
  WHERE published_at IS NULL;
```

## Delivery Modes

### 1. Polling (Pull)

The outbox library ships a `@Scheduled` poller that runs inside a transaction:

```
every fixedDelay (default 1s):
  BEGIN TRANSACTION
    SELECT … WHERE published_at IS NULL
      ORDER BY created_at
      FOR UPDATE SKIP LOCKED      ← concurrent-safe, no double-send
      LIMIT 50
    for each event:
      kafkaTemplate.send(topic, aggregateId, payload).get()  ← synchronous
      if success: add to successIds
      if InterruptedException: restore interrupt, break
      if other error: log warn, skip (retry next poll)
    UPDATE outbox_events SET published_at = NOW()
      WHERE id = ANY(successIds::uuid[])
  COMMIT
```

Key choices:
- **`fixedDelay`** (not `fixedRate`) — delay counts from job completion, prevents overlap for variable-duration batches
- **Synchronous `.get()`** — blocks until Kafka broker acks; at-least-once guarantee (row stays unpublished on timeout)
- **Partial success** — only successfully sent IDs are marked; failed events remain for next cycle
- **`FOR UPDATE SKIP LOCKED`** — multiple poller instances (replicas) can run safely; each locks a disjoint set of rows

### 2. CDC via Debezium (Push)

An alternative where `published_at` is never written. Debezium reads the WAL and streams inserts directly.

**Connector config** (`scripts/debezium/outbox-connector.json`):
```json
{
  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
  "plugin.name": "pgoutput",
  "slot.name": "outbox_slot",
  "publication.name": "outbox_publication",
  "table.include.list": "public.outbox_events",
  "tombstones.on.delete": "false",
  "transforms": "outbox",
  "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
  "transforms.outbox.table.field.event.key": "aggregate_id",
  "transforms.outbox.table.field.event.payload": "payload",
  "transforms.outbox.route.by.field": "event_type",
  "transforms.outbox.route.topic.replacement": "${routedByValue}"
}
```

**Topic routing:** each row's `event_type` becomes the Kafka topic name directly (e.g. `event_type='BookingCreated'` → topic `BookingCreated`). No prefix is prepended by the Event Router SMT.

**Polling vs CDC comparison:**

| | Polling | CDC (Debezium) |
|---|---|---|
| Delivery | At-least-once (synchronous `.get()`) | At-least-once (WAL) |
| Latency | Configurable (`poll.interval-ms`) | Near-realtime |
| `published_at` | Written after send | Never written |
| Extra infra | None | Debezium + logical replication slot |
| DB load | Periodic SELECT + UPDATE | WAL reads only |

## Library Integration (`outbox-lib`)

Auto-configures via `OutboxAutoConfiguration` (`@ConditionalOnClass(DSLContext.class)`). All beans are `@ConditionalOnMissingBean` — override any by providing your own.

**Adopting in a service:**
1. Add `outbox-lib` Maven dependency
2. Add `"classpath:db/outbox"` to `FlywayConfig` migration locations (creates `outbox_events`)
3. Add `spring-kafka` dependency + Kafka producer config
4. Inject `OutboxEventRepository` into your `@Transactional` writer service
5. Call `outboxEventRepository.save(OutboxEvent)` in the same transaction as your domain write

```java
// booking-service: ReservationWriter.java
@Service
class ReservationWriter {

    @Transactional
    Reservation writeReservation(CreateReservationCommand cmd) {
        quoteRepository.markUsed(cmd.quoteId());           // idempotency guard
        Reservation saved = reservationRepository.save(…); // domain write
        outboxEventRepository.save(OutboxEvent.builder()   // outbox write
            .aggregateId(saved.getId())
            .aggregateType("Reservation")
            .eventType("BookingCreated")
            .payload(objectMapper.writeValueAsString(Map.of(
                "reservationId", saved.getId(),
                "userId", saved.getUserId(),
                …
            )))
            .build());
        return saved;
    }
}
```

**Event types emitted per service:**

| Service | Event Types |
|---|---|
| booking-service | `BookingCreated`, `BookingConfirmed`, `BookingCancelled`, `RefundFailed` |
| payment-service | `PaymentAuthorized`, `PaymentCaptured`, `PaymentRefunded`, `PaymentCancelled`, `PaymentFailed` |

## In the Project (atomic-book)

Both delivery modes coexist. They share the same DB table, the same domain model, and the same port/out interface — only the publisher differs.

### Shared Infrastructure

```
outbox_events table (public schema)
       ↑ write (same for both modes)
OutboxEventRepository (port/out interface)
       ↑ inject
ReservationWriter / PaymentWriter (@Transactional service)
       └── reservationRepository.save(...)
       └── outboxEventRepository.save(...)   ← same call regardless of delivery mode
```

The service code that writes to the outbox is identical whether polling or CDC is configured downstream. The delivery mechanism is entirely transparent to the writer.

### Polling Path (default, enabled by `outbox-lib`)

```
OutboxAutoConfiguration
  → OutboxPollingPublisher (@Scheduled, fixedDelay=1s)
      → OutboxEventJooqRepository.findUnpublishedBatch(50)
          SELECT … WHERE published_at IS NULL FOR UPDATE SKIP LOCKED LIMIT 50
      → KafkaTemplate.send(eventType, aggregateId, payload).get()
      → OutboxEventJooqRepository.markPublished([ids])
          UPDATE outbox_events SET published_at = NOW() WHERE id = ANY(?)
```

`published_at` is the delivery marker. Undelivered rows have `published_at IS NULL` and will be retried on the next poll cycle.

### CDC Path (Debezium, enabled by `scripts/debezium/register-connector.sh`)

```
PostgreSQL WAL (logical replication, pgoutput plugin)
  → Debezium outbox connector (slot: outbox_slot)
      → EventRouter SMT
          route.by.field=event_type
          route.topic.replacement=${routedByValue}
      → Kafka topic (name = event_type value, e.g. "BookingCreated")
```

`published_at` is **never written**. Debezium tracks its WAL offset in the replication slot; the `outbox_events` rows are append-only. Re-delivery on restart is handled by replaying from the last committed WAL offset.

### What They Share

| | Polling | CDC |
|---|---|---|
| **Outbox table** | Same `public.outbox_events` | Same `public.outbox_events` |
| **Domain model** | `OutboxEvent` | `OutboxEvent` |
| **Port interface** | `OutboxEventRepository` | `OutboxEventRepository` |
| **Writer code** | Identical `outboxEventRepository.save(...)` | Identical `outboxEventRepository.save(...)` |
| **Topic naming** | `eventType` field → Kafka topic | `event_type` column → Kafka topic (via SMT) |
| **Kafka key** | `aggregateId.toString()` | `aggregate_id` column (via SMT `table.field.event.key`) |
| **Payload** | `payload` field (JSON string) | `payload` column (JSONB, delivered as string) |
| **Delivery guarantee** | At-least-once | At-least-once |

### What Differs

| | Polling | CDC |
|---|---|---|
| **Delivery marker** | `published_at` timestamp (written on success) | WAL offset in replication slot (never touches rows) |
| **Latency** | Up to `poll.interval-ms` (default 1 000 ms) | Near-realtime (WAL tail latency, typically < 100 ms) |
| **Retry on crash** | Rows with `published_at IS NULL` are retried on next poll | WAL offset rolled back; events re-streamed from last committed position |
| **Duplicate risk** | Poll transaction committed, Kafka ack lost → row already marked → no duplicate | WAL replayed from offset → duplicate if consumer not idempotent |
| **DB write amplification** | Extra `UPDATE published_at` per batch | None — rows are append-only |
| **Infrastructure** | None beyond the app | Debezium Connect cluster + Postgres logical replication slot |
| **Replication slot risk** | None | Unconsumed slot holds WAL indefinitely → disk exhaustion if Debezium lags |
| **Ordering** | `ORDER BY created_at` in SELECT | WAL order (insertion order) — same in practice |
| **Schema flexibility** | Can add routing logic in `TopicResolver` bean | Routing is SMT config; changing requires connector restart |
| **Outbox table growth** | Rows accumulate; needs a periodic `DELETE WHERE published_at IS NOT NULL` cleanup job | Rows accumulate; same cleanup needed |

### Which Mode Is Active When

- **Development / default**: polling only. `OutboxAutoConfiguration` activates automatically when `DSLContext` and `spring-kafka` are on the classpath. `published_at` is written after each send.
- **Production (with Debezium)**: `scripts/debezium/register-connector.sh` registers the connector. Both modes can technically run simultaneously — polling still marks rows while CDC also streams them — so in practice, **disable the polling publisher** (`outbox.polling.enabled=false` or remove the `spring-kafka` producer config) when running CDC to avoid double-publishing.
- **Testing**: polling mode only; Debezium is not started in `BaseIntegrationTest`. The test Kafka container receives events via the polling publisher.

### Consumer Idempotency Requirement

Both modes deliver **at-least-once**. Consumers must be idempotent:
- Use the `OutboxEvent.id` (UUID) as a deduplication key
- `idempotency-lib`'s two-phase store (`INSERT ON CONFLICT DO NOTHING`) is the recommended approach for any consumer that performs a DB write in response to an event
- For notification-service (email/SMS send), natural idempotency via per-user/per-event deduplication keys is sufficient

---

## Relation to CQRS and Inline Projection

The outbox pattern and inline projection are two different responses to the same underlying question: *how do you keep a second piece of state consistent with the first?*

### Dual-Write in One Transaction

Both patterns solve their consistency problem using the same mechanism — writing two things atomically in one DB transaction:

```
Outbox:
  BEGIN TRANSACTION
    INSERT INTO reservations …          ← domain write
    INSERT INTO outbox_events …         ← event relay (for broker delivery)
  COMMIT

Inline Projection:
  BEGIN TRANSACTION
    INSERT INTO reservations …          ← domain write
    UPSERT INTO booking_summary_view …  ← read model (for queries)
  COMMIT
```

The structural pattern is identical. The intent differs:

| | Outbox write | Inline projection write |
|---|---|---|
| **Target** | `outbox_events` relay table | Query-optimised read model table |
| **Consumer** | External services via Kafka (async) | Same service's query layer (sync) |
| **Consistency** | Eventual — after broker delivery | Immediate — visible after commit |
| **Coupling** | Write side decoupled from read schema | Write side knows read schema |
| **Infrastructure** | Broker + poller/CDC | None beyond the DB |

### Outbox as the Bridge for Async Projections

In a CQRS architecture, async projections need a reliable way to receive write-side events. The outbox is that bridge:

```
Write Side                 Outbox                   Read Side
──────────                 ──────                   ─────────
INSERT reservation  →  INSERT outbox_event  →  [Poller/CDC]
(same transaction)                              → Kafka
                                                → ProjectionConsumer
                                                    → UPSERT read model
```

Without the outbox, publishing directly to Kafka inside a transaction is unsafe — the broker call can fail after the DB commits, leaving the event permanently lost. The outbox guarantees the event is delivered if the transaction committed, making async projections reliable.

### Choosing Between Them

Use **inline projection** when:
- The read model is owned by the same service as the write model
- Immediate consistency is required (user sees their change right away)
- The projection is simple (one or two extra rows)

Use **outbox + async projection** when:
- The read model belongs to a different service or bounded context
- Multiple consumers need independent views of the same event
- Eventual consistency is acceptable

In atomic-book, `notification-service` is the clearest example of outbox-driven async projection: booking-service emits `BookingConfirmed` via outbox → Kafka → notification-service builds its dispatch queue. The write side (booking) has no knowledge of the read side (notification).

---

## Ports & Adapters

```
application/port/out/OutboxEventRepository     ← port interface
adapter/out/persistence/OutboxEventJooqRepository  ← jOOQ impl
outbox/publisher/OutboxPollingPublisher        ← @Scheduled poller
outbox/config/OutboxAutoConfiguration          ← Spring auto-config
```

## Gotchas

**`publication.autocreate.mode: filtered` fails if table missing** — use `all_tables` until Flyway has run and created `outbox_events`.

**Payload must be serialized JSON, never `String.format`** — use `objectMapper.writeValueAsString(Map.of(...))`. String formatting silently produces invalid JSON on special characters.

**`Map.of()` rejects null values** — use `LinkedHashMap` for payloads with conditionally present fields.

**Event DTOs belong in `application/port/in/event/`** — not in `adapter/in/kafka/`. Application services must not import adapter packages.

**Kafka event DTOs must carry an explicit `userId`** — never pass a related entity ID (e.g. `bookingId`) where `userId` is required; the consuming service can't look it up.

**Outbox Flyway migration must use a separate history table** — `outbox-lib`, `idempotency-lib`, and the service each ship `V1`. Use three `Flyway` beans pointing to distinct `flyway_schema_history_<name>` tables. Secondary beans need `baselineOnMigrate(true)` + `baselineVersion("0")`.

**Debezium Event Router SMT topic routing** — `route.topic.replacement=${routedByValue}` routes to the topic named exactly after `event_type`; no `topic.prefix` is prepended. Don't confuse this with the connector-level `topic.prefix` (used only for non-outbox tables).

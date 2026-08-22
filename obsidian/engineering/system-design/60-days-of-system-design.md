# 60 Days of System Design Questions

> A question-a-day workbook — scenario, four options, and the reasoning behind the right call.
> Author: Joud Awad · 60 questions · 240 explanations

---

## Outline by Category

> Study outline grouping the questions above into 12 categories. Each category has a unifying theme and the core principle it drills.

### 1. API Design & Service Architecture

_Boundary definition, client coupling, deployment granularity_

- [[#Day 01: Decoupling Mobile from Backend Services|Day 01 — Decoupling Mobile from Backend Services]]
- [[#Day 47: Incrementally Strangling a Monolith ⭐|Day 47 — Incrementally Strangling a Monolith ⭐]]
- [[#Day 52: Versioning an API Without Breaking Clients|Day 52 — Versioning an API Without Breaking Clients]]
- [[#Day 56: Tracking Long-Running Async Jobs|Day 56 — Tracking Long-Running Async Jobs]]
- [[#Day 60: Architecting a SaaS Platform from Scratch ⭐|Day 60 — Architecting a SaaS Platform from Scratch ⭐]]

### 2. Database Performance & Scaling

_Query efficiency, write cost, index/partition strategy_

- [[#Day 02: Killing the N+1 Query Problem|Day 02 — Killing the N+1 Query Problem]]
- [[#Day 05: Choosing a Database Sharding Strategy ⭐|Day 05 — Choosing a Database Sharding Strategy ⭐]]
- [[#Day 12: Indexing a High-Ingest Table ⭐|Day 12 — Indexing a High-Ingest Table ⭐]]
- [[#Day 13: Managing a Shared Connection Pool|Day 13 — Managing a Shared Connection Pool]]
- [[#Day 16: Taming a Hot Partition Key ⭐|Day 16 — Taming a Hot Partition Key ⭐]]
- [[#Day 24: Paginating Large Result Sets Efficiently ⭐|Day 24 — Paginating Large Result Sets Efficiently ⭐]]
- [[#Day 49: Controlling Data-Warehouse Query Costs|Day 49 — Controlling Data-Warehouse Query Costs]]
- [[#Day 53: Zero-Downtime Schema Migrations ⭐|Day 53 — Zero-Downtime Schema Migrations ⭐]]

### 3. Data Modeling: Read/Write Shape & History

_Separating read shape from write shape; reconstructing state_

- [[#Day 09: Splitting Read and Write Data Models ⭐|Day 09 — Splitting Read and Write Data Models ⭐]]
- [[#Day 23: Feed Fanout for Celebrity Accounts ⭐|Day 23 — Feed Fanout for Celebrity Accounts ⭐]]
- [[#Day 33: Reconstructing State with Event Sourcing ⭐|Day 33 — Reconstructing State with Event Sourcing ⭐]]

### 4. Caching

_Freshness vs speed, invalidation, thundering herds_

- [[#Day 08: Keeping Cache and Database in Sync ⭐|Day 08 — Keeping Cache and Database in Sync ⭐]]
- [[#Day 15: Fast "Has the User Seen This?" Checks ⭐|Day 15 — Fast "Has the User Seen This?" Checks ⭐]]
- [[#Day 18: Surviving a Cache Stampede ⭐|Day 18 — Surviving a Cache Stampede ⭐]]
- [[#Day 26: Write-Path Cache Consistency ⭐|Day 26 — Write-Path Cache Consistency ⭐]]
- [[#Day 43: Reliable CDN Cache Invalidation on Deploy|Day 43 — Reliable CDN Cache Invalidation on Deploy]]

### 5. Consistency & Concurrency

_Lost updates, races, coordination, convergence_

- [[#Day 06: Safe Distributed Locks for Cron Jobs ⭐|Day 06 — Safe Distributed Locks for Cron Jobs ⭐]]
- [[#Day 19: Read-Your-Writes with Read Replicas ⭐|Day 19 — Read-Your-Writes with Read Replicas ⭐]]
- [[#Day 37: Multi-Writer Conflicts in Collaborative Editing ⭐|Day 37 — Multi-Writer Conflicts in Collaborative Editing ⭐]]
- [[#Day 39: Preventing Concurrent Balance Overspend ⭐|Day 39 — Preventing Concurrent Balance Overspend ⭐]]
- [[#Day 44: Syncing Offline Edits Without Data Loss ⭐|Day 44 — Syncing Offline Edits Without Data Loss ⭐]]
- [[#Day 57: Consistency for Payment-Confirmation Reads ⭐|Day 57 — Consistency for Payment-Confirmation Reads ⭐]]

### 6. Messaging, Events & Async Workflows

_Ordering, delivery guarantees, distributed transactions_

- [[#Day 07: Event Ordering in a Message Queue ⭐|Day 07 — Event Ordering in a Message Queue ⭐]]
- [[#Day 10: Distributed Transactions Across Services ⭐|Day 10 — Distributed Transactions Across Services ⭐]]
- [[#Day 11: Handling Webhook Retries Idempotently ⭐|Day 11 — Handling Webhook Retries Idempotently ⭐]]
- [[#Day 17: Backpressure on an Overwhelmed Consumer ⭐|Day 17 — Backpressure on an Overwhelmed Consumer ⭐]]
- [[#Day 22: Reliable Messaging Across Services ⭐|Day 22 — Reliable Messaging Across Services ⭐]]
- [[#Day 25: Queue Backpressure Under a Traffic Spike|Day 25 — Queue Backpressure Under a Traffic Spike]]
- [[#Day 41: Moving from Batch to Real-Time Streaming|Day 41 — Moving from Batch to Real-Time Streaming]]

### 7. Reliability & Resilience

_Failure containment, retries, rollouts, abuse protection_

- [[#Day 03: Rate Limiting Without Boundary Bursts ⭐|Day 03 — Rate Limiting Without Boundary Bursts ⭐]]
- [[#Day 04: Preventing Duplicate Payment Charges ⭐|Day 04 — Preventing Duplicate Payment Charges ⭐]]
- [[#Day 14: Safely Rolling Out a Risky Change ⭐|Day 14 — Safely Rolling Out a Risky Change ⭐]]
- [[#Day 20: Containing a Failing Downstream Dependency ⭐|Day 20 — Containing a Failing Downstream Dependency ⭐]]
- [[#Day 59: Designing Idempotency Keys for Payments ⭐|Day 59 — Designing Idempotency Keys for Payments ⭐]]

### 8. Networking, Infrastructure & Multi-Region

_Transport, storage, secrets, geography_

- [[#Day 21: Choosing a Real-Time Streaming Transport|Day 21 — Choosing a Real-Time Streaming Transport]]
- [[#Day 30: Choosing a File Storage Backend|Day 30 — Choosing a File Storage Backend]]
- [[#Day 31: Cutting Cross-Region Latency ⭐|Day 31 — Cutting Cross-Region Latency ⭐]]
- [[#Day 32: Managing Secrets and Credentials|Day 32 — Managing Secrets and Credentials]]
- [[#Day 36: Choosing HTTP/3 vs HTTP/2 at the Edge|Day 36 — Choosing HTTP/3 vs HTTP/2 at the Edge]]

### 9. Specialized Systems at Scale

_Domain-specific data structures and engines_

- [[#Day 35: Geospatial "Find Nearby Drivers" at Scale ⭐|Day 35 — Geospatial "Find Nearby Drivers" at Scale ⭐]]
- [[#Day 45: Scaling Full-Text Search ⭐|Day 45 — Scaling Full-Text Search ⭐]]
- [[#Day 50: Serving ML Models at High Throughput ⭐|Day 50 — Serving ML Models at High Throughput ⭐]]
- [[#Day 51: Isolating Noisy Tenants in Multi-Tenant SaaS ⭐|Day 51 — Isolating Noisy Tenants in Multi-Tenant SaaS ⭐]]

### 10. Frontend

_Main-thread and rendering concerns_

- [[#Day 40: Offloading Heavy Work Off the Main Thread|Day 40 — Offloading Heavy Work Off the Main Thread]]

### 11. LLM / GenAI — Foundations

_Retrieval, embeddings, model output control_

- [[#Day 27: Keeping an LLM's Answers Up to Date|Day 27 — Keeping an LLM's Answers Up to Date]]
- [[#Day 28: Choosing a Vector Store for Semantic Search|Day 28 — Choosing a Vector Store for Semantic Search]]
- [[#Day 34: Improving LLM Classification Accuracy|Day 34 — Improving LLM Classification Accuracy]]
- [[#Day 38: Fitting a Large Document into an LLM|Day 38 — Fitting a Large Document into an LLM]]
- [[#Day 46: Enforcing Structured Output from an LLM|Day 46 — Enforcing Structured Output from an LLM]]
- [[#Day 54: Handling Embedding Drift in RAG|Day 54 — Handling Embedding Drift in RAG]]

### 12. AI Agents — Orchestration & Operations

_Multi-step reasoning, tool use, memory, observability_

- [[#Day 29: Coordinating a Multi-Agent Workflow|Day 29 — Coordinating a Multi-Agent Workflow]]
- [[#Day 42: Designing Memory for an AI Agent|Day 42 — Designing Memory for an AI Agent]]
- [[#Day 48: How an Agent Chooses Which Tools to Call|Day 48 — How an Agent Chooses Which Tools to Call]]
- [[#Day 55: Parallel Agents with Shared State|Day 55 — Parallel Agents with Shared State]]
- [[#Day 58: Observability for LLM Agent Pipelines|Day 58 — Observability for LLM Agent Pipelines]]

### Cross-Cutting Threads

_Study these across categories — same idea at different boundaries_

#### Idempotency

- [[#Day 04: Preventing Duplicate Payment Charges ⭐|Day 04]]
- [[#Day 11: Handling Webhook Retries Idempotently ⭐|Day 11]]
- [[#Day 22: Reliable Messaging Across Services ⭐|Day 22]]
- [[#Day 59: Designing Idempotency Keys for Payments ⭐|Day 59]]

#### Consistency

- [[#Day 08: Keeping Cache and Database in Sync ⭐|Day 08]]
- [[#Day 19: Read-Your-Writes with Read Replicas ⭐|Day 19]]
- [[#Day 26: Write-Path Cache Consistency ⭐|Day 26]]
- [[#Day 57: Consistency for Payment-Confirmation Reads ⭐|Day 57]]

#### Write Amplification

- [[#Day 02: Killing the N+1 Query Problem|Day 02]]
- [[#Day 05: Choosing a Database Sharding Strategy ⭐|Day 05]]
- [[#Day 09: Splitting Read and Write Data Models ⭐|Day 09]]
- [[#Day 12: Indexing a High-Ingest Table ⭐|Day 12]]
- [[#Day 23: Feed Fanout for Celebrity Accounts ⭐|Day 23]]

#### Scale ≠ Distribution

- [[#Day 31: Cutting Cross-Region Latency ⭐|Day 31]]
- [[#Day 45: Scaling Full-Text Search ⭐|Day 45]]
- [[#Day 60: Architecting a SaaS Platform from Scratch ⭐|Day 60]]

---

## Day 01: Decoupling Mobile from Backend Services

**Scenario:** Mobile app talks directly to 3 backend services. A 4th (NotificationService) ships next sprint. The mobile team is drowning in domain sprawl: new domain to whitelist, new auth scheme, new error shape per service. Reduce coupling before the new service lands.

> [!success] **A: API Gateway** ✅ — single entry point (`api.yourapp.com`), one domain, one auth flow, one error contract. New services = one route added, zero mobile changes. Centralizes authN/authZ, rate limiting, request logging, TLS termination, versioning. Netflix, Stripe, every mature fintech runs this.

- [ ] **B: BFF (Backend for Frontend)** — solves data shape per client type (mobile vs web payload). Here the pain is domain sprawl + coupling, not payload shape. Puts 4 URLs → 1 URL + 1 extra service you own end-to-end. Wrong tradeoff.
- [ ] **C: Load Balancer** — distributes traffic across identical instances of the same service. Can't route `/orders` here and `/users` there — that's application-layer routing (what an API Gateway does).
- [ ] **D: GraphQL Federation** — solves schema unification, not transport-layer coupling. Still needs a gateway in front; requires rewriting every backend service to expose a GraphQL subgraph. Multi-quarter migration for a sprint-sized problem.

---

## Day 02: Killing the N+1 Query Problem

**Scenario:** `/orders` endpoint loads 50 orders. P95 = 2.4s. 51 queries per request: one SELECT for the list, then 50 more (one per order) to fetch the customer. The ORM is lazy-loading `order.customer` inside a map.

> [!success] **A: Eager-load the relation** ✅ — `include: { customer: true }`. One LEFT JOIN, single round trip, P95 drops to ~80ms. No new infrastructure, no new failure modes. Prisma's `include`, Sequelize's `include`, TypeORM's `relations` — every ORM has this. Reach for fancier patterns only when JOIN genuinely can't solve it.

- [ ] **B: DataLoader** — beautiful pattern but earns its keep in GraphQL where the resolver graph fans out in ways a single JOIN can't express. Here you have one list endpoint with one relation. JOIN is simpler and faster. Paying a complexity tax forever.
- [ ] **C: Redis cache-first** — still 50 cache GETs per request, now own cache invalidation every time a customer updates, cold-hit every ID after deploy. Cache is a scaling tool, not an N+1 tool.
- [ ] **D: Denormalize `customer_name` onto orders** — legitimate at Instagram scale. But also how you serve a maiden name three years after marriage because nobody wrote the update path. Write-amplification decision masquerading as read-optimization. Do it when JOIN can't hit your latency SLO at your scale.

---

## Day 03: Rate Limiting Without Boundary Bursts ⭐

**Scenario:** POST `/v1/messages` is the money endpoint. Plan limit: 100 req/min per API key. Customers get 429s at minute boundaries even though average RPS is under cap. Fixed-window counter resets at 13:00:00 → 90 requests at 12:59:58 + 90 more at 13:00:02 = 180 requests in 4 seconds.

- [ ] **A: Fixed Window** — literally the bug described. Counter resets at minute boundary → customers burst 2x their limit in a 2-second window. Most common production mistake.
- [ ] **B: Sliding Window Log** — mathematically perfect but stores one Redis entry per request per key. At 100k active keys = real memory pressure and p99 latency spikes. Smart engineers pick it without thinking about memory cost.

> [!success] **C: Token Bucket** ✅ — each API key gets 100 tokens, refilling at ~1.66 tokens/sec. Every request takes a token; empty bucket = 429. No window resets — the 12:59:58 burst drains the bucket, and 13:00:02 finds an almost-empty bucket. O(1) memory, O(1) check, trivially distributed. What AWS API Gateway, Stripe, GitHub all run.

- Token bucket doesn't eliminate burtiness, it caps the burst to the bucket size and smooths the refill

- [ ] **D: Leaky Bucket** — shapes output by queuing requests at constant dispatch rate. Great for protecting a fragile downstream. Wrong for customer-facing API: adds latency to legitimate bursts. Token Bucket rejects excess; Leaky Bucket delays it. For a public API, reject > delay.
- Leaky bucket delays excess/adds latency

---

## Day 04: Preventing Duplicate Payment Charges ⭐

**Scenario:** User taps "Pay \$499." Spinner hangs. Taps again. And once more. Three requests hit the Payments API. Two succeed. Customer charged \$1,497. Three near-identical POSTs within 4 seconds.

- [ ] **A: Unique constraint on `(orderId, amount)`** — stops the second INSERT from committing, but what about the first charge to Stripe? Request #1 charges Stripe, DB insert succeeds. Request #2 charges Stripe again, then DB insert fails with constraint violation. Customer charged twice, DB looks clean. Even if you flip the order, you now have a payment row with no actual charge when #1 crashes. Great defense-in-depth, not the primary mechanism.

> [!success] **B: Idempotency-Key header** ✅ — client generates a UUID before the first request, attaches it on every retry. Server does work once, stores `{key → response}` in durable store, returns cached result on retry. Critical detail: cache the full response (status + body), not just "I saw this key." If retry #2 arrives while #1 is still processing, make it wait or return 409. This is exactly what Stripe, PayPal, Shopify, AWS all ship.

- [ ] **C: Distributed lock (Redis SETNX) on `orderId`** — serializes concurrent retries, but doesn't help with sequential retries arriving after lock is released and the response was lost in transit. Lock long gone, you charge again. Distributed locks = preventing concurrent execution. Idempotency = preventing repeated execution across time. Different problems.
- [ ] **D: SERIALIZABLE transaction** — protects the database from concurrent-write anomalies, has nothing to say about the external side effect (the HTTP POST to Stripe). Transaction rolls back, DB is pristine, but the money is gone. Treating the DB as the boundary of correctness when the real boundary is the external side effect.

---

## Day 05: Choosing a Database Sharding Strategy ⭐

**Scenario:** Postgres orders table at 500M rows, growing 3M/week. 80% reads = "customer X's last 30 days of orders." 15% reads = analytics joins on date ranges. 5% writes = new orders (400 RPS steady, 2x on sale days).

- [ ] **A: Hash sharding on `order_id`** — classic tutorial answer. Wrecks you here: a single customer's 200 orders scatter across all shards. Every read becomes a 4-shard fan-out gated by your slowest node. P99 latency goes up.
- [ ] **B: Range sharding on `created_at`** — creates a hot shard by design. Every new order writes to the same shard. Newest shard absorbs 100% of writes and 70% of reads. On Black Friday, this shard melts while others sit idle.

> [!success] **C: Directory-based sharding** ✅ — keep a `customer_shard_map` table (cached in Redis). Every order for a customer on exactly one shard. Customer-scoped read hits one node, no scatter-gather fan-out. If shard 3 gets hot, migrate specific heavy customers (whales) without rehashing anything. Targeted rebalancing is the superpower. Figma, Notion, Slack do this.

- [ ] **D: Consistent hashing with virtual nodes** — great for uniform data, but you can't migrate specific heavy tenants. If four whales land on the same shard, you are stuck.

---

## Day 06: Safe Distributed Locks for Cron Jobs ⭐

**Scenario:** Job scheduler on 3 instances. Redis SETNX lock with 300s TTL. Instance B wins lock, starts job, gets OOM-killed at 60s. Lock still held for 4 more minutes. Instance B's pod restarts and also tries to run it. Both processing same job. Worse: GC pause makes instance A hold lock past TTL — Redis quietly gives lock to instance C. Both think they own it.

> [!success] **A: SETNX + short TTL + fencing token** ✅ — every lock acquisition hands out a monotonically increasing token (42, 43, 44). Downstream resource (DB, storage) remembers the highest token seen and rejects any write with a lower token. When instance A wakes up from GC pause with token 42 and instance C is writing with token 43, A's write gets rejected by the resource itself. This is what Google's Chubby does. Only pattern on this list that's safe against process pauses.

- fencing token: the lock service hands you a monotonically increasing number. the shared resouce remembers the highest token it has seen and rejects any write with lower token -> prevent a service holding lock longer than TTL

```
   t0  B: acquire → token 42          resource: highest_seen = 42
   t1  B: writing (token 42) ✅
   t2  B: GC pause (2 min, > TTL)
   t3  lock expires, C: acquire → token 43   resource: highest_seen = 43
   t4  C: writing (token 43) ✅
   t5  B: wakes up, writes (token 42) → resource rejects ❌  (42 < 43)
```

- [ ] **B: Redlock** — Martin Kleppmann's 2016 post showed Redlock is unsafe in the exact GC-pause scenario. Without a fencing token, same fundamental flaw as SETNX. You're maintaining 5 Redis clusters for a problem a fencing token solves on 1.
- [ ] **C: DB pessimistic lock (`SELECT ... FOR UPDATE`)** — works for tiny critical sections. Lock auto-releases when transaction ends. But a 60-second report job holds a row lock on your primary DB for 60 seconds. Connection pool starved. Every other query blocked behind it.
- [ ] **D: Optimistic concurrency** — beautiful when work is idempotent and a single write. Breaks when the job involves external API calls, S3 writes, Slack pings. Three instances racing = triple the compute cost.

---

## Day 07: Event Ordering in a Message Queue ⭐

**Scenario:** Order service publishes 3 events per order: `created`, `paid`, `cancelled`. Standard SQS, 5 consumers, ~2K orders/min. 47 orders stuck in "cancelled" state with no "created" record. Events arrived in order but consumed in parallel — "cancelled" got processed first, state machine rejected "created" as invalid.

> [!success] **A: SQS FIFO + `MessageGroupId` per `order_id`** ✅ — don't need global ordering, need per-order ordering. Set `MessageGroupId = order_id`. FIFO guarantees same group ID delivered in exact send order, one consumer processing that group at a time. 2K orders/min still fan out across 5 workers — throughput unchanged. Ship it Monday.

- [ ] **B: Reorder buffer** — in-memory buffer per `order_id` + TTL logic + dead-letter path for gaps + crash recovery + stuck buffer monitoring. You just rebuilt FIFO in app code. Valid only when you can't use FIFO (e.g. Kafka with a taken partition key). Not here.
- [ ] **C: Saga** — for long-running distributed transactions with compensating actions (book flight → charge card → reserve hotel). This is a state stream for one entity, not a multi-service transaction. Forces async events into sync RPC, increases coupling, still doesn't fix ordering.
- [ ] **D: Event versioning + order-agnostic state machine** — partially works but drops legitimate events. "cancelled" arrives first, moves state forward, "created" gets rejected. DB says order is cancelled with no creation record. Full event sourcing needed to make D correct (6-month rewrite, not a Monday fix).

---

## Day 08: Keeping Cache and Database in Sync ⭐

**Scenario:** E-commerce product catalog. Redis in front of Postgres. 40K RPS peak. Within 48 hours of prod: wrong prices, old stock counts, products showing "available" that shipped out hours ago. Multiple write paths: admin panel, inventory service, order service.

- [ ] **A: Write-through** — "write to both atomically" — except no distributed transaction between Redis and Postgres. Write to Postgres, then Redis. Redis write fails → consistent Postgres + stale Redis. Worse: couples every service to Redis; one Redis outage takes down the entire write path.
- [ ] **B: Write-behind (write-back)** — Redis becomes source of truth. Loses data during failovers, OOM kills, AOF lag. "Might lose the last few price updates" is not defensible when real money is involved. Belongs in metrics pipelines, not e-commerce write paths.

> [!success] **C: Cache-aside (lazy loading)** ✅ — each writer updates Postgres → invalidates cache key (`DEL product:123`) → next read misses → fetches fresh data → repopulates Redis. Postgres stays the uncontested source of truth. Redis is a disposable read accelerator. If Redis dies, app still works — slower, but correct. What Shopify, Etsy, and most AWS reference architectures run in prod.

- [ ] **D: Read-through** — only solves the read side. Writes still going through 3 different services with nothing telling the cache. Doesn't fix stale data from multiple writers — still need invalidation on top, which is just cache-aside with extra steps.

---

## Day 09: Splitting Read and Write Data Models ⭐

**Scenario:** Orders service: 8K writes/min, 40K reads/min. Same tables, same schema. Write side needs normalized (orders, line_items, payments, shipments, addresses — clean FKs, ACID). Read side wants denormalized — dashboard joins 7 tables per order card, reporting queries light up CPU at 85% every 9am. Tuned indexes, added caching — the fundamental problem is schema shape mismatch.

> [!success] **A: Full CQRS** ✅ — separate read/write models (not request routing). Write side stays normalized, ACID, FK-enforced. Read side is a flat `order_view` table (or Elasticsearch index) where every order card renders from one row, zero joins. Projector keeps them in sync (outbox → Kafka → read-model updater, or CDC). Eat eventual consistency — dashboard might lag a few hundred ms. For the 5% of reads needing strong consistency (user's own order confirmation), read from write side directly.

- [ ] **B: Read replicas** — fixes read load, not read shape. The 7-table join is still a 7-table join — just runs on different hardware. Moved the CPU bill, not removed it. Right when joins are structurally fine but primary is overwhelmed. Wrong when the joins themselves are the problem.
- [ ] **C: Denormalize the write model** — every line-item change rewrites the order row. Every address update cascades through every order ever placed. Write amplification compounds at 8K writes/min. Schema ossifies. Buys a quarter, mortgages two.
- [ ] **D: GraphQL + DataLoader** — DataLoader batches API calls, not joins. The 7-table join still happens in the database. 3 months of GraphQL migration later, reads are exactly as slow as before.

---

## Day 10: Distributed Transactions Across Services ⭐

**Scenario:** Order #4471: OrderService creates order ✅ → PaymentService charges $89.50 ✅ → InventoryService tries to reserve SKU → fails (oversold by 3 units). Now holding customer's money, no inventory to ship, order stuck in PENDING. In a monolith you'd ROLLBACK. Can't do that across 4 services with 4 databases.

- [ ] **A: Choreography Saga** — elegant on paper. Falls apart at 4+ steps with branching compensations. Business logic for "what happens when inventory fails after payment succeeded" smeared across 3 services that all need to know each other's failure modes. Nobody owns the flow. At 3am, piecing together state from events across 4 Kafka topics.

> [!success] **B: Orchestration Saga** ✅ — a central CheckoutSaga state machine (Temporal, AWS Step Functions, Camunda) calls each service in order: OrderService → PaymentService → InventoryService → ShippingService. Each step has a registered compensation: CancelOrder, RefundPayment, ReleaseInventory. When Inventory fails, orchestrator walks backward and refunds automatically. State is durable, observable, replayable. At 3am you see exactly which step failed with full inputs/outputs.

- [ ] **C: Two-Phase Commit (2PC)** — Stripe doesn't speak 2PC. Neither does any shipping carrier API. Holds locks during PREPARE — one slow service stalls everything. At checkout volumes, lock contention alone takes you down.
- [ ] **D: Outbox + eventual consistency** — Outbox is infrastructure, not a saga. It solves how to reliably publish events after local DB commit. Doesn't define step ordering, compensations, or what happens when Inventory fails. You'd still need a saga on top.

---

## Day 11: Handling Webhook Retries Idempotently ⭐

**Scenario:** Stripe POSTs `charge.succeeded` to `/webhooks/stripe`. Pod was mid-restart, webhook timed out. Stripe retries. Three failure modes: pod restarts mid-deploy (double processing), DB slow at peak (handler takes 12s → Stripe times out → retries while first still running), events arriving out of order (`charge.succeeded` then `charge.refunded` 200ms apart).

- [ ] **A: Idempotency key + dedup table** — absolutely need it, but incomplete alone. Dedup table on `event.id` with unique constraint is table stakes. But handler is still synchronous, still on the critical 10-second path, still getting killed by pod restarts mid-write. Idempotency is a property the handler must have, not an architecture. C is the architecture; A lives inside it.
- [ ] **B: Retry + DLQ** — Stripe already does retry with exponential backoff (up to 3 days). You'd be duplicating provider behavior. Retry + DLQ is right for your internal queue (the one C creates), not for the webhook endpoint itself.

> [!success] **C: Verify signature, return 200 immediately, push to internal queue** ✅ — validate HMAC signature in <5ms, write raw payload to SQS/Kafka/Redis Streams, return 200. Handler bounded by network + signature verification, not by downstream services. Pod restart mid-processing? Message already durable in queue. DB slow? Webhook endpoint doesn't care — returned 200 in 8ms. This is what Stripe, Shopify, and GitHub literally tell you to do in their webhook docs.

- [ ] **D: Sequence numbers + reorder buffer** — most webhook providers don't give sequence numbers (Stripe doesn't, GitHub doesn't). Ordering at the receiver is wrong layer — handle at domain level with a state machine. State machines beat reorder buffers: handle out-of-order arrivals AND the case where one event never arrives.

---

## Day 12: Indexing a High-Ingest Table ⭐

**Scenario:** Events table on PostgreSQL 15, 200M rows, 8K writes/sec from Kafka consumer. P99 write latency climbed from 12ms to 140ms. Already has 4 indexes — each new write touches every one. But 92% of dashboard queries hit a single tenant's last 7 days of signup events. A tiny slice of a huge table.

- [ ] **A: Full composite B-tree on `(tenant_id, event_type, created_at)`** — dashboard fast, but indexing every single one of 8K writes/sec across all tenants and event types. Paying full write cost to serve a query hitting 0.2% of data.
- [ ] **B: Covering index with `INCLUDE (user_id, payload)`** — looks gorgeous in EXPLAIN. But `payload` is a JSONB blob averaging a few KB. Every insert writes the row to heap AND a fat index entry. Every UPDATE rewrites the index entry. You multiplied write cost. INCLUDE is right for narrow columns on read-heavy tables.
- [ ] **C: Read replica** — indexes still have to exist somewhere. Put them on replica and it falls behind replaying WAL. Put them on primary and you're back to original problem. Read replicas solve "primary can't serve all reads" — not "write path bottlenecked by index maintenance."

> [!success] **D: Partial index** ✅ — `WHERE event_type = 'signup' AND created_at > now() - interval '7 days'`. Only indexes rows matching the predicate. If signup events are ~4% of stream and 7-day window covers ~5% of table, partial index covers ~0.2% of rows. Inserts that don't match the predicate cost nothing on this index. Planner uses it for any query whose WHERE is a subset of the index predicate. Catch: when dashboard wants 30 days instead of 7, you rebuild. Known cost, not hidden.

- what you pay on the write path of full/partial indexes?
  - full b-tree is updated for every single row, partial b-tree is updated row matching the predicate

---

## Day 13: Managing a Shared Connection Pool

**Scenario:** 3 workloads against one Postgres RDS. `max_connections = 300`. NestJS REST API (short transactions, 800 RPS, 10 tasks × 40 pool = 400 requested). Background workers (long analytics queries, hold connection 30–90s each). Lambda functions (bursty, cold-start heavy, 0–200 concurrent). Math doesn't math.

- [ ] **A: PgBouncer transaction mode for everyone** — silently destroys the workers. Analytics query needs temp table → PgBouncer hands connection back to pool between transactions → next query gets different backend connection → state gone. Works in dev (low concurrency, same connection by luck), dies in prod.

> [!success] **B: PgBouncer session mode for workers + transaction mode for REST API** ✅ — transaction mode collapses API's 400 requested connections to ~30–50 actual backend connections. Session mode gives workers stable connections for temp tables, `SET LOCAL`, prepared statements, cursors that outlive a transaction. Lambda traffic goes through the API's transaction-mode pool (stateless, short-lived). One pooler instance, two pool configs, two listening ports. PgBouncer supports this natively.

- pgbouncer is pooler between client and postgres backend connections

```
   Client (worker)  →  PgBouncer  →  backend process #17:  CREATE TEMP TABLE results (...)
                                    COMMIT  → PgBouncer returns conn #17 to the pool

   Client (worker)  →  PgBouncer  →  backend process #42 (borrowed, was idle):  SELECT * FROM results
                                    → ERROR: relation "results" does not exist
```

- [ ] **C: RDS Proxy for Lambda + PgBouncer for ECS** — RDS Proxy is genuinely good for Lambda (cold-start connection storm, IAM auth, VPC integration). But doesn't fix the workers — still long-running, still need session state. Introduced second pooling product to operate, monitor, and pay for.
- [ ] **D: Read replica for analytics workers** — solves read scaling and noisy neighbor on query plans/cache/IO. Doesn't solve connection math. Replica has its own `max_connections` ceiling. Workers still hold connections for 30–90s. Moved the exhaustion problem from primary to replica, and now paying for extra RDS instance.

---

## Day 14: Safely Rolling Out a Risky Change ⭐

**Scenario:** Shipping a rewrite of checkout write path on Friday. ~3K RPS. Change touches the line that actually charges the card — old path uses Stripe Charges API, new path uses PaymentIntents with 3DS. QA green. Load test passed. But it's checkout — if this breaks, money breaks. Can't roll back a card that already got charged.

- [ ] **A: Blue/Green** — "instant cutover" is the problem. Flip the LB → 100% traffic hits new code, including Stripe webhooks confirming PaymentIntents created by old code. Cross-version race condition on real money. Rollback doesn't undo a charge.
- [ ] **B: Canary** — routes by request, not customer. A B2B billing job hits 1% canary 50 times in an hour. Bug on their card type? Charged 50 times before dashboards catch it. Payment failures surface as successful 200s with wrong amount — error-rate alarm never fires.
- [ ] **C: Rolling** — for 5–10 minutes, old and new tasks serve checkout simultaneously. "Create order" hits v1, "confirm payment" webhook 800ms later hits v2. Inconsistent state written by code never tested together.

> [!success] **D: Feature Flag** ✅ — deploy new code to 100% of ECS tasks behind a flag defaulting OFF. Flip for internal users → 1% of customers → 10% → 100%, with instant kill switch. Decouples deploy from release. Rollback is a config push, not a deploy (sub-second). Target who sees the new path — $0.99 and $40K B2B customers shouldn't get coin-flipped equally. Keep old code path warm for weeks.

- rolling/blue-green/canary are deployment strategies (how new code reaches machines)
- feature flags are a release strategy (how clients get new behavior)

---

## Day 15: Fast "Has the User Seen This?" Checks ⭐

**Scenario:** Content recommendation feed, 50M users. Every API call asks "has this user already seen post X?" `user_seen_posts` table: 80B rows. p99 latency = 600ms. ~120K RPS peak. False positives tolerable, false negatives survivable. Target: p99 < 100ms.

> [!success] **A: Bloom filter per user in Redis** ✅ — sub-millisecond "definitely not seen" check, fall through to Postgres only on hit. ~97% of feed checks are for unseen posts → Postgres never touched. Memory: 10K posts per user at 1% false-positive = 12 KB (vs 80 KB+ for Redis SET). At 50M users: Bloom = ~600 GB, SET = ~4 TB. Medium's "have you read this", Cassandra's SSTable short-circuit, Bitcoin's SPV wallets all use this.

- bloom filter mathematically produces **ZERO** false negative -> "definitely not seen" is always true

- [ ] **B: Redis SET per user** — same O(1) speed with perfect accuracy. Trap: memory explodes on power users. 50K posts seen = 3–4 MB per user. Top 5% blow up the Redis cluster. Rule: SET when cardinality <1K per key or false positives unacceptable. Bloom when cardinality large and "probably not" is good enough.
- [ ] **C: Move to Cassandra** — handles wide-column data fine. But problem isn't storage (Postgres with partitioning handles 80B rows) — it's read latency under load. Still doing point lookup per recommendation, now with multi-quarter migration.
- [ ] **D: Postgres read replica + pooler** — buys horsepower, not efficiency. Still hitting disk on every check, still B-tree lookup, still round-trip per request. You don't need more database — you need to not hit the database for the 97% where the answer is "no."

---

## Day 16: Taming a Hot Partition Key ⭐

**Scenario:** Multi-tenant analytics on DynamoDB. 200 tenants, 12K writes/sec total. One tenant onboards a massive customer overnight — their event volume 100x's. That one tenant hits 9K writes/sec on a single partition key. `ProvisionedThroughputExceeded` errors. P99 write latency: 8ms → 400ms. PK: `tenant_id`, SK: `event_timestamp`.

> [!success] **A: Write sharding** ✅ — append random suffix to PK: `tenant_id#0` through `tenant_id#9`. Hash function sees 10 different keys, distributes writes across 10 logical partitions (~900 WPS each). Read cost: scatter-gather across all 10 suffixes. This is literally the pattern AWS documents as the canonical fix for hot partitions.

- [ ] **B: Jitter the writes** — real pattern for thundering herd (N clients firing at same millisecond). But a hot partition is sustained 9K WPS, not a burst. Adding delay doesn't reduce the rate — DynamoDB still sees 9K WPS on same partition.
- [ ] **C: Partition splitting** — DynamoDB auto-splits based on throughput, not key cardinality. One PK value generating 9K WPS still hashes to same destination after split. Can't split a single key across two physical shards. Survives the design doc, dies in the war room.

- partition splitting helps when the heat is spread across a range of keys that happen to co-locate, not single key. DynamoDB splits a partition by its size limit/throughput

- [ ] **D: Time-bucket the key (`tenant_id#YYYY-MM-DD-HH`)** — at any given hour, still one partition key absorbing all 9K WPS for that tenant. Renamed the hot partition to a hot time bucket. Plus reads now have to query 24 different PKs for a day's data.

---

## Day 17: Backpressure on an Overwhelmed Consumer ⭐

**Scenario:** Kafka consumer processing 800 events/sec. Producer just hit 5,000 events/sec. Lag: 12 minutes behind and climbing. Consumer memory: 89%. JVM about to GC-thrash and OOM-kill. SLA: events must be processed, not silently dropped.

- [ ] **A: Drop events** — SLA says "must be processed, not dropped." Done.
- [ ] **B: Block the producer** — backpressure-as-blocking works in Reactor/RxJava/Akka because the protocol carries the signal. Kafka is pull-based and decoupled — producer doesn't know your consumer exists. No socket-level backpressure signal flowing upstream.
- [ ] **C: Buffer harder** — bigger in-memory queue delays the inevitable. 4,200 events behind per second × 1M-event buffer = ~4 minutes. Then back where you started with memory exhaustion. And the real bottleneck (external HTTP call) limits scaling anyway.

> [!success] **D: Rate-limit + load-shed** ✅ — cap consumer intake at ~1K/sec, route overflow to a durable secondary topic (`events.overflow`) with its own consumer group that drains during off-peak. Producer keeps producing. Primary consumer keeps steady heartbeat. Overflow gets processed later. Graceful degradation. Stripe and Shopify publish architecture posts on this exact pattern.

- consumer has 2 independent processes: fetch/process. rate-limit intake/a bounded queue throttles the fetch to match process (avoid queue filling too much -> OOM). Kafka doesn't have back-pressure to talk producers slow down.
- the excess stays in the topic as lag (Kafka keeps them on disk), is moved to `overflow` topic and processed during off-peak

```
   Kafka primary ──fetch (1,000/s, capped)──► [small bounded queue] ──process──► done ✅
                                               (flat, healthy)
           │
           └── excess (4,000/s) ──► events.overflow topic ──► drainer consumer (off-peak) ✅
```

---

## Day 18: Surviving a Cache Stampede ⭐

**Scenario:** Redis cache expired on a key that 8,000 users hit every second. All 8K req/sec now flying straight at Postgres (comfortable at ~200 req/sec). DB on its knees. Next TTL expiry in 60 seconds.

- [ ] **A: Mutex lock** — one request gets lock, rebuilds cache, everyone else waits. Under 8K req/sec, "waiting" means API threads blocked, request queue filling, p99 latency spiking to seconds. Traded DB overload for application-layer backup. DB survives; user experience dies.
- [ ] **B: Probabilistic early expiry (XFetch)** — clever math but probabilistic, not guaranteed. Under exact wrong timing (low traffic right before TTL, then sudden spike) key still expires cold. For 8K req/sec 24/7, want deterministic guarantee — not good odds.
- [ ] **C: Request coalescing** — elegant on a single server. On 50 Node.js instances behind LB, each instance coalesces independently → 50 concurrent DB queries instead of 8,000. Better, but still 50x spike at every TTL expiry. To coalesce across instances, need distributed coordination layer.

- request coalescing with shared cache
  - 1 request acquires lock to update cache, other requests are blocked
- CDN

```
  ### Exact Behavior: Cold Cache Miss (No Stale Data)

    Client 1 ──┐
    Client 2 ──┼──► CDN Edge ──► Holds 999 connections open (paused) ──► 1 Request to Origin
    ...        │		  │
    Client 1000┘		  │ (Origin responds in 200ms)
                                  ▼
               CDN caches response & writes data to all 1,000 clients simultaneously

- if request is timeout, all requests return 504 (not sending 2nd request)
```

> [!success] **D: Cache pre-warming** ✅ — background job (cron, Lambda, Sidekiq) rebuilds the cache key on a schedule shorter than TTL. Key never goes cold in production. No expiry cliff for 8,000 requests to fall off. Pair with stale-while-revalidate: serve stale while background refreshes. Netflix pre-warms content metadata. Twitter pre-builds timelines for high-follower accounts.

- use Stale-While-Revalidate (SWR) to replace cache with dual TTL (refresh + return old cache (soft-ttl)/new cache (hard-ttl))

---

## Day 19: Read-Your-Writes with Read Replicas ⭐

**Scenario:** Added read replica, P95 dropped from 400ms to 90ms. Two hours later: customers update shipping address but see old one on confirmation screen. "Order already exists" check read stale data and missed duplicate. Replication lag ~200ms.

> [!success] **A: Read-your-writes consistency** ✅ — after a user performs a write, route their subsequent reads to primary for a short window (a few seconds, or until replica lag catches up). Everyone else reads from replica. Performance win preserved for vast majority of traffic.

- [ ] **B: Synchronous replication** — primary waits for replica to confirm before ACKing write. Replica lag → zero, but write P95 goes from 20ms to 80–120ms. Coupled primary's availability to replica's health.
- [ ] **C: Monitor replica lag + retry** — average lag isn't the problem. The problem is a user reads their own write within 200ms of making it. Lag metric looks fine (200ms is "normal"), but the data the user needs is still in transit.
- [ ] **D: Route critical reads to primary** — "critical" is not a stable category. The primary-read list quietly shrinks, stale-read bugs come back, you spend the next quarter playing whack-a-mole. Traded a systematic solution for a per-feature judgment call.

---

## Day 20: Containing a Failing Downstream Dependency ⭐

**Scenario:** Checkout calls 3rd-party fraud-check API. API starts timing out at 30s instead of 200ms. Node.js pods have 50-connection pool. Within 90 seconds, every connection parked waiting on fraud API. P99 on `/checkout`: 300ms → 28s. Pods OOM. The fraud API is degraded — entire checkout is down.

- [ ] **A: Drop timeout to 2s + 3 retries with backoff** — canonical anti-pattern. Fraud API already struggling, you just decided to send it 3x the traffic. Every retry storm converges on a service that needs less load to recover. How a partial outage becomes a total outage.
- [ ] **B: Circuit Breaker alone** — most-mentioned resilience pattern. But between failure #1 and breaker tripping, every one of those N requests still holding connection from shared pool. Can saturate 50-connection pool before breaker notices. Reduced outage window, didn't eliminate cascade.
- [ ] **C: Bulkhead alone** — contains damage but your 10 dedicated fraud connections still spend 30 seconds each on doomed calls. Customers still see slow checkouts; just don't lose `/cart` with them. "The leak is contained, but the room is still flooding."

> [!success] **D: Circuit Breaker + Bulkhead together** ✅ — Circuit Breaker stops hammering dead dependency: after N consecutive failures, flips OPEN, every subsequent call fails instantly with fallback. After cooldown, HALF-OPEN with single probe request. Bulkhead isolates resource pools: fraud gets dedicated 10 connections, separate from 40 for `/cart`, `/orders`, `/health`. When fraud hangs, saturates its 10, others stay free. Ship doesn't sink because one compartment flooded. Netflix wrote Hystrix specifically for this.

- circuit breaker

```
  A state machine wrapped around an external call to prevent repeated doomed network requests:

                      ┌───────── Success (Reset failure count) ─────────┐
                      ▼                                                 │
              ┌──────────────┐     Failure rate > threshold     ┌──────────────┐
              │    CLOSED    │ ───────────────────────────────► │     OPEN     │
              │ (Pass calls) │                                  │ (Fail Fast)  │
              └──────────────┘                                  └──────────────┘
                      ▲                                                 │
       Success        │                                                 │ Sleep window expires
       (Reset)        │             ┌─────────────────┐                 │
                      └──────────── │    HALF-OPEN    │ ◄───────────────┘
                        Probe fails │  (1 Test Call)  │
                        ──────────► └─────────────────┘

  • CLOSED: Normal operation. Calls pass through.
  • OPEN: Triggered when failure/timeout rate exceeds threshold (e.g., >50% failures in 10s). The system fails fast immediately (0ms) without making the
  network call.
  • HALF-OPEN: After a cooldown window (e.g., 30s), lets one probe request through:
      • If probe succeeds → returns to CLOSED.
      • If probe fails → resets OPEN timer.
```

- bulkhead is resource pools isolation (1 dependency cannot consume all resources) -> limit the blast radius of a slow/failing dependency

---

## Day 21: Choosing a Real-Time Streaming Transport

**Scenario:** AI chat product. LLM streams ~40 tokens/sec per user. 50K concurrent users. Browser clients only. Tokens flow one way: server → user. Reconnects must be invisible (mobile networks drop constantly).

- [ ] **A: WebSockets** — "chat" tricks people. User-to-user chat is bidirectional; AI chat is unidirectional token stream with separate POST for prompt. At 50K connections: sticky sessions on ALB, hand-rolled reconnect + replay, heartbeats, higher per-connection memory. Every one becomes an on-call page.

> [!success] **B: Server-Sent Events (SSE)** ✅ — traffic is one-way. Server pushes tokens, client renders. One long-lived HTTP connection, `text/event-stream`, browser's native `EventSource` reads. No protocol upgrade, no new framing, no new auth path. Killer feature: automatic reconnect with `Last-Event-ID` — browser drops, reconnects on its own, tells server last event seen, replay from there. With WebSockets, you write that logic yourself and write it wrong the first three times. OpenAI's streaming API? SSE. Anthropic's streaming API? SSE.

- [ ] **C: gRPC streaming** — browsers don't speak gRPC. Need Envoy + gRPC-Web, which downgrades streaming model and adds proxy hop. Operating Envoy and debugging Protobuf frames to ship UTF-8 tokens.
- [ ] **D: Long polling** — at 40 tokens/sec, every poll cycle burns a full HTTP request. 50K users × 40 req/sec = 2M RPS just to render text. Valid fallback when SSE/WS blocked. Not primary transport in 2026.

---

## Day 22: Reliable Messaging Across Services ⭐

**Scenario:** PaymentService charged a customer. Needs to tell NotificationService: "Send confirmation email." HTTP call times out. Did it arrive? Don't know. Retry. Customer gets two emails. The Two Generals Problem — it's not a bug, it's a proof. No protocol over an unreliable channel can guarantee both sides agree.

- [ ] **A: Retry until ACK** — what if the 200 response is what timed out, not the request? NotificationService sent the email AND returned 200, but you never saw the response. Retry → second email. Now need to confirm your ACK arrived too... the Two Generals recursion. No finite number of retries closes this loop.
- [ ] **B: 2PC** — coordinator single point of failure. If it crashes between Phase 1 and Phase 2, both services stuck with locks held waiting for decision. Traded message uncertainty for coordinator-failure uncertainty — same problem, more complexity.
- [ ] **C: Outbox Pattern** — actually solid: atomicity at DB level, event and payment always in sync. But running relay process + CDC pipeline + outbox cleanup. For teams with SQS already in place, D gets 95% of same guarantees with fraction of infrastructure. C shines at scale or when strict ordering matters.

> [!success] **D: SQS + at-least-once + idempotency key** ✅ — the only answer that accepts the impossibility and designs around it. At-least-once means message will arrive — maybe twice. Idempotency on consumer side (`payment_id:email:v1` in dedup table) makes second delivery a no-op. No missed sends, no double-sends in practice. Exactly how Stripe and AWS handle it.

- at-most-once
  - message is delivered 0 or 1 time (fire and forget)
  - producer (no retry) -> broker -> consumer (ack) -> process
- at-least-once
  - message is delivered 1 or more times
  - producer (retry / outbox) -> broker (durable log) -> consumer -> process (ack)
- exactly-once (physically impossible) -> effectively once (at-least-once delivery + idempotent consumer)
  - producer writes business state change + event into same local DB transaction (transactional outbox)
  - broker-level deduplication
    - kafka: producerId + sequenceNumber

```

    [ Step 1: Producer ]          [ Step 2: Broker ]               [ Step 3: Consumer ]
     ┌─────────────────┐           ┌──────────────┐                 ┌──────────────────┐
     │  Transactional  │ ────────► │ Deduplication│ ──────────────► │ Atomic DB Trans  │
     │     Outbox      │           │    Window    │                 │ (State + Dedup)  │
     └─────────────────┘           └──────────────┘                 └──────────────────┘
                                                                             │ (If calling 3rd party)
                                                                             ▼
                                                                    [ Step 4: External API ]
                                                                    (Pass Idempotency-Key)
```

---

## Day 23: Feed Fanout for Celebrity Accounts ⭐

**Scenario:** Feed service reading at 20ms. Celebrity with 2M followers posted. Now 4 seconds. P99 on fire. 10M users, ~50K posts/day. One account: 2M followers. Feed query fans out across 2M follower rows, sorts by timestamp, buries read replicas.

- [ ] **A: Fanout on Write** — looks perfect. Reads instant. Until Cristiano Ronaldo posts and you're writing to 500M caches in parallel. At 2M followers, even 1ms per write = 2,000 seconds of write work. Cache cluster saturates. Works great at 1M users, then hits the celebrity problem already in production.

- fanout-on-write (push model/precomputed feed)
  - high write amplification (find followers and write to them)
  - read precomputed result

- [ ] **B: Fanout on Read** — 500 accounts followed = 500 queries, sorted in memory, before returning anything. Expensive computation to fill a cache that expires in 30s. Just a slow fanout-on-write with extra latency.

- fanout-on-read (pull model/dynamic feed)
  - write once (no write amplification)
  - slow read (queries across many tables/partions for aggregation) -> limit read scalability

> [!success] **C: Hybrid fanout** ✅ — fanout-on-write for regular users (<10K followers), fanout-on-read for celebrities (≥10K). At read time, fetch from two sources: precomputed cache (regular accounts) + real-time query for celebrity accounts. Merge + deduplicate. Celebrity slice is small and bounded. This is how Twitter actually solved it. (writes << reads -> optimize reads)

- [ ] **D: Materialized feed table** — denormalized row per user, updated async via CDC. But celebrity post still triggers 2M row updates, just asynchronously. Haven't solved write amplification, deferred it. Plus event stream + idempotent consumers + reconciliation logic.

---

## Day 24: Paginating Large Result Sets Efficiently ⭐

**Scenario:** 10M orders. Frontend asks for "page 5." Offset 40, limit 10. Query time: 4.2s. PostgreSQL, 50M rows in orders, sorted by `created_at DESC`, filterable by status. At 50M, offset pagination reads and discards 40M rows to return 10. SLA: p99 < 200ms.

> [!success] **A: Cursor pagination** ✅ — encode last seen `(created_at, id)` into opaque token. Next request decodes and uses `WHERE created_at < :last_ts OR (created_at = :last_ts AND id < :last_id)`. Query always hits index at anchor point — no scan, no discard. p99 flat from page 1 to page 50,000. Cursor is position-stable: new rows inserted before cursor don't shift your page. UX tradeoff: no jump-to-page, only prev/next. Right tradeoff for dashboard.

- [ ] **B: Keyset pagination** — looks identical to cursor on surface. Difference: keyset is a query pattern, cursor is a product decision. Status filter breaks row-tuple comparison in most query planners when equality column isn't part of tuple comparison. Partial index scan that degrades under high cardinality filters.
- [ ] **C: Deferred join** — legitimate optimization: inner query fetches only IDs (fits in index), outer join fetches full rows for just 10 records. Shopify uses a version of this. But: still pays O(offset) cost on inner query at deep pages. At page 50,000, still scanning 500K index entries. Shaved 80% of cost, kept 20% of problem.
- [ ] **D: Covering index** — good idea regardless of approach. But doesn't change algorithmic complexity of OFFSET. Makes table scans faster, not shorter. "Throw hardware at it" — buys time, not a solution.

---

## Day 25: Queue Backpressure Under a Traffic Spike

**Scenario:** SQS order processing. Normal: 200 orders/min. Black Friday: 4,000 orders/min. Queue depth: 80K messages in 20 min. Downstream DB at 95% CPU. Consumers falling behind.

- [ ] **A: Scale consumers horizontally** — instinct answer that treats a rate mismatch as a capacity problem. Producer can always generate faster than consumers can process — unbounded producer rate vs finite consumption. Spin up 10x Lambda, hit DynamoDB write limits, hammer RDS connection pool, queue still grows. Just slower and infra bill doubled.
- [ ] **B: Visibility timeout + DLQ** — failure handling, not backpressure. Catches poison pills and prevents double-processing. Neither slows the producer nor reduces queue depth growth.

> [!success] **C: Rate-limit producers at the source** ✅ — queue grows because producer is winning: 4,000 in, 200 out. Scale consumers all day and gap won't close with DB at 95% CPU. Fix is upstream: token bucket or sliding window on the emitter (not the user — user already has their ack from the write; throttle the event emitter that reads from DB and pushes to queue). Queue depth stabilizes, consumers catch up naturally. Mental model: slow the tap, don't just widen the drain.

- put rate-limit to the background event emitter/outbox relay by token bucket, congestion control (resource measures), polling batch window throttling

```
  ### Architecture Overview

    User Checkout ──► [ DB Transaction: Order + Outbox ] ──► Return HTTP 200 ✅
                                    │
                                    ▼
                       [ Outbox Poller / Emitter ]
                                    │
                       ◄─── [ Rate Limiter Guard ] ◄── (Feedback: DB CPU & SQS Depth)
                                    │ (Throttled: max 300 msg/sec)
                                    ▼
                           [ SQS Order Queue ]
                                    │
                                    ▼
    			 [ Downstream DB / Workers ] (Healthy at 60% CPU)
```

- [ ] **D: SQS delay queues** — defer message visibility, not creation. Producer still pushes 4K msg/min. Messages pile up invisibly, then become visible in bursts when delay expires. Like covering a flooding sink with a lid and calling it fixed.

---

## Day 26: Write-Path Cache Consistency ⭐

**Scenario:** NestJS API → PostgreSQL (source of truth) + Redis (cache). ~600 req/s reads, ~80 req/s writes. Current pattern: write to DB, manually invalidate cache key on success. 3 incidents this month — all stale cache after writes. Need strategy surviving race conditions, retries, partial failures.

- [ ] **A: Write-through** — looks safest. Is most dangerous at scale. Two synchronous I/Os on every write. If Redis is slow, write API is slow. If Redis is down, do you block the user? Made Redis a hard dependency of write path.
- [ ] **B: Write-behind** — fast but: if async worker crashes before DB flush, that write is gone. Acceptable for analytics counters. Never acceptable for source of truth.
- [ ] **C: Write-around** — solves stale cache by not writing to cache at all. Clean — but read-after-write broken under replica lag, and high-write workloads tank cache hit rate.

> [!success] **D: Dual-write with an outbox** ✅ — the core problem isn't "which order to write in" — it's "what happens when one write succeeds and the other fails?" One atomic DB transaction: record + outbox event. A consumer updates Redis from the event. If Redis goes down and comes back, re-process the outbox. Cache update is a consequence of the DB write, not a sibling operation.

- native dual write (write to DB then cache)
  - partial failure/crash
  - concurrent race conditions (out of order) due to network latency
- dual write with outbox
  - cache invalidation is subsequence of DB write (use outbox relay/CDC)
  - during propagation window, cache read is stale (eventual consistency)
  - race condition: permanent stale cache -> versioned cache writes

```

                               [ Local PostgreSQL Transaction (ACID) ]
    Application Write ──────► ┌───────────────────────────────────────────┐
                              │ 1. UPDATE products SET price = 99.00      │
                              │ 2. INSERT INTO outbox_table (product_123) │
                              └───────────────────────────────────────────┘
                                                    │ (Committed atomically)
                                                    ▼
                                        [ Outbox Relay / CDC Engine ]
                                                    │ (Guaranteed delivery + retries)
                                                    ▼
                                            [ Redis Invalidation ]
                                              DEL product:123
```

---

## Day 27: Keeping an LLM's Answers Up to Date

**Scenario:** Customer support bot on GPT-4. Trained through early 2024. Product changed 14 times since then. ~2K support queries/day, 15% return wrong answers tied to stale knowledge. Knowledge base updates weekly. Budget: mid-size startup, not training custom models.

> [!success] **A: RAG (Retrieval-Augmented Generation)** ✅ — embed knowledge base, retrieve relevant chunks at query time, inject into context. Model stays frozen (no retraining cost). Knowledge base lives in vector store — update a doc, re-embed it, done. New pricing ships Monday, bot knows by Monday. Turned a model problem into a data pipeline problem — every engineering team knows how to solve data pipelines.

- [ ] **B: Fine-tune the base model** — bakes knowledge into weights. Weekly product updates = weekly retraining at real cost + real risk of catastrophic forgetting. Fine-tuning teaches the model how to behave (tone, format, domain fluency), not what to know. Wrong tool for freshness.
- [ ] **C: Fine-tune + RAG hybrid** — genuinely powerful but step 3, not step 1. Can't productively fine-tune for style until factual grounding is solid. 3-month project when 2-week RAG fixes the actual problem.
- [ ] **D: Prompt engineering only** — fastest to ship, first to break. Cannot inject 400 pages of updated product docs without hitting token limits. Manually picking which docs to include is just RAG without the retrieval infrastructure.

---

## Day 28: Choosing a Vector Store for Semantic Search

**Scenario:** B2B SaaS semantic search. 4M support articles/docs/tickets. 1536-dimensional vectors (OpenAI ada-002). ~24GB raw embeddings. Query volume: 300 req/s, weekend spikes to 900 req/s. Sub-100ms p99 required.

- [ ] **A: pgvector** — great under ~500K vectors, often the right call since you already own PostgreSQL. At 4M rows and 300 req/s, HNSW index runs inside Postgres buffer pool competing with transactional workload. Latency goes non-linear under concurrency. VACUUM on large embeddings table is painful.
- [ ] **B: Pinecone** — works and teams ship fast. But cost model bites at 300 req/s sustained — thousands/month. Proprietary lock-in: no standard wire protocol, migrating means re-implementing ingestion pipeline from scratch. Right when speed to market > cost and query volume under ~50 req/s.
- [ ] **C: Weaviate** — solid hybrid search (BM25 + vector) and multi-modal support. Kubernetes footprint heavier than Qdrant for this use case. Shines for multi-modal search or semantic graph relationships; for pure dense vector with filtering, Qdrant leaner.

> [!success] **D: Qdrant** ✅ — purpose-built, Rust core = low latency and predictable memory under load. HNSW implementation tuned for high concurrency. Killer feature: payload filtering — users search within workspace/tenant/product line, not globally. Vector search + metadata filter in one pass. Every other option forces post-filtering which blows up recall. Self-hosted gives full control over HNSW params, memory mapping, on-disk indexing as corpus grows past RAM.

---

## Day 29: Coordinating a Multi-Agent Workflow

**Scenario:** 4 specialized AI agents: Planner, Researcher, Coder, Reviewer. Problems: Researcher sometimes returns before Planner finishes → Coder gets incomplete context. Reviewer flags issues but no retry loop. One agent timeout hangs entire pipeline 40s. No visibility into which agent failed.

- [ ] **A: Centralized orchestrator** — closest wrong answer. Sequential by default — Planner and Researcher run one after another unless you explicitly add parallelism. Hand-building a DAG imperatively, and badly. Every new dependency becomes a code change.
- [ ] **B: Choreography via event bus** — works for loosely coupled fire-and-forget. But pipeline has tight dependencies — Coder literally cannot start without both Planner AND Researcher. No natural "wait for these two" primitive. Choreography for independence, orchestration for dependency.

> [!success] **C: DAG-based execution** ✅ — model pipeline as directed acyclic graph. Planner and Researcher can run in parallel, Coder blocks until both complete. Retry loop: Reviewer → Coder as a first-class edge in the graph. Each node has its own deadline — one timeout doesn't freeze everything. DAG engines give full execution trace per run. Real implementations: LangGraph, Temporal, AWS Step Functions, Prefect, Dagster.

- [ ] **D: Supervisor pattern** — great layer on top of C for human escalation and anomaly detection. As base orchestration: adds latency (every decision through supervisor), single point of failure, doesn't solve the dependency problem. Supervisor still needs to know execution order — just an implicit DAG.

---

## Day 30: Choosing a File Storage Backend

**Scenario:** File upload service. 10TB today, 100TB in 12 months. Upload service (NestJS) receives files from mobile + web. ML pipeline reads uploaded images. Audit service needs read access. Files range 5KB profile pics to 2GB video exports. On AWS.

> [!success] **A: S3** ✅ — one storage layer, zero capacity planning. Every service reads from same bucket using S3 key stored in DB. At 100TB ≈ $2,300/month. Lifecycle policies move cold files to Glacier. S3 events trigger ML pipeline. Versioning, encryption, audit logs — all built in. For greenfield cloud services, this is the default. Deviate only with specific reason.

- [ ] **B: EBS** — a fast, reliable disk attached to one EC2 instance at a time. ML pipeline on different instance can't read those files. Auto-scaling = each new instance gets blank disk. Works perfectly in dev; silently breaks the moment you scale horizontally.
- [ ] **C: EFS** — shared NFS, multiple EC2 instances mount simultaneously, full POSIX semantics. But $0.30/GB/month = $30,000/month at 100TB vs S3's $2,300. 13x cost difference. Right when legacy app is hardcoded to `open()`/`read()`/`write()` and can't be refactored. Greenfield NestJS with S3 SDK? Paying 13x for filesystem semantics you don't need.
- [ ] **D: MinIO on EC2** — real product used at hyperscale. But self-hosted means you own availability, disk failures, backups, capacity planning, 3am incidents. At 10–100TB, engineering cost exceeds S3 spend. Makes sense at petabyte scale with dedicated infra teams and painful egress bills.

---

## Day 31: Cutting Cross-Region Latency ⭐

**Scenario:** E-commerce, 2M DAU. 70% US, 30% Europe. European latency: 380ms average to us-east-1. Support tickets up 40%. Black Friday in 6 weeks. Single AWS us-east-1, RDS PostgreSQL, Redis, 12 microservices. Target: <80ms for Europe. Cannot afford full DB rewrite.

- [ ] **A: Active-Active + distributed DB (CockroachDB/Aurora Global)** — "correct at scale" answer that kills teams before Black Friday. Migrating RDS Postgres to distributed DB under 6-week deadline is multi-quarter project. Right for long term; wrong for problem as stated.

> [!success] **B: Active-Passive with read replicas** ✅ — keep us-east-1 as primary, spin up eu-west-1 as hot standby with read replicas. European reads go local (~15ms instead of 380ms), writes still go to US (acceptable — users tolerate slightly higher write latency for checkout). Replication lag typically <100ms. 1–2 days infra work. Also gives real failover story: US down → promote EU replica in minutes. Constraint (6 weeks, no DB rewrite) is the answer.

- [ ] **C: CDN + Edge caching** — solves static asset latency (images, JS, CSS). Does nothing for dynamic reads (user cart, order history, account data) and zero for write latency. Layer you add on top of real solution, not instead of one.
- [ ] **D: Active-Active + eventual consistency** — most honest version of multi-region. Most dangerous to deploy without prep. European user places order, US region sees different inventory count for 200ms. Limited stock = oversell. Conflict resolution is product problem disguised as infra problem.

---

## Day 32: Managing Secrets and Credentials

**Scenario:** First SOC 2 audit. Half of secrets in `.env` files committed to git 18 months ago. Three hardcoded in Lambda env vars. One in Slack message from 2023. 6 services, 4 environments, zero rotation, zero audit trail, zero centralized access control.

> [!success] **A: AWS Secrets Manager** ✅ — already AWS-native. Centralized encrypted storage (KMS-backed), IAM-based access control per secret per service, native auto-rotation for RDS + custom Lambda rotators. Every access logged in CloudTrail → exactly what SOC 2 auditor wants. Migration zero-downtime: swap env vars for `getSecretValue()` calls. Cost: ~$0.40/secret/month → $8/month for 20 secrets.

- [ ] **B: HashiCorp Vault** — more powerful (dynamic secrets, per-request Postgres credentials expiring in 1h). But Vault is infrastructure you own and operate: Raft cluster (3+ nodes), storage backend, unsealing procedures, DR planning. If Vault goes down, services fail. Wins for multi-cloud, on-prem, dynamic secrets at scale, or dedicated infra team. AWS-native under 50 engineers → Secrets Manager first.
- [ ] **C: CI/CD injected env vars** — right for build-time and deploy-time secrets (Docker Hub creds, Terraform tokens). Wrong for runtime secrets that app needs at 3am (DB password, Stripe key for live webhook). Injected as env vars into ECS task defs — harder to rotate atomically, no audit trail on runtime access. Complements A or B; doesn't replace them.
- [ ] **D: DIY KMS + own database** — reinventing Secrets Manager badly. Now own: encryption key management, rotation logic, access control, audit logging, and a database that itself needs credentials. What protects the secret store? Bootstrapping problem managed secret stores specifically solve. What teams built in 2012 before managed options existed.

---

## Day 33: Reconstructing State with Event Sourcing ⭐

**Scenario:** Order service, 200 writes/sec peak. Audit finds two orders with same ID, different totals. Current state only — every UPDATE overwrites previous row. No audit log, no event history, no replay. Billing dispute: need to reconstruct exactly what happened to Order #8471. Can't.

> [!success] **A: Event Sourcing** ✅ — append-only event log as source of truth. Current state derived from replaying events (or from snapshot). Every mutation preserved, timestamped, immutable. Can reconstruct state at any point in time. Build new projections without changing core model — just replay and project differently. Axon, EventStoreDB, most serious fintech/e-commerce systems do this. It's not a log — it's the primary data model.

- [ ] **B: Change Data Capture (CDC)** — powerful with Debezium + Kafka. Looks like Event Sourcing from outside. But CDC captures state deltas, not business events. You get `total changed from 89.99 to 79.99` — not `DiscountApplied by coupon SAVE10`. Semantic meaning lost. Can reconstruct what changed, not why. Kills you during disputes and compliance audits.
- [ ] **C: Audit_log table (triggers)** — classic band-aid. Treating row as source of truth and logging changes as side effect. Side effects break: triggers disabled during migrations, bulk imports skip them, schema changes orphan the trigger. Six months later, audit_log has gaps — exactly when needed most.
- [ ] **D: Dual-write** — created distributed consistency problem inside own service. State write succeeds, events write fails → state with no corresponding event. Audit trail unreliable by design. If going this far with Outbox Pattern, already halfway to proper Event Sourcing.

---

## Day 34: Improving LLM Classification Accuracy

**Scenario:** SaaS, 50K support tickets/week. AI triage system classifies into 6 categories (billing, bug, feature request, account access, security, other). Dev accuracy: 71%. Need 90%+ to cut manual review. Model locked. Inference budget not unlimited. Close the 19-point gap.

- [ ] **A: Zero-shot with better system prompt** — accuracy ceiling: ~78–82%. Instructions describe categories but can't show where ambiguous cases land. "I can't log in and I was charged twice" — billing or account access? No amount of rewriting tells model which bucket. Ceiling is real.

> [!success] **B: Few-shot examples** ✅ — add 3–5 real classified tickets in prompt. Accuracy: 88–93%. Shifts model from reading rules to pattern-matching against real examples. Critical: pick the ambiguous ones — ticket that looks like billing but is account access, feature request reading like a bug. Those are where model fails and those examples close the gap. Crystal-clear examples teach nothing new.

- [ ] **C: Chain-of-Thought** — accuracy delta: ±2%, latency +200–400ms. Model generates reasoning chain then commits to label. On ambiguous tickets, chain becomes liability: "Mentions a charge... but also a login issue... charge is mentioned first... probably billing" — wrong. CoT helps when answer emerges from reasoning (math, debugging). For classification, answer emerges from calibration.
- [ ] **D: Self-Consistency** — accuracy 93–96% but 5x cost and latency. Run ticket 5x at temperature=0.7, majority vote. $500/week vs $100/week. Worth it when wrong is expensive (fraud detection, medical triage). For support routing where misclass costs ~$0.10 of human rerouting time — use B.

---

## Day 35: Geospatial "Find Nearby Drivers" at Scale ⭐

**Scenario:** Ride-hailing. 500K active drivers updating GPS every 5 seconds. ~100K proximity queries/sec. Naive lat/lng bounding box = full table scan at scale, 800ms latency.

- [ ] **A: Geohash** — production-grade but wrong here. Z-order curve doesn't guarantee geographic adjacency for adjacent prefix strings. Two drivers 1 meter apart straddling cell boundary → entirely different prefix strings. Systematic miss rate at 100K queries/sec. Right for coarse partitioning (sharding by region), wrong for real-time sub-km proximity.
- [ ] **B: PostGIS** — correct for 5K trucks on fleet dashboard. Not for 500K drivers updating every 5s = 100K writes/sec against GiST index. GiST indexes write-expensive, DB burns half capacity on index maintenance, can't scale Postgres writes horizontally.
- [ ] **C: Quadtree in memory** — O(log n) insert/query in theory. Breaks at ride-hailing density: driver crossing cell boundary = delete + reinsert + potential rebalancing, 100K times/sec. Same rectangular boundary problem as geohash. Building block, not complete solution at scale.

> [!success] **D: H3 Hexagonal Grid (Uber's system)** ✅ — divide earth into hexagonal cells at multiple resolutions. Hexagons have 6 equidistant neighbors (squares have corner neighbors ~40% farther — distorts "within 2km"). 16 resolution levels, no reindexing on zoom. Killer feature: k-ring query (target cell + 6 neighbors) guarantees no driver missed near boundary. Uber does sub-10ms lookups at millions of drivers. Lyft, Airbnb, DoorDash all use variants.

---

## Day 36: Choosing HTTP/3 vs HTTP/2 at the Edge

**Scenario:** API response 320ms → 95ms after CDN switch. Only difference: CDN started speaking HTTP/3 to clients. Mobile app on lossy connections (4G→5G transitions, flaky WiFi, Asia-Pacific routes). 800ms+ tail latency at p99.

- [ ] **A: HTTP/2 only** — multiplexing is genuine improvement but doesn't solve TCP HOL blocking. On lossy mobile connections, still at mercy of TCP retransmission window. Won't move p99.
- [ ] **B: HTTP/3 only (end-to-end)** — to origin introduces operational risk: enterprise firewalls and cloud LBs block/rate-limit UDP 443. Origin isn't bottleneck, last mile is. Fixing origin leg with QUIC doesn't help, adds complexity and breakage.
- [ ] **C: HTTP/2 end-to-end** — same problem as A. Done nothing about last mile. "Clean" doesn't show up in p99.

> [!success] **D: HTTP/3 to clients, HTTP/2 to origin** ✅ — problem is the last mile. HTTP/2 fixed HTTP/1.1's application-layer HOL blocking but TCP still has transport-layer HOL blocking — one lost packet stalls ALL streams. HTTP/3 on QUIC (UDP): each stream independent, dropped packet stalls only that stream. 0-RTT resumption shaves 1–2 round trips. Datacenter leg (CDN→origin) is stable, low-loss: HTTP/2 multiplexing mature and well-optimized without QUIC's CPU overhead. Exactly how Cloudflare, Fastly, Akamai operate.

---

## Day 37: Multi-Writer Conflicts in Collaborative Editing ⭐

**Scenario:** Two users edit same document at 9:03 AM. No locking, no coordination. Both changes hit server 300ms apart. One lands first, the other overwrites it. User A's work gone — no error, just silently lost.

- [ ] **A: Last-Write-Wins (LWW)** — highest timestamp takes record. Loser's change vanishes silently — no error, just gone. Cassandra defaults to this. Fine for append-only (metrics, event logs). For anything a human edited: silent data loss with timestamp attached.
- [ ] **B: Vector Clocks** — track causality per replica, detect conflicting versions, surface to application for resolution. Amazon Dynamo used this. Correct and transparent. Problem: conflict resolution is now your job. Vector clocks tell you where conflicts are; they don't tell you how to fix them.

- vector clock = vector of node counter. it only detects conflicts, cannot resolves them -> user intervention

> [!success] **C: CRDTs (Conflict-free Replicated Data Types)** ✅ — data structures designed so any two replicas always merge mathematically without coordination. Operations are commutative, associative, idempotent. G-Counter: only increments, merge = take max. RGA/YATA (sequence CRDTs): each character gets unique ID, concurrent inserts deterministically ordered — collaborative text editing. Figma's canvas runs on CRDTs. Notion's block model is CRDT-based. Millions of concurrent writers across distributed regions converge independently — zero coordination.

- [ ] **D: Operational Transformation (OT)** — Google Docs' original approach. Transform each operation relative to concurrent ones before applying. Magical when it works. Operationally brutal: transformation functions notoriously hard to get right (original papers had bugs), every new operation type adds transformation pairs growing quadratically, requires centralized server to sequence. Modern Google Docs moved toward CRDT-like hybrid.

---

## Day 38: Fitting a Large Document into an LLM

**Scenario:** LLM has 128K tokens. Document has 150K words. Something has to give.

> [!success] **A: Chunk + embed + RAG** ✅ — split into overlapping chunks (~500 tokens, 10–20% overlap), embed each, store in vector DB, retrieve top-K at query time. LLM context only sees retrieved chunks — staying well inside window. Latency low (fast ANN lookup). Production fix: chunk at sentence/paragraph boundaries, not character counts. Hybrid retrieval (keyword + semantic) handles edge cases where chunk boundaries destroy semantic coherence.

- [ ] **B: Sliding window** — process in overlapping passes, accumulate answer. Doesn't fix context window problem — still process every chunk sequentially. Answer spanning chunk 1 and chunk 47 gets lost. O(n) LLM calls per query. Minutes per query at 150K words. Fine for summarization; wrong for retrieval.
- [ ] **C: Progressive summarization** — map-reduce: summarize sections, then summarize summaries. Works for high-level understanding. For answering specific question about clause 38(b) on page 97 — intermediate summary compressed away the specific detail. Lossy compression applied to information retrieval is category error.
- [ ] **D: Truncate to most recent tokens** — default behavior of most LLM wrappers when exceeding context limit. Beyond obvious data loss: LLMs have "lost in the middle" failure mode — performance highest at start/end of context, degrades significantly when answer buried in middle. Truncation compounds this unpredictably.

---

## Day 39: Preventing Concurrent Balance Overspend ⭐

**Scenario:** Two users try to spend from same wallet balance at same time. Both read $200. Both want to spend $150. Both see enough balance. Both write deduction. Wallet now -$100.

- [ ] **A: Pessimistic locking (`SELECT FOR UPDATE`)** — works and correct. Holds row-level lock for entire transaction. At 10K TPS on popular wallet, serialized all writes to single queue. Throughput collapses. Lock wait timeouts cascade. Use for low-concurrency paths (admin ops, batch jobs); not high-throughput payment writes.

> [!success] **B: Optimistic locking** ✅ — read wallet row with version number. Write with `WHERE version = :read_version`. If another transaction already updated, WHERE matches zero rows → conflict detected → retry. `UPDATE wallets SET balance = balance - 150, version = version + 1 WHERE id = :wallet_id AND version = :read_version`. No locks held during read. At 10K TPS with low conflict rates, significantly faster — only pay retry on actual conflicts. Catch: under HIGH contention (same hot wallet), retry storms eat you alive — need Redis `INCRBY` with atomic decrement or queue.

- [ ] **C: MVCC + default isolation (READ COMMITTED)** — dangerous. PostgreSQL defaults to READ COMMITTED — MVCC gives consistent snapshot but refreshes per statement, not per transaction. Both transactions read $200, both pass check, both commit. No conflict detected. MVCC prevents dirty reads; does NOT prevent lost updates at READ COMMITTED.
- [ ] **D: SERIALIZABLE isolation** — theoretically correct. PostgreSQL SSI tracks read-write dependencies. Under high concurrency, serialization failures spike — transactions abort and retry even without actual conflict. Real throughput penalty. Right for complex financial workflows where correctness > throughput. Wrong default for high-throughput per-transaction API.

---

## Day 40: Offloading Heavy Work Off the Main Thread

**Scenario:** React dashboard freezes 4 seconds on CSV upload. 80MB CSV (200K rows, 40 columns). `Papa.parse` on main thread = 3.8s synchronous JS. Scroll dies, spinner stops spinning, input lag infinite. INP score red. Lighthouse screaming.

- [ ] **A: `requestIdleCallback` + time-slicing** — keeps UI technically responsive but stretches parse from 3.8s to ~6s wall-clock. Idle callbacks deprioritized — under load, don't fire at all. React 18 concurrent rendering uses time-slicing for rendering, not blocking IO-shaped work.

> [!success] **B: Web Worker** ✅ — separate OS-level thread with its own event loop. Ship file via `postMessage` with Transferable (zero-copy), parse over there, send back parsed rows. Main thread stays at 60fps. INP drops from 3800ms to ~80ms. What Figma does for rendering, Google Sheets for formula recalc, Excalidraw for scene processing, VS Code Web for syntax highlighting. Boring, correct, ten-year-old answer.

- [ ] **C: `SharedArrayBuffer` + Atomics** — requires COOP + COEP headers site-wide, breaks Stripe Elements, YouTube embeds, Intercom, half your analytics scripts. Single 80MB CSV parse is embarrassingly serializable — splitting across 4 cores saves ~2s while costing weeks of cross-origin isolation hell. Right for real-time audio/video processing or shared simulation state.
- [ ] **D: Compile parser to WebAssembly** — makes parser faster, doesn't move it off main thread. WASM parser running synchronously still freezes UI — just for 1.2s instead of 3.8s. Would still need to put it inside worker. D is an optimization inside B, not an answer.

---

## Day 41: Moving from Batch to Real-Time Streaming

**Scenario:** New SLA: surface fraud signals within 500ms of transaction. Currently nightly Spark batch jobs. 8K events/sec peak. On AWS. Fraud model in Python. Output feeds DynamoDB that API reads from.

- [ ] **A: Kafka Streams** — event-by-event too, sub-10ms. Constraint: runs inside JVM. Fraud model is Python → separate service, adding network hop. Flink handles that boundary more cleanly with PyFlink. Right when fraud logic is stateful JVM-native aggregation; wrong default when model is Python.

> [!success] **B: Apache Flink** ✅ — true streaming engine, event-by-event, not batch. Every transaction triggers processing the moment it arrives. Latency: sub-50ms end-to-end. Exactly-once semantics mean fraud signals not double-counted when node fails. Watermark model handles out-of-order events cleanly (distributed payment processors with clock skew). Python fraud model integrates via PyFlink or sidecar. Operational overhead real but SLA demands it — 500ms + 8K events/sec is exactly what Flink was built for.

- [ ] **C: Spark Structured Streaming** — micro-batch under the hood. Collects events for trigger interval (100ms–5s under load), processes as mini-batch. Will pass staging, breach SLA at peak traffic. "Streaming" in name ≠ event-by-event processing.
- [ ] **D: Batch, 1-minute windows** — minimum latency = window size. At 60 seconds, 120x over SLA before first line of fraud logic runs. "Near real-time" is not an SLA.

---

## Day 42: Designing Memory for an AI Agent

**Scenario:** Agent remembered user's name, then forgot what it was doing. Multi-step booking task: find cheapest flight to NYC, search hotels under $150/night, compare total trip cost. By step 3, agent calls LLM with 8K tokens of raw conversation history and answers as if turn 1.

- [ ] **A: In-context window only** — collapses at ~15 turns or 8K tokens. Works for demos, fails in production multi-step tasks. "Just increase context length" ignores cost and lost-in-the-middle problem.
- [ ] **B: Vector memory store** — semantic similarity ≠ task relevance. In multi-step booking, embedding "find hotels under $150" might retrieve memory from different user session or past conversation about different city. Great for knowledge retrieval; unreliable for procedural task state.

> [!success] **C: Episodic memory with summarization** ✅ — keep last N turns in context (short-term), compress older turns into structured event summaries (episodic), inject only relevant summaries per new request. More engineering upfront — only pattern that degrades gracefully at scale. How Anthropic, LangChain Memory v2, OpenAI Assistants API all converge.

- [ ] **D: Redis session state** — solid and deterministic. Catch: agent must explicitly decide what to write and when to read. Non-trivial design problem — building working memory protocol on top of tool calls. Most teams underestimate schema design this requires.

---

## Day 43: Reliable CDN Cache Invalidation on Deploy

**Scenario:** Edge nodes still serving old JS bundle — TTL hadn't expired. Triggered cache purge manually but hit wrong environment. Prod served stale version for 6 more hours.

> [!success] **A: Anycast + stale-while-revalidate + event-driven purge via API** ✅ — Anycast advertises same IP from multiple PoPs, BGP routes each user to closest edge. Stale-while-revalidate: serve cached version immediately, fetch fresh in background. Event-driven purge: CI/CD fires Cloudflare/CloudFront API call on every deploy targeting exactly changed assets. No manual steps, no wrong-env clicks, no 2am mistakes.

- [ ] **B: Unicast + aggressive TTLs + manual purge** — Unicast means one edge region, Tokyo users routing to Virginia. Deployed CDN and routing past it. Manual dashboard purges during deploy: someone will forget or click wrong environment. Aggressive TTLs shrink damage window, don't make invalidation reliable.
- [ ] **C: Anycast + long TTLs + tag-based invalidation** — tag-based (Cloudflare Cache-Tag, Fastly surrogate keys) lets you purge logical groups in one API call. Clean and surgical. Trap: long TTLs work when deploy pipeline robust, but if invalidation API call fails silently during incident, serving wrong version for hours with no TTL fallback.
- [ ] **D: Short TTLs, no invalidation** — "short TTLs = always fresh" is most expensive misconception. Every TTL expiry is potential cache stampede. 200K RPS peak, TTL expires on hot endpoint, every PoP fires simultaneous request to origin. Zero to 200K RPS in 2 seconds. Zero control for hotfixes.

- CDN
	- unicast: 1 IP -> 1 location
	- anycast: 1 IP -> many locations (edge PoPs). use BGP (border gateway protocol) for single IP

---

## Day 44: Syncing Offline Edits Without Data Loss ⭐

**Scenario:** Field-service app offline mode. Technician in Munich finishes repair offline, syncs when she gets signal — updates gone, overwritten by colleague who edited same record online 12 minutes earlier. Last-write-wins. Another technician: app throws unhandled promise rejection and crashes — IndexedDB schema v2, update shipped v3, migration never ran offline. 400 technicians, avg offline 40 min, ~3 write conflicts/day on 8 hot assets.

- [ ] **A: localStorage + JSON diff** — hard-capped ~5MB, no indexing, no range queries, wipes in private/incognito. JSON diff breaks on nested arrays, partial field updates, deletions. End up building mini-CRDT by hand without guarantees. Works in weekend prototype; corrupts silently in production.
- [ ] **B: Vector Clocks + Merge UI** — detect exactly when/where conflict occurred, surface merge UI. Right when humans must stay in loop (technician marking "inspected" vs "needs repair" — not something algorithm should auto-resolve). 3/day manageable. 300/day = support nightmare.
- [ ] **C: Versioned IndexedDB + LWW** — Dexie.js makes migrations manageable. LWW with deterministic composite key (`updated_at + device_id`) is production-grade. But LWW throws away real writes. Munich technician always loses to anyone who touched record online. When every write has operational meaning, that's unacceptable.

> [!success] **D: CRDT-based sync engine (Automerge/Yjs)** ✅ — operations are commutative, associative, idempotent. Two technicians edit same asset offline for 6 hours, sync in any order — final state always deterministic. No merge UI, no "who wins," no data loss. Linear uses Automerge, Figma custom CRDT, Notion similar model for block store. Tradeoff: CRDT payloads larger (carry operation history), server-side merge logic must understand CRDT ops.

---

## Day 45: Scaling Full-Text Search ⭐

**Scenario:** Search box returns 80ms. Added 50M more documents. Now 4 seconds. 100M documents. Search fields: title, description, tags, partial phrases. Current: PostgreSQL full-text. p95 = 4.2s. Target: sub-200ms p99.

> [!success] **A: Migrate to Elasticsearch** ✅ — inverted index: tokenizes text into posting lists ("database" → [doc_1, doc_5...]). Query does fast posting-list intersection, not table scan. At 100M docs: Lucene segments immutable (no row locking), horizontal sharding native (queries fan out parallel), BM25 scoring runs during retrieval. Sub-100ms p99 with proper shard sizing. Netflix, Uber, GitHub all run this. Tradeoffs: new infra to operate, write amplification from segment merging, eventual consistency (~1s).

- [ ] **B: GIN indexes on PostgreSQL tsvector** — genuinely good for 1–5M docs. At 100M: index balloons (40–80GB), no native horizontal read scaling, BM25 bolted on not native. Gets 4.2s → maybe 500ms. Need 200ms. What you reach for before dedicated search engine, not instead of.
- [ ] **C: Cache top 1,000 queries in Redis** — real optimization but not search architecture. Top queries cover maybe 40% of traffic. Other 60% hits slow path. Every document update invalidates cache logic. P99 problem still there the moment any user types something not in cache.
- [ ] **D: Typesense / Meilisearch** — excellent for 10–30M docs: simpler ops, great DX, built-in typo tolerance. At 100M with strict p99 and complex relevance tuning: distributed indexing less mature, scoring customization constrained, ops tooling thinner. For smaller product, D is right call.

---

## Day 46: Enforcing Structured Output from an LLM

**Scenario:** Production LLM agent returns: `{"action": "refund", "amount": "fifty dollars", "order_id": null, "confidence": "pretty high"}`. Downstream service crashes. Retry hits same model, same broken output. Refund never fires but user got confirmation email.

- [ ] **A: Prompt-engineer harder** — "Always return valid JSON" is a suggestion, not a contract. LLMs are probabilistic. 97% valid JSON, 3% markdown code block. At 100K req/day = 3,000 failures. Teams end up with 50-line system prompts enumerating every failure mode — model still escapes.

> [!success] **B: Structured outputs / function calling (API-level schema enforcement)** ✅ — OpenAI `response_format: { type: "json_schema" }`, Bedrock tool use, Gemini `response_schema`. Model's token sampling constrained — cannot produce output violating schema. Under the hood: constrained decoding masks invalid tokens at each step. Not "less likely" — mathematically cannot. Guaranteed schema conformance every call. Use Pydantic/Zod to define schema, pass to API, deserialize directly into typed model.

- [ ] **C: Post-process + retry loop** — legitimate when can't use structured outputs (open-source models via Ollama/vLLM). Parse → validate with Pydantic → on failure, re-inject corrective context → retry max 2 → fail hard. But: every retry is latency + cost. Corrective context doesn't help when model fundamentally can't produce what's asked. Use when B isn't available; use B when it is.
- [ ] **D: LLM-as-judge for validation** — real for offline eval (scoring quality, tone, safety). In hot path: expensive, slow (~200–500ms extra), unreliable for schema enforcement. Judge can say "this seems wrong" — cannot guarantee valid typed object. Belongs in eval harness (nightly runs, CI), not request/response loop.

---

## Day 47: Incrementally Strangling a Monolith ⭐

**Scenario:** 6-year-old monolith, 500K lines, deploy every 3 weeks, one bad migration takes down everything. 40 engineers, 3 teams deploying to same codebase. Returns processing is bottleneck — extract it first. Can't freeze feature work.

> [!success] **A: Strangler Fig** ✅ — introduce routing proxy in front of monolith. `/returns` traffic routes to new service. Monolith handles everything else. Run both in parallel — no freeze, no big-bang. Migrate one endpoint at a time, each step independently rollback-able. Only deprecate monolith code after new service proven under real load. Netflix and Amazon run versions of this at scale.

- [ ] **B: Branch by Abstraction** — real pattern but lives inside codebase. Wrap logic behind interface, build new implementation behind flag, flip when ready. Refactoring tool, not deployment strategy. Often used inside Strangler Fig to prepare internal structure. On its own doesn't get you to independently deployed service.
- [ ] **C: Big Bang Rewrite** — monolith doesn't freeze while you rebuild. Business keeps shipping features. Parallel rewrite immediately diverges. "Done" keeps moving. Cutover is single high-stakes event with no incremental validation. Joel Spolsky: "single worst strategic mistake."
- [ ] **D: Database-First Migration** — extract DB tables first sounds logical but breaks monolith's ORM immediately. Created distributed data problem before building distributed system to handle it. Data migration is last step — extract service logic first, keep data co-located temporarily, then migrate with dual-write.

---

## Day 48: How an Agent Chooses Which Tools to Call

**Scenario:** "Book me a flight to Dubai next Friday." LLM has 12 tools: `search_flights`, `get_user_preferences`, `check_calendar`, `book_flight`, `send_confirmation`, `get_weather`... How does agent decide which tools, what order, when to stop?

> [!success] **A: ReAct loop (Reason + Act)** ✅ — dominant production pattern. Model emits "Thought:" explaining what it's doing, then "Action:" with single tool call, observes result before deciding next. Each step observable and debuggable. Model can bail out, retry, change direction after each tool result. Works with tools that have side effects — gate dangerous calls. Supported natively by OpenAI, Anthropic, LangChain, LlamaIndex. Trap: sequential by default. If `get_user_preferences` + `check_calendar` + `search_flights` are independent, making 3 round trips when 1 would do.

- [ ] **B: Parallel tool calling** — modern LLMs can emit multiple tool calls in one response. If tools independent — massive latency win. Trap: not all tools are independent. If Tool B needs Tool A's output, parallel calling breaks. Production pattern: parallel for fan-out phase, ReAct for sequential decision phase.
- [ ] **C: Forced function schema** — looks like control, actually limits. Model loses ability to reason before calling. Breaks when user intent ambiguous or tool fails and needs retry decision. Use schema enforcement for output validation, not tool dispatch.
- [ ] **D: Planner-executor split** — architecture behind Devin, AutoGPT-style. Planner builds DAG upfront, executor runs it, planner re-engages at checkpoints. Parallelism by default, cost-efficient. Trap: planner must get full plan right before execution. World changes mid-run → need replanning. Most teams reach for this too early. Start with ReAct, add parallel when latency hurts, build planner-executor only with 10+ tools and real parallelism.

---

## Day 49: Controlling Data-Warehouse Query Costs

**Scenario:** $4,200 BigQuery bill. Single month, one analyst, 12 queries. Every query scanned full 3.2 TB table — no partition pruning, no cost control. Analysts always filter on date range ("last 30 days") and customer_id ("for customer X").

- [ ] **A: Date partition only** — real improvement, bill drops 60–70%. But inside each date partition, all customer rows interleaved. Still scanning every customer inside that window — ~500 GB. A is obvious first step; D is A taken all the way.
- [ ] **B: Customer_id range partitioning** — smart engineers pick this. But customer_id distributions never uniform. Enterprise clients (IDs 1-10,000) generate 80% of events. Every query against active customers hits same partition — no pruning benefit. Full-partition scan on hottest partition. Same cost, different framing.
- [ ] **C: DISTKEY + SORTKEY, no partitioning** — real optimizations for join/distribution, but neither replaces partition pruning at 3.2 TB. Without partitioning, every query triggers full table scan. DISTKEY skewed when enterprise customers dominate — one node holds 60-70% of data, every expensive query hammers it.

> [!success] **D: Partition by ingestion date + cluster on customer_id** ✅ — date pruning eliminates ~94% of table before scanning a single row ("last 30 days" on 18 months). Clustering sorts rows by customer_id within each partition into storage blocks — filter skips 90–95% of remaining rows. Combined: 3.2 TB → ~12 GB. Bill: $4,200 → ~$70/month. Works across BigQuery (partition + cluster), Snowflake (micro-partitioning + cluster keys), Redshift (partition key + SORTKEY compound).

---

## Day 50: Serving ML Models at High Throughput ⭐

**Scenario:** PyTorch model, ~6B params, single A100 GPU (80GB VRAM). 3K inference requests/sec. P99 latency: 4.2s. GPU utilization: 23%. FastAPI calling `model.predict()` one request at a time. No batching, FP32. GPU starving — not overloaded.

> [!success] **A: Dynamic batching** ✅ — GPU utilization at 23% tells you GPU is starving. Every request arriving one at a time, paying full GPU kernel launch overhead, then idling. GPUs built for parallelism — want 256 inputs simultaneously, not 1. Buffer requests for ~50ms, collect 32–128, fire single forward pass. Utilization jumps to 85–90%. Latency improves because batch throughput dramatically outpaces sequential calls even with small buffer wait. Exactly how NVIDIA Triton, TorchServe, vLLM work by default.

- [ ] **B: INT8 Quantization** — legitimate, valuable. Reduces model size ~4x, speeds up individual forward passes. But model fits comfortably in 80GB VRAM and GPU isn't saturated. Speedup modest (1.5–2x) — still sequential execution. Right order: batch first, quantize second (for memory or cost, not latency emergencies).
- [ ] **C: Tensor parallelism** — splits model layers across multiple GPUs via NVLink. Reduces per-request latency for very large models or sub-100ms requirement. 6B param on 80GB A100 fits. Adds coordination overhead. Need 2+ GPUs — inflating cost before trying the cheap fix.
- [ ] **D: Async queue + workers** — decouples HTTP from inference, prevents timeouts. But doesn't improve GPU utilization or throughput. Still processing one at a time, just asynchronously. Users get job IDs instead of timeouts but wall-clock wait same or worse. Adding a lobby to a slow restaurant — hides congestion, doesn't fix it.

---

## Day 51: Isolating Noisy Tenants in Multi-Tenant SaaS ⭐

**Scenario:** B2B SaaS, 50 enterprise customers. One DB, one schema, `tenant_id` on every table. Free-tier customer running badly-written bulk export hammered DB for 40 seconds. Paying enterprise customer's checkout flow timed out.

- [ ] **A: Row-level security + query budgets** — works but share same DB process. Tenant opening 500 connections, triggering table lock, or filling WAL bleeds into everyone. Can throttle CPU, can't throttle I/O blast radius once in buffer pool. Fine at 5 tenants; falls apart at 50.
- [ ] **B: Schema-per-tenant** — 300 tenants need migration = 300 sequential DDL operations. Migration windows become multi-hour risk event. At 500 tenants burning connection slots faster than PgBounce can handle. One long-running query still holds locks on shared system tables — noisy neighbor hasn't gone away, just can't see it as clearly.
- [ ] **C: Full silo for all tenants** — correct isolation for enterprise. Applying to free tier with 1,000 accounts = 1,000 Postgres instances, $40K/month RDS. Right endgame for top 5% of customer base; everywhere is overengineering.

> [!success] **D: Middleware bridge (hybrid model)** ✅ — pattern Salesforce, HubSpot, every mature B2B SaaS converges on. Free/small → shared pool DB. Mid-tier → schema-per-tenant in shared Postgres cluster. Enterprise → dedicated DB cluster (full isolation, SLA-able). Tenant registry (Redis or lightweight service) maps `tenant_id → connection config`. App server doesn't care which model — asks registry, gets connection string. Noisy neighbor contained. Enterprise can't touch each other. Migrate tenants up isolation ladder as they grow without touching app code. GDPR deletion = one DB drop for enterprise.

---

## Day 52: Versioning an API Without Breaking Clients

**Scenario:** `/users` now returns `fullName` instead of `first_name` + `last_name`. 3 mobile clients broke. 1 partner integration went down.

- [ ] **A: URL path versioning (`/v1/users`, `/v2/users`)** — pragmatic default used by Stripe, Twilio, GitHub. Not theoretically pure but operationally obvious — every proxy/log/CDN understands without configuration. Cost: running parallel route trees, v1 maintenance debt compounds. Stripe pins clients to version at API key level and deprecates slowly over years.
- [ ] **B: Header versioning (`API-Version: 2`)** — clean architecture: URL represents resource, header represents negotiation. Works for internal microservices when you control both ends. Problem: invisible in browser tabs, impossible to share as curl without flags, "default to latest" on missing header is footgun. Legacy client drops header, server defaults to v2, client breaks — not in URL, not in logs unless instrumented.
- [ ] **C: Query param versioning (`/users?version=2`)** — fast to implement, zero client SDK changes. Cache-unfriendly: every CDN layer treats `?version=1` and `?version=2` as separate cache keys, hit rate tanks. Bigger problem: version drift with no forcing function — clients scatter across v1/v2/v3 with no deprecation pressure.

> [!success] **D: Content negotiation (`Accept: application/vnd.api.v2+json`)** ✅ — semantically correct per HTTP spec: asking for specific representation of resource, not different route. In practice: Accept header parsing inconsistent across client libraries, middleware strips headers silently, misconfigured client gets 406 with no obvious error pointing to version field. GitHub tried early and moved to URL versioning. Correct spec, wrong reality.

---

## Day 53: Zero-Downtime Schema Migrations ⭐

**Scenario:** PostgreSQL, `users` table, 40M rows, active writes from 8 services. Need to split `full_name` into `first_name` + `last_name`. 2-hour maintenance window.

- [ ] **A: `ALTER TABLE` during maintenance window** — acquires ACCESS EXCLUSIVE lock, blocks every read/write for duration. On 40M row table with active traffic, lock holds for minutes. 8 services timeout, queue backs up, alerts fire. Maintenance window doesn't save you — the lock is the problem, not the timing.

> [!success] **B: Expand then contract** ✅ — Phase 1 (Expand): add `first_name` + `last_name` as nullable columns (PostgreSQL adding nullable column with no default is metadata-only — near-instant, no lock). Backfill in small batches (rate-limited, no row lock escalation). Update services to write to both columns. Phase 2 (Contract): once every service writing to new columns and reads fully migrated, drop `full_name`. Every step independently reversible. If something breaks after Phase 1, stop — old column still exists, old services still work. Slower than A? Yes. 3am pages? Zero.

- [ ] **C: Create `users_v2` + dual-write + flip read pointer** — works but for a column split on single table? 3 weeks of engineering for 3-day problem. Worth it for structural rewrites (new PK, re-partitioning, changing storage engines).
- [ ] **D: DB view aliasing** — buys time, useful as transition layer inside B. PostgreSQL write-through views only work on simple single-table views. Still need to backfill real columns eventually. Defers migration, doesn't replace it.

---

## Day 54: Handling Embedding Drift in RAG

**Scenario:** RAG pipeline worked in dev. 6 months later: "search results are garbage." Product evolved — new features, docs, tickets. Data drifted but embedding index didn't. 400GB FAISS index last rebuilt in January. 50M chunks. Full rebuild = 4 hours + ~$800 embedding API cost. Model updates every 6 weeks.

- [ ] **A: Scheduled full rebuild** — $800 every Sunday whether needed or not. At 6-week model updates, most rebuilds wasted spend on data that hasn't meaningfully changed. Works at 1M chunks; painful at 50M.
- [ ] **B: Incremental upserts + soft delete** — only re-embedding what changed. Silent killer: model drift. Index has vectors from 4 different model versions. Nearest neighbor across mixed-space returns garbage — not because data stale, because geometry inconsistent. Handles data drift; doesn't handle model drift.

> [!success] **C: Embedding version registry + hot swap** ✅ — track which embedding model version produced each vector. When model changes, invalidate mismatched vectors and rebuild only those. Two indexes run in parallel during migration. Route traffic by model version. Only solution handling the real problem: embedding model changed (fine-tuned or upgraded). Options A and B still serve mixed index — vectors from model v1 and v2 in different embedding spaces, cosine similarity breaks. Migrate 10% of traffic to new index, validate retrieval quality, then cut over.

- [ ] **D: Approximate staleness detection** — nightly sample 1% of corpus, re-embed, measure cosine distance against stored vector. If drift exceeds threshold, trigger rebuild. Useful monitoring signal, but tells you that you have drift, not which vectors or why. Trigger, not architecture. Combine with C for complete system.

---

## Day 55: Parallel Agents with Shared State

**Scenario:** Research agent system. Fan out to 3 specialized sub-agents simultaneously, one might spawn 2 more based on findings, all write back to shared context, final agent synthesizes.

> [!success] **A: Centralized Orchestrator** ✅ — one controller agent dispatches tasks, collects results, manages shared state. Sub-agents are stateless and dumb on purpose — receive task, return result, done. When something fails, know exactly where to look: orchestrator holds retry logic, timeout budgets, fallback paths. Sub-agents can die and restart without corrupting global state. LangGraph, CrewAI, every production agentic framework defaults to this. Debuggable, observable, deterministic — can replay orchestrator run from state log.

- [ ] **B: Decentralized Peer Handoff** — elegant in theory. Who resolves conflicts? Agent A hands to B, B decides task belongs to C, C hands back to A — cycle with no circuit breaker. Works in closed, well-defined pipelines (Git commit hook chain). Breaks with conditional routing, error recovery, parallel fan-out.
- [ ] **C: Shared Message Queue + Blackboard** — real and useful as data layer, not coordination mechanism. Agents reading/writing shared state works for passing context. Can't cleanly orchestrate who runs next, when, with what inputs. End up building implicit orchestrator via polling — same thing, no visibility.
- [ ] **D: Hierarchical Nesting** — right when problem hierarchically decomposable ("summarize AI papers" fans out to 10 sub-tasks, each fanning further). Recursion adds latency and debugging at every layer. If problem doesn't naturally decompose into clean sub-trees, adding indirection for no gain. Default to flat centralized first.

---

## Day 56: Tracking Long-Running Async Jobs

**Scenario:** Video upload processing, 2–8 minutes. Millions of users. What do you expose to the client?

> [!success] **A: Polling endpoint** ✅ — client hits `/jobs/:id/status` every 5s until done. Client-controlled, stateless, scales independently. Server doesn't care if client disconnects/retries/crashes — job runs, status endpoint just answers queries. 5s polling for 2–8 min job is trivially cheap. Key rules: stable, idempotent job IDs; TTL on job records; exponential backoff not fixed intervals. LinkedIn, YouTube, S3 multipart uploads all use polling for async job status.

- [ ] **B: Webhook** — great for server-to-server where receiver has stable HTTPS endpoint. Falls apart for mobile clients (no public URL), NAT/firewall environments, and when receiver down at delivery time. Need retry queue, delivery guarantees, signature verification. Works as supplementary for platform integrations, not primary client notification.
- [ ] **C: SSE / WebSocket** — fantastic for chat, live dashboards, collaborative editing. For job taking 2–8 minutes triggered once: holding open connection, burning file descriptor, adding connection-management complexity for maybe 3 meaningful state changes. Makes sense for sub-second updates or continuous streaming. For async job progress, polling cheaper and simpler.
- [ ] **D: Synchronous wait** — keeping HTTP connection open 2–8 minutes kills load balancer (most timeout 30–60s), ties up server thread, gives client no recovery if connection drops mid-job. How systems get "stuck" — jobs complete but client never hears because connection dropped. Never block on long-running work.

---

## Day 57: Consistency for Payment-Confirmation Reads ⭐

**Scenario:** 50K writes/sec, reads 10x that. Split Postgres into primary + 2 replicas. Payment confirmation reads from replica — returned stale data 200ms after write. User saw "payment pending" when it already succeeded. Replication lag: 80–300ms under load. (~ Read after write)

- [ ] **A: Synchronous replication** — primary waits for replica to confirm before ACKing write. Zero lag, reads always consistent. Cost: every write = primary_write_time + network roundtrip to replica. Under load with flaky replica, write latency hostage to slowest replica. Sync replica goes down → either halt writes or fall back to async breaking guarantee. 3am decision. Serious architectural commitment for whole DB.
- [ ] **B: Semi-sync replication** — primary waits for replica to write to relay log. Sounds like middle ground. Replica acknowledged receipt of bytes — not that data is applied and readable. Relay log is incoming queue, not applied state. Still read stale data. Protects from data loss on primary failure; does NOT protect from replication lag on reads. Different problem entirely.

> [!success] **C: Route payment confirmation reads to primary** ✅ — payment confirmations are a tiny slice of read traffic (~0.1%). Not routing ALL reads to primary — just reads where stale data causes visible user harm. Pattern called read-your-writes consistency. Stripe, Shopify, every serious fintech does this. Flag/middleware: "if consistency-sensitive flow, read from primary." Everything else keeps hitting replicas. Primary read traffic increases slightly — negligible. No topology change, no new failure modes, surgical precision.

- [ ] **D: Sleep 500ms after write** — seems pragmatic. Replication lag isn't fixed constant: 50ms now, 300ms during spike, 2s during vacuum. Hardcoded sleep = either too slow or still broken. Every payment path artificially 500ms slower. When sleep isn't enough during spike — back to original bug with worse latency.

---

## Day 58: Observability for LLM Agent Pipelines

**Scenario:** 2am. LLM agent on fire, every log says HTTP 200. AI support agent chains 4–5 prompts per request, calls tools, hits vector search, calls back into API. Token spend jumped $180→$540/day, no idea which flow caused it. Eval suite passes 94% in CI, prod users hitting hallucinations. On-call engineer literally cannot answer "why is this run slow/expensive/wrong?"

> [!success] **A: Structured trace IDs through every LLM + tool call** ✅ — every problem is same root cause: can't see shape of single agent run. Need span-level attributes: model name, prompt tokens, completion tokens, cost, tool name, retrieval doc IDs, actual prompt/response payload. LangSmith, Helicone, Arize, Langfuse give this out of box. The 14-second span opens into 7 sub-spans: one taking 9s was Claude fallback from rate limit. $540/day spike is one user hammering agent that recursively calls itself. Hallucinations correlate with retrievals returning 0 chunks.

- [ ] **B: LLM-as-judge eval pipeline** — answers different question: is quality trending up or down? Not debugging tool. "78% correctness on last 200 samples" tells nothing about the request that broke. Evals without tracing are unfalsifiable — no way to drill into failing samples. Step 2; ride on top of traces.
- [ ] **C: Cost dashboards + budget alerts** — same info you already had from the bill. Aggregate cost without span-level attribution tells you room is on fire, not which wall. Can't build per-agent, per-user attribution without instrumenting spans first. Solving CFO's problem, not on-call engineer's.
- [ ] **D: Custom middleware, own your data** — need: schema for nested agent runs, trace tree visualizer, correlation IDs across async tool calls, sampling logic, retention, PII redaction, cost rollups. Just rebuilt Langfuse badly in spare time while incident still open. Every serious LLM observability tool emits OpenTelemetry-compatible spans — switch vendors in a week if needed. Ship vendor now, revisit self-hosting when earned that problem.

---

## Day 59: Designing Idempotency Keys for Payments ⭐

**Scenario:** Payment service charged customer twice. Same request, different response code. Client retried. No dedup logic. Downstream calls (Stripe, Kafka, wallet credit) cannot be undone once triggered.

> [!success] **A: Client-generated keys** ✅ — client sends UUID as `Idempotency-Key` header. Server stores `key → response` in Redis with 24h TTL. Flow: (1) Write key with status `pending` before processing (Redis SET NX), (2) Process payment, (3) Update key to `completed` with full response body. Write key first, not after — if crash between payment succeeding and key write, charged with no dedup record. Scope to `(customer_id, key)`. TTL: 24h standard, 72h for aggressive retry clients. How Stripe, Braintree do it.

- [ ] **B: Server-generated keys** — client calls `POST /payments/init`, server returns one-time key, client uses on actual payment. Gives: pre-validation before money moves, audit trail at key issuance, protection against garbage UUIDs, full key lifecycle control. Shines for internal service-to-service and regulated environments. Hurts: mobile on flaky networks now has two calls that can fail independently — retry complexity goes up.
- [ ] **C: Deterministic key from business fields** — `sha256(customer_id + order_id + amount + currency)`. Same business intent = same key. Falls apart on legitimate retries: same customer, same amount, same item, but fresh order after refund. Hash matches completed request — returns cached success for brand new charge that should go through. Plus field serialization drift across SDK versions silently breaks dedup window. Right for internal job dedup; never for customer-facing payment flows.
- [ ] **D: Outbox + idempotent consumer** — strongest for distributed systems. Payment record + outbox event in one DB transaction. Worker processes downstream using row ID as dedup token. No separate key store. Exactly-once enforced at DB layer. Cost: outbox table + reliable worker + idempotent consumers. Overkill at 100 payments/day. Only defensible architecture at 10K TPS with regulatory requirements.

---

## Day 60: Architecting a SaaS Platform from Scratch ⭐

**Scenario:** New SaaS platform. 50K req/s at launch. Multi-tenant. Real-time data. Global users. AI inference built in. 3 months, blank slate.

- [ ] **A: Distributed microservices from day one** — 50K RPS sounds like you need microservices. Doesn't. Solved LB problem, not distribution problem. What you actually get: 6+ independently deployable services before finding real domain boundaries, distributed transactions across auth/billing/inference, network hops on every in-process call, 3 months infra work instead of product. Amazon's two-pizza teams were for existing services with known boundaries. You don't know yours yet.

> [!success] **B: Modular Monolith** ✅ — one deployable unit with clean internal module boundaries (auth, billing, inference, core domain — no shared DB tables, no cross-module direct calls). Single deploy, single observability surface, single transaction boundary. Fast iteration — no network serialization, no cross-service API contracts to version. The constraint isn't scale (50K RPS is solved LB problem, not distribution problem). It's 3-month runway + uncertainty about domain boundaries. Extract services later when you know which boundary is real — migration is refactor, not rewrite. AI inference: latency dominated by model I/O (50–500ms), not app code — reason to put behind clean interface, not separate service on day one.

- [ ] **C: Serverless (Lambda/Cloud Functions)** — "scales to zero" sounds great until pricing 50K RPS sustained. 5,000 concurrent Lambda executions at 100ms avg. Paying more than reserved EC2 cluster. Cold starts are real with "real-time data" promise. AI inference in Lambda = cold start + memory limit + 15-min hard timeout = pain. Serverless wins for bursty, unpredictable event workloads — not SaaS with consistent load and real-time requirements.
- [ ] **D: Event-driven from day one (Kafka backbone)** — trips up engineers who read about Kafka at Netflix/Uber. Event-driven is right answer — for Netflix and Uber after they've mapped their domain. Starting with Kafka before working system: every feature needs event schema + producer + consumer before working, debugging "why didn't this event get processed" in week 2, eventual consistency as default when you don't know which operations need strong consistency, Kafka ops overhead before validating product. Event-driven is optimization for known system, not foundation for unknown one.

---

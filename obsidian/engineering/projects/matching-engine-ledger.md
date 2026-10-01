# Matching Engine + Ledger — Design

> Flagship project for [[banking-trading backend engineer]].
> One repository, two halves, three interview stories.
> Java 21 · Spring Boot · PostgreSQL · Kafka · JMH · HdrHistogram

---

## Why this project

| | A banking interviewer asks about | A trading interviewer asks about |
| --- | --- | --- |
| **Ledger** | The whole conversation | Context — where trades settle |
| **Matching engine** | "Interesting, tell me more" | The whole conversation |
| **The seam** | Outbox, exactly-once settlement | Why the hot path never touches a DB |

The seam is the best of the three. It shows you understand the latency/durability
trade-off rather than just knowing two patterns. Most candidates have one half.

The commit history is part of the artifact: correctness first, latency layered on
top. That sequence is itself the argument.

---

## Architecture

```
   Order ──►  ┌───────────────────────┐
              │   MATCHING ENGINE     │   in-memory, single-threaded
              │   order book          │   no I/O, no locks, no allocation
              │   price-time priority │   target: p99 < 10 µs
              └───────────┬───────────┘
                          │  TradeExecuted events
                          ▼
              ┌───────────────────────┐
              │   SETTLEMENT          │   consumes trades
              │   → double-entry      │   PostgreSQL, ACID
              │   → outbox → Kafka    │   target: correctness, not speed
              └───────────────────────┘
```

**The core decision:** the matching engine is deliberately *not* durable and *not*
transactional on the hot path. Durability is someone else's job, downstream and
asynchronous. Real exchanges are built this way. Being able to defend that split
is the point of the project.

---

## Scope

**In scope**
- One trading symbol
- Limit orders, market orders, cancel
- Double-entry ledger with idempotency
- Outbox → Kafka
- Single instance, single process

**Explicitly out of scope** — this project dies if it grows

| Not building | Why |
| --- | --- |
| Auth, user management, UI | Nobody asks about it |
| Multi-instance, consensus, replication | One instance proves the same points |
| Real market data feeds (ITCH/FIX) | Optional stretch, not core |
| Exotic order types (stop, iceberg, FOK) | Limit + market + cancel is the whole lesson |
| Multiple symbols | Adds bookkeeping, teaches nothing new |

Finish depth, not breadth: **provable correctness** and **measured performance**.
A single-symbol book with a real latency histogram beats a half-built exchange
with no numbers.

---

# Stage A — Ledger (Months 3–9)

## Domain model

Three tables carry the whole idea.

```sql
CREATE TABLE accounts (
    id           BIGSERIAL PRIMARY KEY,
    owner_id     BIGINT      NOT NULL,
    currency     CHAR(3)     NOT NULL,
    account_type TEXT        NOT NULL,   -- USER | FEE | SETTLEMENT
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (owner_id, currency, account_type)
);

CREATE TABLE transactions (
    id              BIGSERIAL PRIMARY KEY,
    idempotency_key TEXT        NOT NULL UNIQUE,
    kind            TEXT        NOT NULL,   -- TRANSFER | TRADE_SETTLEMENT | FEE
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE entries (
    id             BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT         NOT NULL REFERENCES transactions(id),
    account_id     BIGINT         NOT NULL REFERENCES accounts(id),
    amount         NUMERIC(38,18) NOT NULL CHECK (amount <> 0),
    created_at     TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE INDEX idx_entries_account ON entries (account_id, id);
CREATE INDEX idx_entries_tx      ON entries (transaction_id);
```

**`NUMERIC`, never `DOUBLE PRECISION`.** `0.1 + 0.2 != 0.3` in binary floating
point. This is the first thing a finance interviewer checks.

### The three rules

**1. Never UPDATE a balance.** Only INSERT entries. A balance is
`SUM(amount)` over an account — *derived state*, not stored state. No lost
updates are possible, and every unit of money is traceable to its origin.

**2. Every transaction sums to zero.** Money moves; it is not created or
destroyed. This invariant is checkable at any moment:

```sql
-- must return zero rows, always
SELECT transaction_id, SUM(amount)
FROM entries
GROUP BY transaction_id
HAVING SUM(amount) <> 0;
```

**3. Idempotency via UNIQUE constraint.** A retried request with the same key
violates the constraint on the second insert; catch it and return the original
result. Networks are unreliable and clients retry — this is the correct handling,
not defensive application-level checks.

## Balance strategy — write an ADR

Deriving `SUM(entries)` on every read is correct but gets slow. Three options,
and the trade-off is the interesting part:

| Option | Correct | Fast | Note |
| --- | --- | --- | --- |
| Always `SUM(entries)` | ✅ | ❌ | Start here. Correct by construction. |
| Cached `account_balances` row | ⚠️ | ✅ | Can drift; needs the same transaction |
| Periodic snapshot + delta since | ✅ | ✅ | What real ledgers do |

Start with option 1. Move to option 3 once you can *measure* that option 1 is too
slow. "I benchmarked it and then changed it" is a much stronger story than
"I guessed and built the complicated one."

```sql
-- Option 3, added later
CREATE TABLE balance_snapshots (
    account_id     BIGINT         NOT NULL REFERENCES accounts(id),
    last_entry_id  BIGINT         NOT NULL,
    balance        NUMERIC(38,18) NOT NULL,
    created_at     TIMESTAMPTZ    NOT NULL DEFAULT now(),
    PRIMARY KEY (account_id, last_entry_id)
);
```

## Concurrency — the section interviewers push hardest on

Two concurrent withdrawals from the same account must not both succeed against
the same balance. Implement **both** strategies and benchmark them.

**Pessimistic**

```sql
BEGIN;
SELECT balance FROM ... WHERE account_id = $1 FOR UPDATE;
-- check sufficient funds
INSERT INTO entries ...;
COMMIT;
```

**Optimistic** — JPA `@Version`, retry on `OptimisticLockException`.

- [ ] Benchmark both with pgbench at 1 / 2 / 4 / 8 / 16 concurrent clients
- [ ] Find and document the crossover point
- [ ] Explain *why* it is where it is (contention rate vs retry cost)

Expected shape: optimistic wins under low contention, loses badly under high
contention because retries multiply. Knowing the shape and having your own
numbers for it is a senior-level answer.

- [ ] Choose and justify an isolation level. Write down why `READ COMMITTED` is
      or is not sufficient here, and what `REPEATABLE READ` would change.
- [ ] Demonstrate write skew in this schema, then show `SERIALIZABLE` prevents it.

## Outbox

Writing to the DB and publishing to Kafka cannot be one atomic operation. The
outbox makes them one *database* transaction, with publication following after.

```sql
CREATE TABLE outbox (
    id           BIGSERIAL PRIMARY KEY,
    aggregate_id TEXT        NOT NULL,
    event_type   TEXT        NOT NULL,
    payload      JSONB       NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at TIMESTAMPTZ
);

-- partial index: only unpublished rows are ever scanned
CREATE INDEX idx_outbox_pending ON outbox (id) WHERE published_at IS NULL;
```

The entries and the outbox row are written in the same transaction. A poller
publishes to Kafka and marks `published_at`. If the app crashes between publish
and mark, the event is re-sent — **at-least-once**, so consumers must be
idempotent. Say this out loud in the interview; it shows you know what guarantee
you actually built.

## Saga

Extend to a two-service flow (e.g. reserve funds → confirm booking) with
compensating transactions.

- [ ] Inject failure at each step
- [ ] Verify clean compensation for every failure point
- [ ] Zero resource leaks across 10k operations

## Test matrix — all must pass

| Test | Proves |
| --- | --- |
| Every transaction sums to zero | Core invariant |
| DB crash mid-transaction | Atomicity |
| Duplicate idempotency key | Exactly-once semantics |
| Concurrent transfers, same account | No lost update |
| App crash mid-outbox-publish | At-least-once delivery |
| Saga failure at step 1 / 2 / 3 | Clean compensation |
| Negative balance attempt | Constraint holds |
| 100k random transfers, then invariant check | Correctness at volume |

Use Testcontainers for a real PostgreSQL. Mocked DB tests prove nothing here.

## Numbers to record

- [ ] Transfers/sec at 1 / 2 / 4 / 8 / 16 threads
- [ ] Optimistic vs pessimistic throughput, with the crossover
- [ ] p50 / p99 transfer latency
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` before and after each index change

---

# Stage B — Matching Engine (Months 9–15)

## The order book

```
   ASKS (sell)              BIDS (buy)
   ───────────              ───────────
   102.5 × 300              100.0 × 500   ← best bid
   102.0 × 150               99.5 × 200
   101.0 × 200  ← best ask   99.0 × 800
```

**Price-time priority**, the rule at nearly every exchange:
1. Better price first
2. At equal price, earlier order first (FIFO)

## Matching algorithm

```
on LimitOrder(side, price, qty):
    book = opposite_side_book(side)

    while qty > 0 and book.best_price crosses price:
        level = book.best_level()
        resting = level.head()                  # FIFO

        fill = min(qty, resting.remaining)
        emit TradeExecuted(resting.id, incoming.id, level.price, fill)

        qty                -= fill
        resting.remaining  -= fill

        if resting.remaining == 0:
            level.pop_head()
            if level.empty(): book.remove_level(level)

    if qty > 0:
        own_side_book(side).insert(price, qty)   # rests in the book
```

"Crosses" means: a buy at price `p` crosses any ask `<= p`; a sell crosses any
bid `>= p`. A market order crosses everything until filled or the book empties.

## Data structures — where the engineering is

| Requirement | Structure | Why |
| --- | --- | --- |
| Best bid/ask in O(1) | Tick-indexed array + cached pointer | Hottest read in the system |
| FIFO within a price level | Intrusive doubly-linked list | O(1) append and unlink |
| Cancel by order ID in O(1) | `Long2ObjectMap<OrderNode>` | See below |
| No allocation on hot path | Preallocated object pool | GC pause destroys p99 |

**The insight worth stating in an interview:** in real markets, the large majority
of orders are cancelled rather than filled. Cancel performance matters more than
match performance. Design for O(1) cancel first.

Tick-indexed array: prices are discrete (tick size), so map price → array index
directly instead of using a tree. Memory for the full range, O(1) access, no
pointer chasing, cache-friendly. The trade-off — memory vs range — is an ADR.

## Latency work

Do these **in order**, measuring after each. Applying all of them at once teaches
nothing because you cannot attribute the improvement.

1. [ ] **Baseline.** Naive implementation, `TreeMap`, allocation everywhere.
       Record p50/p99/p99.9. This number matters — everything is measured
       against it.
2. [ ] **HdrHistogram** in the harness. Never report averages; the tail is the
       product.
3. [ ] **Kill allocation.** Object pool for order nodes, reuse event objects.
       Verify with JFR or `-Xlog:gc` that the hot path allocates nothing.
4. [ ] **Primitive collections.** `Long2ObjectHashMap` (Agrona) instead of
       `HashMap<Long, Node>` — no boxing, better locality.
5. [ ] **Cache-line padding.** `@Contended` on the top-of-book struct; measure
       false sharing before and after.
6. [ ] **Disruptor.** Replace the inbound queue with an LMAX ring buffer.
7. [ ] **Single-threaded core.** The matching engine owns its state and never
       locks. Concurrency lives at the edges.
8. [ ] **Profile.** async-profiler flame graph; fix the top item; re-measure.

**Targets** — reachable on the JVM for a single-symbol book:

| Metric | Target |
| --- | --- |
| p50 order insert | < 1 µs |
| p99 | < 10 µs |
| p99.9 | < 50 µs |
| Throughput | > 1M orders/sec single-threaded |

If p99.9 is much worse than p99, the cause is almost always GC or a cache miss.
Finding out which — and proving it — is the exercise.

## Test matrix

| Test | Proves |
| --- | --- |
| Price-time priority respected | Core correctness |
| Partial fills across multiple levels | Matching loop |
| Cancel a resting order | O(1) unlink, no leak |
| Cancel an already-filled order | Idempotent, no crash |
| Market order against an empty book | Edge case |
| Self-trade (same owner both sides) | Policy decision — document it |
| Replay 1M random orders, verify book state | Correctness at volume |
| Sum of fills equals sum of order quantities | Conservation invariant |

## Numbers to record

- [ ] Latency histogram: p50 / p99 / p99.9 / max, before and after each of the
      8 optimization steps
- [ ] Throughput (orders/sec), same
- [ ] GC pause distribution during a sustained run
- [ ] Flame graph before and after the top fix

---

# The seam — trade settlement

The matching engine emits `TradeExecuted`. Settlement turns each trade into a
ledger transaction: buyer's cash decreases, seller's cash increases, asset moves
the other way, fee accounts take their cut. All entries, one transaction, sums to
zero.

```
TradeExecuted(buyOrderId, sellOrderId, price, qty)
    │
    ▼
transaction (idempotency_key = trade_id)
    entries:
        buyer.cash    -= price × qty
        seller.cash   += price × qty - fee
        buyer.asset   += qty
        seller.asset  -= qty
        fee_account   += fee
                          ─────────
                          sum = 0
```

- [ ] `trade_id` is the idempotency key — replayed trades settle exactly once
- [ ] Settlement is asynchronous; the engine never blocks on it
- [ ] Backpressure: what happens when settlement falls behind the engine?
      Document the answer. This is a *very* common interview question.
- [ ] Failure test: kill settlement mid-batch, restart, verify no double-settle
      and no lost trade

---

## ADRs to write

One file each in `docs/adr/`. These are the interview script.

1. Why `NUMERIC` and not floating point
2. Derived balance vs cached vs snapshot+delta
3. Optimistic vs pessimistic locking — with the benchmark that decided it
4. Chosen isolation level, and what it does not protect against
5. Outbox over dual-write, and the at-least-once consequence
6. Tick-indexed array vs tree for price levels — memory/range trade-off
7. Single-threaded matching core — why not a thread pool
8. Why the matching engine does not write to the database
9. Backpressure policy when settlement lags
10. Self-trade policy

---

## Milestones

Every milestone is a valid stopping point with a story to tell.

| Months | Deliverable |
| --- | --- |
| 3–5 | Ledger schema, double-entry, invariant tests green |
| 5–7 | Idempotency, both locking strategies benchmarked, failure tests |
| 7–9 | Outbox + Kafka, saga with compensation |
| 9–11 | Order book: structures, matching, cancel, correctness tests |
| 11–13 | Trade → settlement seam, backpressure, failure tests |
| 13–15 | Latency: histogram, zero-allocation, Disruptor, flame graphs |

Get an offer at month 9? The ledger half alone is already a strong story.

---

## Repository standard

- [ ] `README.md`: problem statement, architecture diagram, key decisions,
      benchmark tables, "what I'd do differently"
- [ ] `docker-compose up` works for a stranger in under 5 minutes
- [ ] `docs/adr/` — the ten decisions above
- [ ] GitHub Actions CI badge; tests run on every push
- [ ] Benchmark results committed as data, not just prose
- [ ] Commit messages in English, written as a narrative of the work

---

## Questions this project answers

**Banking**
- How do you prevent double-spending under concurrent requests?
- What happens if the client retries a payment?
- How do you guarantee the ledger never loses money?
- Why `NUMERIC` and not `double`?
- Which isolation level, and what does it not protect against?
- How do you publish an event and commit a transaction atomically?

**Trading**
- How do you get best bid/ask in O(1)?
- How do you cancel an order in O(1)?
- What is your p99, and what causes the tail?
- How do you avoid allocation on the hot path?
- What is false sharing and where does it show up here?

**Senior, either side**
- Why doesn't the matching engine write to the database?
- What happens when settlement can't keep up?
- Where would this break at 10× the load?

# Banking / Trading Backend Engineer Roadmap

> **12–15 months · 24 hrs/week target · 16 hrs/week floor · ~1,450 hrs**
> Java/Spring (trunk) · PostgreSQL · Kafka · C++ (secondary) · English (gate)

---

## Mission

**Land a backend role in the banking/trading space within 12–15 months, with one
portfolio project that proves both transactional correctness and latency
engineering — while building the low-level foundation to move toward
low-latency/HFT later without starting over.**

Banking and trading are treated as **one merged target**. Whichever lands first
is the right answer. Both are reached through the same trunk: Java + JVM depth,
transactional correctness, and measured performance.

---

## Operating principles

1. **Plan against the floor, not the target.** Content is sized for 16 hrs/week.
   Anything above that is acceleration, not obligation. A 24h week shortens the
   timeline; a 12h week does not break the plan. A plan that requires 24h to
   reach the goal collapses on the first bad month — and the real loss is
   motivation, not hours.
2. **Study and interview in parallel.** Do not wait for the roadmap to finish
   before applying. Every rejection tells you what to learn next, faster and more
   accurately than any plan can predict.
3. **One flagship, evolving.** The ledger becomes the matching engine. Same repo,
   visible evolution, two interview stories.
4. **Technical work is done in English.** Reading, ADRs, commit messages, and
   spoken system design. This adds ~4–6h/week of English exposure at zero extra
   cost.
5. **Heavy work on weekends.** The binding constraint is mental energy, not clock
   hours. Deep JVM study after a 9-hour debugging day is low-yield.

---

## Stack & time allocation

| Area | Role | Share |
| --- | --- | --- |
| English | Hard gate for every international and trading firm | ~33% |
| Java / Spring / JVM | Trunk language for both banking and low-latency finance | ~21% |
| Flagship project | Ledger → matching engine; the portfolio centerpiece | ~21% |
| PostgreSQL | MVCC, WAL, isolation, EXPLAIN — interrogated directly in banking | ~8% |
| Low-level track | C++, memory model, perf — feeds the order book, keeps momentum | ~8% |
| System design + LeetCode | Interview surface for any senior role | ~8% |

---

## Weekly rhythm — 24 hrs

| Day | Hrs | Focus |
| --- | --- | --- |
| Mon | 3 | English 2 · LeetCode 1 |
| Tue | 3 | English 2 · Java/Spring 1 |
| Wed | 3 | English 2 · Java/Spring 1 |
| Thu | 3 | English 2 · System design 1 *(spoken, in English, recorded)* |
| Fri | 3 | PostgreSQL lab 2 · Low-level 1 |
| Sat | 6 | Flagship project 5 · Low-level 1 |
| Sun | 3 | Java/Spring 2 · Weekly ADR + next-week plan 1 |

### Floor rhythm — 16 hrs

Drop to: English 6 · Java 3 · Flagship 4 · PostgreSQL 1 · LeetCode/SysDesign 1 ·
Low-level 1. Keep **every category alive** — cutting a category entirely is how
plans die. Reduce depth, not breadth.

---

## Priorities

### 1. English B1 → B2 · 8 hrs/week · continuous · **priority #1**

Missing Java still gets you interviews at Node/Python shops. Missing English
gets you filtered before any interview at an international firm — and every
trading firm demands more English than a retail bank does.

| Activity | Hrs | Note |
| --- | --- | --- |
| Speaking | 3 | Highest yield. Never cut this first. |
| Active listening | 2 | With transcript; replay what you missed. |
| Writing | 1 | Overlaps with ADRs and commit messages. |
| Vocabulary / grammar | 2 | Lowest yield. Do not let this expand. |

- [ ] Switch all commit messages, ADRs, and docs to English
- [ ] Record yourself for 4–5 min on each of 5 work stories, then review:
  - [ ] Two GKE clusters — standard private vs Autopilot, and why
  - [ ] Progressive multi-cluster traffic cutover (50% → 100%)
  - [ ] MongoDB index design — eliminating COLLSCANs
  - [ ] GKE → Cloud Run migration
  - [ ] eKYC pipeline under 2 seconds
- [ ] Replace exam-prep listening with technical talks and podcasts
- [ ] Weekly: one recorded system-design walkthrough in English

**Ceiling note:** English has a daily absorption limit. 8 hrs/week is already
>1h/day. Pushing to 14h turns the surplus into passive study — the lowest-yield
mode. Extra capacity belongs in technical work done *in English*.

**Gate:** speak 5 minutes on one of your own technical decisions, get
cross-examined, and stay fluent.

---

### 2. Java · Spring Boot · JVM · 4–5 hrs/week · Months 1–9

The trunk. Banking runs Spring; low-latency finance runs the same JVM. Coming
from NestJS this is a syntax and runtime change, not an architecture change.

**Spring / application layer**

- [ ] Map NestJS concepts onto Spring: `@Injectable`→`@Service`,
      `@Module`→`@Configuration`, Guards/Interceptors→Filters/AOP, TypeORM→JPA
- [ ] `@Transactional` AOP proxy: why same-class calls bypass it, `REQUIRES_NEW`,
      rollback rules
- [ ] JPA/Hibernate: N+1, fetch strategies, optimistic locking via `@Version`
- [ ] Hexagonal architecture with Maven multi-module; ArchUnit test fails the
      build on a Spring import in the domain module
- [ ] Flyway migrations

**JVM internals — this is the part that carries over to low-latency**

- [ ] G1GC: region-based collection, concurrent marking, safepoints, write barriers
- [ ] ZGC: concurrent relocation via load barriers; pause model vs G1
- [ ] Java Memory Model (JSR-133): happens-before, `volatile`, when volatile is
      insufficient
- [ ] Write a three-way table: Java `volatile` vs Go atomic vs C++
      relaxed/acquire/release
- [ ] JIT tiered compilation (C1/C2), inlining, deoptimization —
      `-XX:+PrintCompilation`, `-XX:+PrintInlining`
- [ ] JMH done correctly: warmup, `Blackhole`, avoiding dead-code elimination
- [ ] Java 21 virtual threads: carrier threads, pinning hazards, when platform
      threads still win
- [ ] Read JCIP Ch. 1–5, 10–12
- [ ] Read 5 JVM Anatomy Quarks posts (Shipilev)

**Gate:** explain why `@Transactional` fails on a same-class call, and when
`volatile` is not enough — both without notes.

---

### 3. ★ Flagship: Matching Engine + Ledger · 5–6 hrs/week · Months 3–15

One repository. The banking half and the trading half share a domain, and the
commit history shows the evolution — which is itself a good interview story.

#### Stage A — Ledger (Months 3–9) · the banking half

- [ ] Double-entry bookkeeping with invariant tests (debits always equal credits)
- [ ] Money as `NUMERIC` / `BigDecimal` — **never** floating point
- [ ] Idempotency keys backed by a UNIQUE constraint
- [ ] Outbox pattern, with Kafka as the transport
- [ ] Optimistic vs pessimistic locking — benchmark both with pgbench, document
      the crossover point
- [ ] Structured JSON logging with correlation IDs; Prometheus metrics
- [ ] Failure tests, all must pass:
  - [ ] DB crash mid-transaction
  - [ ] Duplicate request (same idempotency key)
  - [ ] App crash mid-outbox-processing
  - [ ] Concurrent transfers against the same account — no lost update
- [ ] Saga: extend to a two-service booking flow; inject failure at each step and
      verify clean compensation, zero resource leaks over 10k operations
- [ ] JMH: optimistic vs pessimistic at 1/2/4/8 threads

#### Stage B — Matching Engine (Months 9–15) · the trading half

- [ ] ADR: price level storage — tick-indexed array vs map vs flat hash map
- [ ] Tick-indexed price level array, O(1) best bid/ask pointer
- [ ] FIFO order queue per price level (doubly-linked, O(1) cancel)
- [ ] Order ID → price level map
- [ ] Settle matched trades into the Stage A ledger — the two halves connect
- [ ] Zero allocation on the hot path: preallocate, reuse, off-heap where needed
- [ ] `alignas`-equivalent padding / `@Contended` — verify top-of-book occupies
      its own cache line
- [ ] Replace the internal queue with an LMAX Disruptor ring buffer
- [ ] HdrHistogram: record p50 / p99 / p99.9 / max for order insertion
- [ ] Benchmark before/after every optimization — a number for each
- [ ] Profile with async-profiler / perf; produce a flame graph before and after

#### Repository standard

- [ ] Architecture diagram
- [ ] README: problem statement, design decisions, "what I'd do differently"
- [ ] `docker-compose up` works for a stranger in under 5 minutes
- [ ] ADR folder, one per significant decision
- [ ] CI badge (GitHub Actions)

**Gate:** all failure tests pass; before/after benchmark tables for both halves;
you can defend every ADR under adversarial questioning.

---

### 4. PostgreSQL · 1–2 hrs/week · Fridays · Months 1–12

Banking interviews probe this directly.

- [ ] Install `pageinspect`; inspect raw page layout after 3 INSERTs
- [ ] MVCC: xmin/xmax, tuple versions, snapshot visibility; demonstrate that
      UPDATE writes a new tuple rather than modifying in place
- [ ] B-tree internals: splits, fill factor, covering indexes; Index Only Scan vs
      Index Scan and what the visibility map enables
- [ ] `EXPLAIN (ANALYZE, BUFFERS)` on 5 queries of increasing complexity;
      identify every node type
- [ ] Isolation levels, two psql sessions:
  - [ ] Non-repeatable read at Read Committed
  - [ ] **Write skew at Repeatable Read**
  - [ ] Serializable prevents it
- [ ] Read Berenson et al., "A Critique of ANSI SQL Isolation Levels"
- [ ] WAL → checkpoint → crash recovery, step by step (Rogov Ch. 9)
- [ ] Buffer manager: `shared_buffers`, clock-sweep; `pg_buffercache` for hottest
      relations
- [ ] Autovacuum: dead tuple threshold formula, bloat, TOAST
- [ ] Partition the ledger by month; verify `Partitions: filtered` in EXPLAIN
- [ ] `pg_stat_statements`: find the top-5 slowest queries in the flagship
      workload, fix each, document before/after EXPLAIN
- [ ] PgBouncer in transaction mode — verify Spring behaves correctly
- [ ] Streaming replication: WAL shipping, replication slots

**Gate:** read any `EXPLAIN (ANALYZE, BUFFERS)` and identify the bottleneck node
within 2 minutes. Reproduce write skew and explain why Serializable prevents it.

---

### 5. Kafka · 2–3 week focused sprint (Month 2), then used in the flagship

The largest named gap in target job descriptions, and the fastest to close.

- [ ] Partitions, consumer groups, offsets, rebalancing
- [ ] Ordering guarantees — and what they cost
- [ ] At-least-once vs exactly-once; idempotent producer; transactions
- [ ] Consumer lag, backpressure, retry and DLQ patterns
- [ ] **Why Kafka instead of Redis Pub/Sub** — the durability and replay argument
- [ ] Use it for real as the Outbox transport in the flagship

---

### 6. System design + LeetCode · 2 hrs/week · continuous

- [ ] 7-stage framework: requirements → capacity → API → data model → components
      → failure modes → scale
- [ ] Design, 45 min each, **spoken in English and recorded**:
  - [ ] Payment system *(you built this — defend every decision)*
  - [ ] Matching engine / exchange *(you built this)*
  - [ ] Rate limiter
  - [ ] Distributed cache
  - [ ] Message queue
  - [ ] Notification service
- [ ] LeetCode 30–45 min/day. Patterns over volume: arrays/strings, hash maps,
      binary search, trees, graphs, DP, heaps, monotonic stack
- [ ] LeetCode contests, 2/month
- [ ] **Codeforces: dropped.** Only required for top-tier HFT, which is not the
      merged target.

---

### 7. Low-level track · 2–3 hrs/week · no deadline, no gate

A protected slot. Cutting this entirely is how a purely pragmatic plan gets
abandoned in month three. It also directly feeds Stage B of the flagship.

You are **not starting C++ from zero** — OpenCV/ONNX/NCNN optimization work is real production C++, only cold.

- [ ] Refresh modern C++: RAII, move semantics, `unique_ptr`/`shared_ptr`,
      never raw `new`/`delete` (Effective Modern C++ Ch. 1–5, 7)
- [ ] `std::atomic` and memory orderings; implement a spinlock with
      acquire/release and explain why `seq_cst` is over-specified
- [ ] Watch Herb Sutter, "atomic Weapons" (both parts)
- [ ] **Lock-free MPSC queue** with hazard-pointer reclamation — read the
      Michael-Scott paper (1996) and Michael's hazard pointers paper (2004);
      stress test under ASAN and valgrind
- [ ] Cache hierarchy and false sharing: benchmark padded vs unpadded struct,
      demonstrate >5x penalty
- [ ] Store buffers, memory ordering on weak models (Drepper)
- [ ] `perf stat` / `perf record` / flame graphs on your own flagship
- [ ] OSTEP Ch. 13–23, at a relaxed pace — no gate
- [ ] io_uring vs `read()` benchmark at QD 1/32/128 *(optional, late)*

---

## Phases

### Phase 1 — Java foundation & market entry · Months 1–3 · ~290 hrs

Focus: Java/Spring, Kafka sprint, PostgreSQL core, English ramp-up.
**Applications start in week one, not after the phase.**

**Gate**
- [ ] A Spring Boot service with JPA, Flyway, and hexagonal layering enforced by ArchUnit
- [ ] Kafka producer/consumer with a deliberate rebalance and lag demonstration
- [ ] Read `EXPLAIN ANALYZE` and name the bottleneck node
- [ ] 5 recorded English work stories, reviewed
- [ ] CV corrected and submitted to at least 10 roles

---

### Phase 2 — Ledger & correctness · Months 4–9 · ~580 hrs

Focus: Stage A flagship, PostgreSQL depth, saga/outbox, C++ refresh.

**Gate**
- [ ] All ledger failure tests pass; pgbench locking comparison documented
- [ ] Write skew reproduced; Serializable prevents it
- [ ] Saga compensation clean across all injected failure points
- [ ] Lock-free MPSC queue passes stress tests under ASAN
- [ ] English: comfortable in a 30-minute technical conversation

---

### Phase 3 — Latency & interview readiness · Months 10–15 · ~580 hrs

Focus: Stage B flagship, low-latency JVM, profiling, system design, interviewing.

**Gate**
- [ ] Matching engine with a latency histogram and documented before/after per
      optimization
- [ ] Zero-allocation hot path verified; Disruptor integrated
- [ ] Explain G1GC write barriers, `std::atomic` acquire/release, and JMM
      happens-before — without notes
- [ ] Any of the 6 system designs in 45 minutes, in English
- [ ] Interviewing actively in both banking and trading-adjacent firms

---

## Parallel track — not "study"

Do these this week. They do not wait for the roadmap.

- [ ] **Fix the CV**: remove PostgreSQL, correct ECS→EKS, remove
      Lambda/EventBridge/CloudFront and the CDP-from-CRM claim, drop the
      unverified "2x performance", lower the verbs to match actual scope, add
      the GitHub link
- [ ] **Apply now.** Domestic fintech and digital banks accept the current
      profile. Treat every screening call as free calibration.
- [ ] **Switch commit messages and docs to English** — daily writing practice at
      zero cost
- [ ] **Push performance work at the current job**: measure real p99, build
      benchmarks, record numbers. It is CV material now and core skill later.
- [ ] When choosing between offers, ask which **domain** you will work in.
      Core ledger, payments/settlement, e-trading, market data, and securities
      order routing all lead toward the destination. Onboarding, CRM, mobile BFF,
      and admin portals do not.

---

## Reading guide

| Source | Scope | Serves |
| --- | --- | --- |
| **DDIA** — Kleppmann | Ch. 5, 7, 8, 9 | Transactions, consistency, consensus — the single highest-value book here |
| **PostgreSQL 14 Internals** — Rogov | Ch. 1–2, 9 | Page layout, MVCC, WAL |
| **JCIP** — Goetz | Ch. 1–5, 10–12 | Java concurrency, JMM |
| **JVM Anatomy Quarks** — Shipilev | 5 posts | GC, safepoints, JIT |
| **Effective Modern C++** — Meyers | Ch. 1–5, 7 | RAII, move semantics, atomics |
| **What Every Programmer Should Know About Memory** — Drepper | Selected | Cache hierarchy, false sharing, memory ordering |
| **OSTEP** | Ch. 13–23 | Virtual memory, scheduling — relaxed pace, no gate |

**Papers**

- [ ] Berenson et al., "A Critique of ANSI SQL Isolation Levels" (1995)
- [ ] Michael & Scott, lock-free queue (1996)
- [ ] Michael, hazard pointers (2004)
- [ ] Raft (Ongaro & Ousterhout, 2014) — **read only**, do not implement

---

## Milestones

| When | Expected |
| --- | --- |
| Month 1–3 | First offers from domestic fintech / digital banks, on current skills |
| Month 9 | Ledger complete; credible as a Java backend engineer in finance |
| Month 15 | Matching engine with latency numbers; interviewing at trading-adjacent firms |
| Year 2–4 | Move toward payment engines, e-trading, exchanges, securities, crypto |
| Year 4+ | Low-latency specialization; revisit HFT from inside the industry |

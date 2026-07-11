# Low-Level Systems Engineer Roadmap

> **12 months · 30 hrs/week · ~1,560 hrs** | C++17/20 · Go · Java/Spring · PostgreSQL
> Optional Phase 5: HFT Specialization (+3 months, ~180 hrs)

---

## Stack & Time Allocation

| Language | Role | Time |
|---|---|---|
| C++17/20 | Memory control, lock-free structures, storage engine, performance-critical systems | ~35% |
| Go | Systems glue, Raft consensus, HTTP proxy, network tools | ~30% |
| Java/Spring | JVM internals, GC deep-dive, Java Memory Model, wallet project | ~20% |
| PostgreSQL | Storage engine internals, MVCC, WAL, query planner — studied as artifact not tool | ~15% |

---

## Weekly Rhythm

| Day | Hours | Focus |
|---|---|---|
| Mon/Tue | 6 hrs | C++ or Go project work — commit + one-line dev log |
| Wed/Thu | 6 hrs | Read book chapter / paper / source code, notes in own words |
| Fri | 3 hrs | PostgreSQL lab — one EXPLAIN ANALYZE + one storage experiment |
| Sat | 8 hrs | Flagship project — inject failures, write benchmarks |
| Sun | 7 hrs | Write ADR/README for the week, plan next week |

---

## End-State Goals

### C++17/20
- [ ] Build thread-safe memory pool allocator: thread-local caches, CAS global pool, ABA protection — ASAN/UBSAN clean at 16 threads
- [ ] Build lock-free MPSC queue with hazard pointer memory reclamation — stress test passes under valgrind
- [ ] Build LSM-tree KV store: WAL, MemTable (skip list), SSTable, Bloom filter, leveled compaction, sharded LRU block cache, iterators
- [ ] Write correct RAII, move semantics, `std::atomic` with right memory orderings — never `new`/`delete` directly
- [ ] Apply CRTP for static polymorphism, C++20 concepts for type constraints, coroutines for lazy generators, `std::span` for zero-copy
- [ ] Use perf + flame graphs to find hotspots, vectorize with AVX2, measure with Google Benchmark

### Go
- [ ] Write concurrent Go with zero data races under `-race`
- [ ] Build HTTP reverse proxy: round-robin LB, rate limiter, graceful shutdown, pprof flame graph before/after
- [ ] Implement Raft consensus — MIT 6.824 Labs 2A–2D pass 50 consecutive runs, ≥4 documented bugs
- [ ] Understand G/M/P scheduler, goroutine stack copying, escape analysis, `sync.Pool`
- [ ] Build production services: structured logging, Prometheus metrics, gRPC streaming, context cancellation

### Java/Spring
- [ ] Explain G1GC and ZGC pause models, safepoints, write barriers
- [ ] Build digital wallet: double-entry bookkeeping, idempotency keys, Outbox pattern, failure tests all pass
- [ ] Know Java Memory Model happens-before chain — when `volatile` is insufficient
- [ ] Benchmark with JMH correctly: warmup, Blackhole, avoid JIT dead-code elimination
- [ ] Understand JIT tiered compilation (C1/C2), inlining, deoptimization via `-XX:+PrintCompilation`
- [ ] Use Java 21 virtual threads; know when platform threads are still needed

### PostgreSQL
- [ ] Read any `EXPLAIN (ANALYZE, BUFFERS)` and identify bottleneck within 2 minutes
- [ ] Explain MVCC with pageinspect: xmin/xmax, tuple versions, dead tuples, VACUUM
- [ ] Walk through WAL → checkpoint → crash recovery sequence step by step
- [ ] Reproduce write skew in two concurrent transactions; show Serializable prevents it
- [ ] Understand buffer manager (shared_buffers, clock-sweep), autovacuum threshold formula, TOAST
- [ ] Configure streaming replication, table partitioning, PgBouncer, fix top-5 slow queries via pg_stat_statements

### CS Fundamentals
- [ ] Explain virtual memory, TLB, page faults, cache hierarchy (false sharing, 64-byte lines), memory ordering
- [ ] Understand Linux CFS scheduler, VFS/inode/dentry, ext4 journaling, TCP kernel path
- [ ] Reason about lock-free algorithms: CAS, ABA, hazard pointers, epoch-based reclamation
- [ ] Apply distributed theory: vector clocks, consistent hashing, Raft, 2PC tradeoffs, FLP impossibility
- [ ] Design any of 8 classic systems in 45 minutes using 7-stage framework
- [ ] Use perf, bpftrace, off-CPU flame graphs to diagnose production performance issues

---

## Parallel Track: LeetCode + Codeforces

> Run concurrently with Phases 1–4. **60–90 min/day, every day.**
> LeetCode = interview pattern recognition. Codeforces = algorithmic depth + speed under pressure. Do both.

### Codeforces Rating Ladder

| Rating | Title | Problems | Notes |
|---|---|---|---|
| < 1200 | Gray / Newbie | Div. 3 A | Simple loops, conditionals, basic math. Clear in 2 weeks. |
| 1200–1399 | Green / Pupil | Div. 3 B / Div. 2 A | Greedy, sorting, prefix sums, basic BFS/DFS. Month 1 exit. |
| 1400–1599 | Cyan / Specialist | Div. 2 B–C | Binary search on answer, graph algorithms, basic DP. Month 2 exit. |
| 1600–1899 | Blue / Expert | Div. 2 C–D | Harder DP, Dijkstra, segment trees, DSU. Month 3–4 target. |
| 1900–2099 | Violet / Candidate Master | Div. 1 C / Div. 2 E | Tree DP, network flow, LCA, centroid decomp. Required for Jump Trading. |

### Month 1 — Linear Structures + Search
> CF target: **Pupil (1200)** | LC: ~50 problems Easy→Medium

**LeetCode**
- [ ] Arrays & Strings: sliding window (fixed + variable), two pointers, prefix sums, Kadane's
- [ ] Hash Maps & Sets: frequency counting, two-sum, anagram grouping, sliding window with freq map
- [ ] Binary Search: exact target, lower/upper bound, rotated sorted array, minimize-the-maximum
- [ ] Linked Lists: fast/slow pointer, reverse in-place, merge sorted, remove Nth from end

**Codeforces**
- [ ] Register on codeforces.com, set up account, enable rating
- [ ] Solve 30+ problems rated 800–1000: simple greedy, sorting, basic math
- [ ] Solve 20+ problems rated 1000–1200: GCD/modular arithmetic, prime sieve, constructive
- [ ] Participate in 2 live CF rounds (Div. 3 or Div. 2)
- [ ] Complete CF EDU: Binary Search section (15 problems)

**Exit gate:** LC medium array/string cold in <20 min. CF Div. 3 A/B solved within 10 min each.

### Month 2 — Trees + Graphs + Stack
> CF target: **Specialist (1400)** | LC: ~55 problems Medium

**LeetCode**
- [ ] Binary Trees: recursive DFS (pre/in/post), iterative BFS, LCA, diameter, path sum, serialize/deserialize
- [ ] Graphs: BFS shortest path, DFS connected components, topological sort (Kahn's + DFS), union-find, Dijkstra
- [ ] Stacks & Monotonic Stack: next greater element, largest rectangle in histogram, daily temperatures
- [ ] Intervals: merge overlapping, insert, sweep line (meeting rooms), minimum interval cover

**Codeforces**
- [ ] Solve 20+ problems rated 1200–1400: BFS/DFS on grids, basic number theory
- [ ] Solve 15+ problems rated 1400–1500: constructive algorithms, binary search applications
- [ ] Complete CF EDU: DSU (Disjoint Set Union) section (10 problems)
- [ ] Participate in 2 live CF rounds (Div. 2)
- [ ] For every unsolved contest problem: read editorial, write one-line insight note

**Exit gate:** LC medium graph cold in <25 min. Able to solve CF Div. 2 B within contest time.

### Month 3 — DP + Heaps + Backtracking
> CF target: **Expert (1600)** | LC: ~55 problems Medium→Hard

**LeetCode**
- [ ] DP: 1D (house robber, coin change), 2D (grid paths, edit distance, LCS), knapsack, LIS (patience sort)
- [ ] Heaps: top-K elements, K-way merge, sliding window maximum, find median from data stream
- [ ] Backtracking: permutations, combinations, subsets, N-queens, Sudoku solver
- [ ] Tries: insert/search/startsWith, word search II, autocomplete

**Codeforces**
- [ ] Solve 20+ problems rated 1500–1700: harder DP, Dijkstra on weighted graphs
- [ ] Solve 15+ problems rated 1700–1900: DSU applications, segment tree point-update range-query
- [ ] Complete Atcoder DP Contest — all 26 problems at atcoder.jp/contests/dp
- [ ] Participate in 2 live CF rounds
- [ ] Review editorial log weekly — accumulate ≥30 one-line insight notes

**Exit gate:** LC medium DP solved by defining subproblem first. CF Div. 2 C solved within contest time.

### Month 4 — Hard Problems + Contests + Mocks
> CF target: **Expert→CM (1800–2100)** | LC: ~50 problems Hard

**LeetCode**
- [ ] Hard: DP bitmask, segment tree range queries, Bellman-Ford, Floyd-Warshall, SCC (Tarjan/Kosaraju)
- [ ] LC contests: 2 per week (biweekly + weekly), 45-min max per problem
- [ ] Company-specific: filter by target company, last 6 months, top 30 per company

**Codeforces**
- [ ] Solve 20+ problems rated 1900–2200: tree DP, network flow, LCA with binary lifting
- [ ] Run 3 virtual contests per week (old Div. 2 rounds, 2-hour timer)
- [ ] Participate in 2 live CF rounds
- [ ] After every contest/virtual: read all editorials, update insight log

**Mock Interviews**
- [ ] Schedule 3 Pramp mocks per week (pramp.com — free)
- [ ] Do 2 paid mocks on interviewing.io before applying
- [ ] Record yourself solving problems — watch playback and note every hesitation point

**Exit gate:** LC top 25% contest rating. CF Expert (1600+). Cold-solve CF Div. 2 C in <30 min.

### Problem Category Reference

| Category | Count | Key Patterns |
|---|---|---|
| Arrays & Strings | 30–35 | Sliding window, two pointers, prefix sum, Kadane's, Boyer-Moore |
| Binary Search | 15–20 | Search space reduction, lo/hi template, minimize-the-maximum |
| Hash Maps & Sets | 20–25 | Two-sum, frequency count, sliding window with freq map |
| Binary Trees | 25–30 | DFS (pre/in/post), BFS (level order), LCA, define return type first |
| Graphs | 25–30 | BFS/DFS, topological sort, union-find, Dijkstra, 0-1 BFS |
| Dynamic Programming | 30–35 | Define subproblem → recurrence → base case → memoize/tabulate |
| Heaps | 15–20 | Top-K (min-heap size K), K-way merge, two-heap median |
| Backtracking | 15–20 | Draw decision tree first, choose→explore→unchoose |
| Advanced (FAANG Hard) | 20–25 | Monotonic stack, segment tree/BIT, bitmask DP, expression parsing |

---

## Phase 1: OS Deep · Go · PostgreSQL (Months 1–2, ~240 hrs)

### OS Fundamentals — Systems Depth (Weeks 1–3, ~60 hrs)

- [ ] Read OSTEP Ch. 13-23 — full Virtualization section. **Work chapter-by-chapter through the Reading Guide below — a chapter counts only when its self-checks pass cold**
- [ ] Draw a process virtual address space (stack, heap, BSS, text) from memory
- [ ] Study memory allocator internals: dlmalloc/ptmalloc, TCMalloc, jemalloc
- [ ] Explain why TCMalloc is faster than ptmalloc under high thread contention
- [ ] Study CPU cache hierarchy: L1 ~4 cycles, L2 ~12 cycles, L3 ~40 cycles, RAM ~200 cycles
- [ ] Write benchmark demonstrating false sharing penalty vs padded struct (>5x slowdown)
- [ ] Study memory ordering: store buffer, out-of-order execution, acquire/release, seq_cst
- [ ] Explain what a store buffer is and why it causes visibility problems on non-x86
- [ ] Study Linux I/O: epoll internals, Go netpoller, `src/runtime/netpoll_epoll.go`
- [ ] Trace a network read in Go from goroutine block → epoll event → goroutine wake-up
- [ ] Lab: run `strace` on 3 Go programs (file reader, TCP server, concurrent counter) — map every syscall
- [ ] Lab: run `perf stat` to see cache misses, branch mispredictions, IPC
- [ ] Lab: run `perf record + perf report` to find hotspots

### Linux Scheduler + File Systems + Network Stack (Weeks 2–4, ~40 hrs)

- [ ] Study Linux CFS: vruntime, red-black tree, nice values, cgroups v2 CPU controller
- [ ] Lab: use `chrt` and `taskset` to pin processes; measure scheduling latency with `perf sched latency`
- [ ] Explain why high-priority process accumulates vruntime slower
- [ ] Study VFS layer: inode, dentry, file descriptor table
- [ ] Trace the kernel path from `open("foo.txt")` to reading from an ext4 inode
- [ ] Study ext4 journaling: JBD2, ordered mode (default), crash consistency
- [ ] Explain why ordered mode prevents metadata-data inconsistency
- [ ] Study TCP/IP kernel path: `send()` → sk_buff → TCP → IP → NIC ring buffer → DMA
- [ ] Describe the 5-hop sk_buff journey from `write()` syscall to network driver
- [ ] Lab: write Go program that reads `/proc/self/maps` and prints memory regions
- [ ] Correctly identify heap, stack, mmap'd regions, and vDSO from `/proc/self/maps`

### Go: Core + Concurrency + Networking (Weeks 2–7, ~80 hrs)

**Language core**
- [ ] Complete tour.golang.org in one sitting
- [ ] Read go.dev/doc/effective_go
- [ ] Write 10 small concurrent programs using goroutines + channels before moving on
- [ ] Implement concurrent pipeline (producer → transform → consumer) using only channels

**Scheduler + Memory Model**
- [ ] Study Go G/M/P scheduler model, work stealing, goroutine stack copying
- [ ] Explain what happens when a goroutine calls a blocking syscall (M detached, new M spawned)
- [ ] Read Go Memory Model spec at go.dev/ref/mem
- [ ] Build thread-safe LRU cache using `sync.RWMutex` — passes `go test -race`
- [ ] Build lock-free counter using `atomic.AddInt64` — passes `go test -race`

**Advanced Go**
- [ ] Study `sync.Pool`, run `go build -gcflags='-m'` on proxy — find and eliminate ≥1 heap escape
- [ ] Add context cancellation to proxy — backend requests cancel when client disconnects
- [ ] Implement generic LRU cache `LRU[K comparable, V any]` using Go 1.18+ generics

**★ Flagship: HTTP Reverse Proxy**
- [ ] Implement from scratch (no `httputil.ReverseProxy`)
- [ ] Round-robin load balancer with health checks
- [ ] Token bucket rate limiter
- [ ] Graceful shutdown on SIGTERM
- [ ] Structured JSON logs with trace IDs
- [ ] Prometheus metrics: p50/p95/p99 histogram
- [ ] Benchmark with `wrk -t12 -c400 -d30s`
- [ ] Profile with pprof — find and fix one bottleneck
- [ ] Push to GitHub: architecture diagram, benchmark numbers, pprof flame graph before/after, design doc

### PostgreSQL: Storage Engine + MVCC + Indexes (Weeks 1–8, Fridays, ~24 hrs)

- [ ] Install `pageinspect` extension
- [ ] Read Rogov Ch. 1–2 (heap file layout: pages, tuples, item pointers)
- [ ] INSERT 3 rows, inspect the page with pageinspect — see raw byte layout
- [ ] Show xmin/xmax fields using pageinspect
- [ ] Study MVCC: xmin/xmax, tuple versions, snapshot visibility
- [ ] Demonstrate with pageinspect that UPDATE creates new tuple rather than modifying in-place
- [ ] Study B-tree index: splits, fill factor, covering indexes
- [ ] Explain when Index Only Scan is used vs Index Scan and what the visibility map enables
- [ ] Run `EXPLAIN (ANALYZE, BUFFERS)` on 5 queries of increasing complexity
- [ ] Identify every node type: Seq Scan, Index Scan, Bitmap Heap Scan, Hash Join, Merge Join, Nested Loop
- [ ] Diagnose a slow query from EXPLAIN output in under 2 minutes
- [ ] Study isolation levels — open 2 psql sessions and demonstrate:
  - [ ] Non-repeatable read at Read Committed
  - [ ] Write skew at Repeatable Read
  - [ ] Serializable prevents write skew
- [ ] Read Berenson et al. "A Critique of ANSI SQL Isolation Levels"
- [ ] Study WAL: write-ahead logging, checkpoint, crash recovery (Rogov Ch. 9)
- [ ] Explain checkpoint-to-crash recovery sequence step by step
- [ ] Study PostgreSQL buffer manager: shared_buffers, clock-sweep eviction
- [ ] Use `pg_buffercache` to identify hottest relations in buffer pool
- [ ] Study autovacuum: dead tuple threshold formula, bloat, TOAST
- [ ] Lab: INSERT 100k rows, DELETE 80k, check `pg_stat_user_tables.n_dead_tup`, wait for autovacuum

**Phase 1 Gate**
- [ ] Write concurrent Go with zero races under `-race`
- [ ] Read EXPLAIN ANALYZE and identify bottleneck node
- [ ] Explain false sharing, TLB, and what happens when a goroutine blocks on a syscall
- [ ] HTTP proxy on GitHub with benchmarks and pprof flame graph
- [ ] Reproduce write skew and explain why Serializable prevents it

---

## Phase 2: C++ Systems Programming · Java JVM (Months 3–5, ~360 hrs)

### C++ Language Core + Memory Model (Weeks 9–11, ~50 hrs)

- [ ] Read Stroustrup "A Tour of C++" Ch. 1–5
- [ ] Explain RAII with concrete example (file handle, mutex lock) without notes
- [ ] Study `unique_ptr`, `shared_ptr`, `weak_ptr` — never use `new`/`delete` directly
- [ ] Explain when `shared_ptr` thread safety is insufficient and why `weak_ptr` breaks cycles
- [ ] Read Effective Modern C++ Ch. 1–5 (move semantics) + Ch. 7 (concurrency)
- [ ] Implement a move-only type (unique resource handle) correctly
- [ ] Watch Herb Sutter "atomic Weapons" CppCon talk (both parts)
- [ ] Implement spinlock using acquire/release atomics — explain why seq_cst is over-specified
- [ ] Enable `-fsanitize=address,undefined` in CMakeLists — every project must pass under both
- [ ] Explain one case where UB causes the compiler to optimize away a security check
- [ ] Study templates + CRTP: implement CRTP type hierarchy, verify calls inlined on godbolt.org
- [ ] Study C++20 concepts: add `requires` constraints to allocator template parameters
- [ ] Study `mmap` vs `read()`: benchmark random 4KB reads from 1GB file — document when each wins
- [ ] Study `std::span` + `std::string_view` — refactor SSTable reader to accept `std::span<const std::byte>`
- [ ] Study C++20 coroutines: implement `Generator<int> fibonacci()` using `co_yield`
- [ ] Study Ranges: implement compaction merge as a ranges-based k-way merge

### ★ C++ Flagship 1: Thread-Safe Memory Pool Allocator (Weeks 11–14, ~70 hrs)

- [ ] Write design doc in `/docs/design.md` — ADR for each of 4 decisions:
  - [ ] How many size classes?
  - [ ] Thread-local caches vs global pool tradeoff
  - [ ] Thread-local cache refill strategy
  - [ ] What happens when cache is full on `Put()`?
- [ ] Implement global free list with `std::mutex` (baseline)
- [ ] Write unit tests with Google Test
- [ ] Benchmark vs `std::malloc` with Google Benchmark — document baseline numbers
- [ ] Verify ASAN/UBSAN clean from day one
- [ ] Add thread-local caches: local pop (no lock), batch refill from global pool
- [ ] Benchmark vs mutex-only version at 8 threads — target >3x throughput improvement
- [ ] Replace mutex global pool with lock-free CAS stack using `std::atomic`
- [ ] Use `memory_order_acq_rel` for CAS, `memory_order_acquire` for loads
- [ ] Implement ABA protection via tagged pointers
- [ ] Benchmark before/after CAS optimization
- [ ] Write postmortem README:
  - [ ] Architecture diagram of allocator layers
  - [ ] Google Benchmark results at 1/2/4/8/16 threads
  - [ ] "What I got wrong" section — every bug found via ASAN
  - [ ] Comparison to TCMalloc design
  - [ ] What to add next (object pooling, size classes, hugepage backing)

### ★ C++ Flagship 2: Lock-Free MPSC Queue (Weeks 15–17, ~60 hrs)

- [ ] Read Michael-Scott lock-free queue paper (1996) — 6 pages, free PDF
- [ ] Whiteboard M-S queue enqueue and dequeue from memory
- [ ] Implement MPSC queue: producers CAS on tail, consumer reads head without CAS
- [ ] Test with 8 producer threads + 1 consumer under ASAN
- [ ] Verify: no dropped items under stress test (8 producers × 1M items each)
- [ ] Read hazard pointers paper (Michael 2004)
- [ ] Implement hazard pointer memory reclamation
- [ ] Stress test with frequent reclamation passes under valgrind — zero use-after-free
- [ ] Implement mutex-protected queue as baseline
- [ ] Benchmark: lock-free MPSC vs mutex queue vs Go channel at 1/2/4/8/16 producers
- [ ] Document where each implementation wins/loses and why
- [ ] Write README with benchmark results table

### Java: JVM Runtime + Concurrency + Wallet (Weeks 13–20, ~90 hrs)

**JVM Internals**
- [ ] Study G1GC: region-based, concurrent marking, stop-the-world compaction, safepoints
- [ ] Study ZGC: concurrent relocation via load barriers
- [ ] Write one-page GC comparison: Go GC vs G1GC vs ZGC (design tradeoffs, pause models)
- [ ] Read JCIP (Java Concurrency in Practice) Ch. 1–5 + Ch. 10–12
- [ ] Read 5 JVM Anatomy Quarks posts (Shipilev)
- [ ] Study Java Memory Model JSR-133: happens-before, volatile, synchronized
- [ ] Write three-way comparison table: Java volatile vs Go atomic vs C++ relaxed/acquire/release
- [ ] Study JIT tiered compilation (C1/C2), inlining, deoptimization
- [ ] Lab: use `-XX:+PrintCompilation` and `-XX:+PrintInlining` on wallet hot paths
- [ ] Study Java 21 virtual threads: carrier threads, pinning hazards
- [ ] Benchmark wallet: virtual threads vs platform threads at 10k concurrent requests

**Spring Architecture**
- [ ] Study `@Transactional` AOP proxy: why same-class calls fail, `REQUIRES_NEW` behavior
- [ ] Study hexagonal architecture: ports, adapters, domain module
- [ ] Set up Maven multi-module project with ArchUnit enforcing no Spring imports in domain
- [ ] Verify ArchUnit test catches Spring import in domain module and fails the build

**★ Flagship: Digital Wallet & Ledger**
- [ ] Implement double-entry bookkeeping with invariant tests
- [ ] Add idempotency keys with UNIQUE constraint
- [ ] Benchmark pessimistic vs optimistic locking with pgbench — document results
- [ ] Implement Outbox pattern with Go poller
- [ ] Add Flyway migrations
- [ ] Add structured JSON logging with correlation IDs
- [ ] Add Prometheus metrics
- [ ] Run failure tests:
  - [ ] DB crash mid-transaction
  - [ ] Duplicate request
  - [ ] App crash mid-outbox processing
- [ ] Benchmark with JMH: optimistic vs pessimistic locking at 1/2/4/8 threads
- [ ] All failure tests pass — document results in GitHub repo with ADRs

**Phase 2 Gate**
- [ ] C++ allocator benchmarks documented at 1/4/8/16 threads, ASAN/UBSAN clean
- [ ] Lock-free MPSC queue passes stress test under ASAN
- [ ] Wallet failure tests pass, pgbench results documented
- [ ] Can explain RAII, move semantics, `std::atomic` memory orderings, G1GC safepoints, JMM happens-before without notes

---

## Phase 3: Raft · LSM Tree · Distributed Systems (Months 6–9, ~480 hrs)

### ★ Raft Consensus in Go (Months 6–7, ~160 hrs)

- [ ] Read Raft paper (Ongaro & Ousterhout 2014) — read twice
- [ ] Explain the leader completeness property without notes
- [ ] **Lab 2A: Leader Election**
  - [ ] Randomized election timeout (150–300ms)
  - [ ] `RequestVote` RPC with term comparison and log-up-to-date check
  - [ ] Vote counting with majority quorum
  - [ ] Term update on receiving higher term
  - [ ] Lab 2A passes 50 consecutive runs
- [ ] **Lab 2B: Log Replication**
  - [ ] `AppendEntries` RPC with previous log index/term consistency check
  - [ ] Commit index advances when majority replicated
  - [ ] Follower divergent entries overwritten via nextIndex backtracking
  - [ ] Lab 2B passes — whiteboard nextIndex/matchIndex update protocol
- [ ] **Lab 2C: Persistence**
  - [ ] Persist `currentTerm`, `votedFor`, log entries before responding to RPCs
  - [ ] Lab 2C passes — crash-recovery scenarios all pass
- [ ] **Lab 2D: Snapshots**
  - [ ] Leader sends snapshot to fallen-behind followers
  - [ ] Log compaction implemented
  - [ ] Lab 2D passes
- [ ] Write postmortem README with ≥4 documented bugs: symptom, test failure, root cause, lesson
- [ ] Pin as featured project on GitHub profile

### Distributed Systems Theory (Month 7, ~60 hrs)

- [ ] Read Lamport "Time, Clocks, and the Ordering of Events" (1978)
- [ ] Implement vector clocks in Go — test correctly identifies concurrent vs causally ordered events
- [ ] Read Dynamo paper (Amazon 2007) — consistent hashing + vector clock design
- [ ] Implement consistent hashing ring in Go: `ring.AddNode(id, tokens)`, `ring.GetNode(key)`
- [ ] Verify: adding 1 node to 5-node ring remaps ≈17% of keys (not 80%+)
- [ ] Verify: virtual nodes reduce load imbalance to <5% across nodes
- [ ] Study 2PC: coordinator, cohorts, blocking failure — explain why coordinator crash blocks cohorts
- [ ] Explain why replacing 2PC coordinator with Raft group solves the blocking problem
- [ ] Read FLP impossibility paper (Fischer, Lynch, Paterson 1985)
- [ ] Explain what assumption Raft violates to escape FLP

### ★ C++ Flagship 3: LSM-Tree Key-Value Store (Months 8–9, ~160 hrs)

- [ ] Read LSM tree paper (O'Neil 1996)
- [ ] Read LevelDB design document
- [ ] Draw LSM write path (WAL → MemTable → L0 SSTable → compaction) from memory

**WAL + MemTable**
- [ ] Implement append-only WAL file
- [ ] Implement MemTable backed by skip list
- [ ] `Put(key, value)`: append to WAL, insert into skip list
- [ ] WAL crash recovery test: write 1000 entries, kill process, restart, verify all readable

**SSTable**
- [ ] Implement SSTable flush: sorted key-value pairs + index block at end
- [ ] Implement `Get(key)`: check MemTable first, then SSTables newest-to-oldest
- [ ] 100k Put / Get correctness test passes under ASAN

**Bloom Filter**
- [ ] Implement Bloom filter with 2 hash functions, tuned for 1% false positive rate
- [ ] Benchmark `Get()` on absent keys before/after — target >3x speedup

**Leveled Compaction**
- [ ] Implement compaction thread: triggers when L0 exceeds 4 files
- [ ] Merge + remove deleted keys (tombstones)
- [ ] After 1M writes: Get() latency stays within 2x of fresh-start latency
- [ ] Disk usage stays bounded

**Block Cache**
- [ ] Implement sharded LRU block cache (N shards to reduce lock contention)
- [ ] Use Phase 2 allocator as backing memory
- [ ] Benchmark with Zipf workload — cache hit rate >75% after warmup
- [ ] Verify >10x read throughput improvement for hot keys

**Iterator + Range Scans**
- [ ] Implement iterator interface: `Seek(key)`, `Next()`, `Valid()`, `Key()`, `Value()`
- [ ] Implement iterators for MemTable, SSTable, and MergingIterator
- [ ] Range scan test: `Scan(start, end)` returns all keys in range spanning MemTable + multiple SSTable levels

### Distributed Patterns + PostgreSQL Advanced (Months 7–9, ~100 hrs)

**Saga Pattern**
- [ ] Extend wallet into booking system with choreography-based saga
- [ ] Inject failures at each saga step
- [ ] Verify: all 3 failure scenarios (fail at step 1, 2, 3) result in clean compensation
- [ ] 0 resource leaks across 10k operations

**Event Sourcing + CQRS**
- [ ] Implement event sourcing with PostgreSQL as event store
- [ ] Implement CQRS: separate write model (commands → events) from read model (projections)
- [ ] Event replay produces identical state to direct query
- [ ] Snapshot reduces replay time by >90% for long streams

**PostgreSQL Advanced**
- [ ] Study streaming replication: WAL shipping, replication slots
- [ ] Lab: set up streaming replication, verify WAL shipping to standby
- [ ] Partition wallet ledger by month
- [ ] Verify `EXPLAIN` shows `Partitions: filtered` for date-range queries (partition pruning)
- [ ] Enable `pg_stat_statements`
- [ ] Find top-5 slowest queries from wallet workload
- [ ] Fix each with partial index, covering index, or query rewrite
- [ ] Document before/after EXPLAIN for each fix
- [ ] Configure PgBouncer in transaction mode — verify Spring works correctly

**Phase 3 Gate**
- [ ] Raft labs 2A–2D all pass with documented bugs
- [ ] LSM tree handles 1M writes with bounded read latency and disk usage
- [ ] Saga compensation passes all failure injection scenarios
- [ ] pg_stat_statements query fixes documented
- [ ] Can explain write amplification, leader completeness property, SSI predicate locking without notes

---

## Phase 4: Capstone · OSS · Interview Readiness (Months 10–12, ~360 hrs)

### Linux Observability: eBPF · io_uring · SIMD (Month 10, ~40 hrs)

- [ ] Install bpftrace and BCC tools
- [ ] Run `bpftrace -e 'tracepoint:syscalls:sys_enter_read { @[comm] = count(); }'`
- [ ] Trace block cache miss rate in running LSM process using bpftrace uprobes (no recompilation)
- [ ] Generate CPU flame graph with `perf record -F 99 -g` + flamegraph.pl
- [ ] Introduce artificial lock contention in C++ allocator
- [ ] Use `offcputime-bpfcc` off-CPU analysis to identify contention hotspot
- [ ] Implement io_uring file reader in C++ using liburing
- [ ] Benchmark io_uring vs `read()` at queue depths 1, 32, 128 — document IOPS and p99 latency
- [ ] Benchmark AVX2-vectorized sum vs scalar on 1M-element array
- [ ] Verify AVX2 vectorization on godbolt.org (ymm registers visible in assembly)

### ★ Capstone: Distributed Metrics & KV Backend (Months 10–11, ~240 hrs)

**Design**
- [ ] Write 4 ADRs (one per component) justifying language choice before any code
  - [ ] Go ingestion: why Go for high-throughput I/O
  - [ ] C++ aggregation engine: why C++ for zero-overhead + SIMD
  - [ ] Java/Spring query API: why Java for rich ecosystem
  - [ ] TimescaleDB: why time-series storage

**Go gRPC Collector**
- [ ] gRPC server with streaming RPCs
- [ ] Interceptors: rate limiting + auth + logging
- [ ] MPSC ingestion buffer between gRPC handlers and C++ engine
- [ ] Backpressure: flow control when aggregation engine is full
- [ ] Target: 50k metrics/sec single-instance sustained
- [ ] pprof shows no obvious hotspot

**C++ Aggregation Engine**
- [ ] In-memory ring buffer per metric
- [ ] t-digest for p50/p95/p99 accuracy within 1% vs exact computation
- [ ] Flush aggregated stats to TimescaleDB every 10 seconds
- [ ] Use Phase 2 allocator for t-digest centroid allocation
- [ ] Benchmark: 1M metrics/sec single-threaded
- [ ] Profile with perf — fix top bottleneck, document before/after

**Deployment**
- [ ] Write Helm chart for all 4 components
- [ ] HPA on Go collector (scale on CPU)
- [ ] Grafana dashboard: ingestion rate, p99 latency, queue depth, Java GC metrics
- [ ] Liveness and readiness probes on all services
- [ ] Load test at 100k metrics/sec for 10 minutes — find and fix first bottleneck

### System Design Prep + Portfolio Polish + OSS (Month 12, ~80 hrs)

**System Design (2 sessions/week, 45 min each)**
- [ ] Practice 7-stage framework: requirements → capacity → API → data model → components → failure modes → scale
- [ ] Design: Rate Limiter
- [ ] Design: Distributed Cache
- [ ] Design: Message Queue
- [ ] Design: Payment System (you built this — defend every decision)
- [ ] Design: Time-Series DB (you built this — defend every decision)
- [ ] Design: Distributed KV Store (you built this — explain how it differs from LSM implementation)
- [ ] Design: URL Shortener
- [ ] Design: Notification Service
- [ ] Can complete any of the 8 systems in 45 minutes hitting all 7 stages

**OSS Contribution**
- [ ] Pick one: `pgx` (Go PostgreSQL driver), `River` (Go job queue), `RocksDB` (C++ LSM), or Spring Data JPA
- [ ] Read the codebase for 2 weeks
- [ ] Find an open issue (bug with reproducible test or documented missing feature)
- [ ] Submit PR — merged or seriously reviewed
- [ ] Link PR in portfolio README

**Portfolio Polish**
- [ ] Each flagship repo has:
  - [ ] Architecture diagram (draw.io PNG)
  - [ ] README: problem statement + design decisions + "What I'd do differently" + `docker-compose up`
  - [ ] CI badge (GitHub Actions)
  - [ ] ADR folder
- [ ] Create master index repo: one-line description, tech stack, problem demonstrated for each project
- [ ] Stranger can clone any repo and run it in under 5 minutes

**Behavioral Prep (STAR format)**
- [ ] Write STAR story: most complex bug debugged (Raft bug with root-cause analysis + numbers)
- [ ] Write STAR story: performance optimization (allocator benchmarks with before/after numbers)
- [ ] Write STAR story: technical decision under uncertainty (LSM vs B-tree ADR)
- [ ] Write STAR story: designed for scale (capstone 100k metrics/sec)

**Interview Readiness Gate**
- [ ] Can walk through any of the 5 flagships and defend every decision including 10x scale changes
- [ ] Can design a distributed KV store in 45 minutes and explain how it differs from your LSM
- [ ] Can explain write barriers in G1GC, acquire/release in `std::atomic`, leader completeness in Raft — without notes
- [ ] GitHub has 5 flagships with benchmarks, failure tests, and ADRs

---

## Phase 5: HFT Specialization (Optional — Months 13–15, ~180 hrs)

> Target firms: Citadel Securities, Jump Trading, HRT, Virtu, IMC, Optiver, Two Sigma
> Jane Street additionally requires OCaml + probability/expected value prep

### Nanosecond-Level Profiling (Weeks 1–2, ~25 hrs)

- [ ] Study `rdtsc` instruction — serialization with `lfence; rdtsc; lfence`
- [ ] Benchmark L1/L2/L3 cache latency using rdtsc — verify numbers match published tables for your CPU
- [ ] Study PMU hardware counters: cycles, instructions (→ IPC), cache-misses, branch-misses
- [ ] Run `perf stat -e cycles,instructions,cache-misses,branch-misses ./aggregation_engine`
- [ ] Identify whether aggregation engine is compute-bound, memory-bound, or branch-bound
- [ ] Integrate HdrHistogram C++ library into order book
- [ ] Record p50/p99/p99.9/max latency in nanoseconds for order insertion
- [ ] Compile order book with PGO (`-fprofile-generate` → run workload → `-fprofile-use`)
- [ ] Apply `[[likely]]`/`[[unlikely]]` to error handling branches in hot path

### NUMA + CPU Affinity (Weeks 2–3, ~25 hrs)

- [ ] Run `numactl --hardware` — understand your machine's NUMA topology
- [ ] Benchmark pointer-chasing on local vs remote NUMA node — document ≥1.5x latency difference
- [ ] Implement CPU-pinned thread pool with `sched_setaffinity`
- [ ] Allocate hot data structures with `numa_alloc_onnode(size, node)`
- [ ] Boot with `isolcpus=` kernel parameter for dedicated cores (or test in VM)
- [ ] Measure p99 latency variance: pinned+isolated vs unpinned — document >50% variance reduction
- [ ] Test hyperthreading: run order book on physical core with sibling idle vs sibling busy — measure p99.9 difference
- [ ] Allocate order book on huge pages via `madvise(ptr, size, MADV_HUGEPAGE)`
- [ ] Measure dTLB-load-misses before/after with `perf stat -e dTLB-load-misses`

### Kernel Bypass Networking (Weeks 3–5, ~35 hrs)

- [ ] Benchmark io_uring SQPOLL (`IORING_SETUP_SQPOLL`) vs standard io_uring vs `read()` at QD=1,32,128
- [ ] Document SQPOLL latency advantage at low queue depths
- [ ] Study `SO_BUSY_POLL` + interrupt coalescing (`ethtool -C`) tradeoffs
- [ ] Read DPDK architecture overview: PMD, huge pages, userspace NIC driver, RSS
- [ ] Run DPDK L2 forwarding example
- [ ] Explain DPDK packet path from NIC ring buffer to application memory (no notes)
- [ ] Write Go UDP multicast receiver — subscribe to multicast group
- [ ] Detect and log sequence number gaps in multicast stream
- [ ] Explain gap-fill recovery flow used by real exchange feeds

### ★ Lock-Free Order Book (Weeks 5–8, ~50 hrs)

- [ ] Write ADR: price level storage (tick-array vs map vs flat hash map)
- [ ] Implement tick-indexed price level array with O(1) best bid/ask pointer
- [ ] Implement FIFO queue per price level (doubly-linked, O(1) cancel)
- [ ] Implement order ID → price level map (array or `absl::flat_hash_map`)
- [ ] Allocate all order nodes from Phase 2 memory pool — zero heap allocation on hot path
- [ ] Apply `alignas(64)` to top-of-book struct — verify it fits in one cache line
- [ ] Measure cache miss rate before/after alignment fixes with `perf stat -e cache-misses`
- [ ] Download free Nasdaq ITCH 5.0 historical data
- [ ] Benchmark with ITCH replay of 1M messages using rdtsc + HdrHistogram
- [ ] Target: p50 < 150ns, p99 < 500ns, p99.9 < 2μs
- [ ] Profile with `perf record -e cycles -g` if targets not met
- [ ] Write README: architecture diagram, latency histogram chart, every optimization with before/after numbers

### Market Data Protocol Parsing (Weeks 8–10, ~25 hrs)

- [ ] Read Nasdaq ITCH 5.0 protocol specification PDF
- [ ] Implement full ITCH parser: Add/Delete/Execute/Cancel message types
- [ ] Feed parsed messages into order book from above
- [ ] Achieve >5M messages/sec parsing throughput
- [ ] Verify final order book state against reference after full ITCH replay
- [ ] Study FIX protocol: session layer (Logon, Heartbeat, ResendRequest), application layer (35=D, 35=8, 35=F)
- [ ] Implement FIX parser: scan SOH delimiter, parse tag, skip '=', parse value
- [ ] Implement SIMD-accelerated SOH delimiter search using `_mm256_cmpeq_epi8`
- [ ] Benchmark SIMD vs scalar SOH scan — verify >8x throughput improvement

### HFT Interview Prep (Weeks 10–12, ~20 hrs)

**All HFT firms**
- [ ] Answer without notes: explain ABA problem and fix in your MPSC queue
- [ ] Answer without notes: design an order book with O(1) best bid/ask
- [ ] Answer without notes: why is your allocator faster than malloc under high contention?
- [ ] Answer without notes: what is false sharing and how does it appear in a struct?

**Jane Street specific**
- [ ] Study OCaml for 4 weeks: pattern matching, immutable data, higher-order functions, type inference
- [ ] Read "Real World OCaml" (free online at dev.realworldocaml.org)
- [ ] Solve 20 OCaml programming problems
- [ ] Study probability: expected value, Markov chains, random walk
- [ ] Practice: "roll a die until 6 — expected number of rolls?" (answer: 6)
- [ ] Study market making basics: bid-ask spread, adverse selection, inventory risk

**Two Sigma SWE**
- [ ] Walk through capstone distributed metrics backend — defend every design decision under adversarial questions
- [ ] Answer: design a distributed time-series database
- [ ] Answer: explain LSM write amplification tradeoff
- [ ] Answer: how does ZGC differ from G1GC?

**HFT Readiness Gate**
- [ ] Order book benchmarks: p99 < 500ns on ITCH replay
- [ ] ITCH parser: >5M messages/sec
- [ ] Can explain NUMA topology, hyperthreading latency, DPDK kernel bypass — without notes
- [ ] All C++ projects ASAN/UBSAN clean
- [ ] Can answer "design a lock-free order book" on a whiteboard in 30 minutes

---

## Interview Depth Bank — "Why" and "What Fails"

> The questions an interviewer probes with. Answer all of these cold, without notes.
> Most are extracted from the phase tasks above; the system-design section is the gap this roadmap otherwise doesn't cover.

### OS / CS Fundamentals

- **Why is TCMalloc faster than ptmalloc under high thread contention?**
  Each thread allocates from a thread-local cache with no lock; it only touches the central heap — under a lock — to refill or drain in batches. ptmalloc has per-arena locks, but threads still contend on a bounded number of arenas. TCMalloc removes the lock from the common path and amortizes it over batches.
- **What is a store buffer and why does it break visibility on non-x86?**
  A per-core FIFO holding stores before they reach coherent cache, so the core doesn't stall on cache-coherence. Another core can't see the store until it drains. x86 (TSO) only reorders StoreLoad, so it's mostly hidden; weak models (ARM/POWER) also reorder StoreStore/LoadLoad, so without a barrier another core sees writes out of order or stale.
- **Why do two threads writing *different* variables slow each other >5x?**
  The variables share one 64-byte cache line; each write invalidates the other core's copy (MESI), forcing a coherence round-trip on every access. `alignas(64)` to separate lines removes it.
- **Why does a low-nice (high-priority) process accumulate vruntime more slowly?**
  CFS divides real runtime by the process's weight when incrementing vruntime. Higher weight → smaller vruntime step per unit of real time → it stays leftmost in the RB-tree longer → scheduled more often.
- **Why does ext4 ordered mode prevent metadata pointing at garbage?**
  It flushes data blocks to disk *before* committing the metadata that references them. After a crash, a file's block pointers can never reference blocks that were never written — which would otherwise expose another file's deleted/stale data (an integrity + security hole). It orders data; it doesn't journal it.

### Go

- **What happens to the scheduler when a goroutine makes a blocking syscall?**
  The M (OS thread) blocks in the kernel. The runtime detaches its P and hands it to another M (spawning one if needed) so remaining goroutines keep running. On return, the M tries to reacquire a P; if none is free, its goroutine is queued and the M parks.
- **Why does a value escape to the heap, and how do you see it?**
  If the compiler can't prove the value's lifetime is bounded by the stack frame — its address is returned, stored behind a pointer, captured by a closure, or passed through an interface — it must heap-allocate. `go build -gcflags='-m'` prints each decision.
- **How does a goroutine blocked on a socket read not block an OS thread?**
  The fd is non-blocking and registered with epoll. The goroutine parks and the M is freed. When epoll signals readiness, the netpoller marks the goroutine runnable and the scheduler resumes it — so millions of goroutines block on I/O with a handful of threads.

### PostgreSQL

- **When is an Index Only Scan used instead of an Index Scan, and what enables it?**
  When every column the query needs is in the index *and* the visibility map marks the pages all-visible — so Postgres skips the heap fetch it would otherwise need to check MVCC visibility. If recent writes cleared the VM bit, it falls back to visiting the heap.
- **What anomaly does each isolation level still allow?**
  Read Committed: non-repeatable reads and phantoms. Repeatable Read (snapshot in PG): prevents those but allows write skew. Serializable (SSI): detects the read/write dependency cycle behind write skew and aborts one transaction.
- **Walk the checkpoint-to-crash-recovery sequence.**
  Changes hit the WAL before the data page (write-ahead). A checkpoint flushes dirty buffers and writes a checkpoint record with a REDO pointer. After a crash, redo replays WAL from that pointer forward. No undo pass — uncommitted changes are simply invisible under MVCC because their xids never committed.
- **Why does UPDATE write a new tuple, and what's the consequence?**
  To keep the old version visible to concurrent snapshots (readers don't block writers). Consequence: dead tuples accumulate → bloat → VACUUM must reclaim them. Autovacuum and the visibility map exist to manage exactly this.

### Distributed

- **Why does a coordinator crash block the cohorts in 2PC?**
  After voting yes ("prepared"), a cohort holds its locks and can't unilaterally commit or abort without breaking atomicity — it must wait for the decision. If the coordinator dies after collecting votes but before broadcasting, cohorts are stranded holding locks.
- **Why does making the coordinator a Raft group fix that?**
  The commit decision is replicated to a majority before it's acted on, so it survives any single crash. A new leader reads the decision from the replicated log and finishes the protocol — no single node whose death strands the cohorts.
- **FLP says async consensus is impossible — why does Raft work?**
  FLP assumes full asynchrony, where a slow node is indistinguishable from a dead one. Raft assumes partial synchrony and uses timeouts / randomized election timers — a stronger model FLP doesn't cover. It can sacrifice *liveness* under pathological timing (repeated elections) but never *safety*.
- **State the leader completeness property and why it holds.**
  Once an entry is committed, it's present in every future leader's log. It holds because an entry commits only after reaching a majority, a candidate wins only with a majority, and the RequestVote up-to-date check makes voters reject any candidate whose log is behind — so any winner already has every committed entry.

### System Design — the "what fails" gap (most important for high-scale interviews)

- **Why can a read replica return a stale value, and when does it matter?**
  It applies WAL asynchronously, lagging the primary by ms–s. A user who just wrote (e.g., debited balance) may read the pre-write value — a read-your-writes violation. Fix: route a recently-writing user's reads to the primary, or carry a causal/session token.
- **What fails if two identical requests race on an idempotency key?**
  With a non-atomic check-then-insert, both see "absent" and both execute the side effect — double charge. Fix: a UNIQUE constraint or `INSERT ... ON CONFLICT`, making the key itself the concurrency-control point.
- **A saga isn't atomic — what does that mean for correctness?**
  Each step commits independently; there's no global rollback, only compensation. Between a failure and its compensation the system is valid-per-service but globally inconsistent (money debited, booking not yet made). You must model that intermediate state explicitly (a `pending` status) — acceptable only if the business tolerates eventual consistency.
- **What happens to in-flight limits when a rate-limiter node dies?**
  With node-local counters, its quota share is lost and clients rerouted elsewhere get a fresh bucket — the global limit is briefly exceeded. Fix: centralize counters (Redis) or accept approximate limiting; it's an accuracy vs latency/availability trade.

---

## Reading Guide — Chapter-by-Chapter with Self-Checks

> **Rule for every chapter/paper:** finish it, close the book, answer the checks out loud without notes.
> Can't answer → reread that chapter before moving on. A checkbox means "passed the checks," not "eyes saw the pages."

### OSTEP — ostep.org (free)

**Phase 1: Virtualization/Memory (Ch. 13–23)**
- [ ] **Ch. 13 — Address Spaces.** Check: state the three goals of virtualizing memory (transparency, efficiency, protection). Draw a process address space with stack/heap growth directions — this is the Phase 1 task.
- [ ] **Ch. 14 — Memory API.** Check: name three classic malloc bugs (buffer overflow, use-after-free, leak) and which tool catches each. Why is `free()` given no size argument — where does the size live?
- [ ] **Ch. 15 — Address Translation.** Check: how does base-and-bounds translation work and what hardware does it require? Why is it insufficient for real programs (no sparse address spaces, internal waste)?
- [ ] **Ch. 16 — Segmentation.** Check: how do segment base/bounds pairs enable a sparse address space? What is external fragmentation and why does segmentation cause it?
- [ ] **Ch. 17 — Free-Space Management.** Check: explain splitting and coalescing. Best-fit vs first-fit tradeoffs? How do segregated lists / slab allocation sidestep fragmentation? (Feeds directly into `memory-allocators.md`.)
- [ ] **Ch. 18 — Paging.** Check: translate a virtual address by hand (split VPN/offset, index page table). Why does a linear page table for a 32-bit space with 4KB pages cost ~4MB *per process*?
- [ ] **Ch. 19 — TLBs.** Check: walk a TLB miss end-to-end (hardware-managed vs OS-managed). What happens to the TLB on context switch, and how do ASIDs avoid a full flush? Why does row-major vs column-major array traversal change performance?
- [ ] **Ch. 20 — Smaller Tables.** Check: how does a multi-level page table save memory and what does it cost on a TLB miss? x86-64 uses a 4-level walk — what does that imply about TLB-miss latency?
- [ ] **Ch. 21 — Swapping: Mechanisms.** Check: narrate a page fault from present-bit trap to instruction retry. Why is the page fault handler always software even with a hardware-walked TLB?
- [ ] **Ch. 22 — Swapping: Policies.** Check: why is exact LRU too expensive to implement? Explain the clock algorithm. Define thrashing and what the OS can do about it.
- [ ] **Ch. 23 — VAX/VMS Case Study.** Check: name two VMS ideas that survive in Linux today (e.g., second-chance FIFO lists, demand-zero pages, kernel mapped into every address space).

**Phase 2: Concurrency (Ch. 26–32)**
- [ ] **Ch. 26 — Concurrency Intro.** Check: show why `counter++` is not atomic at the instruction level. Define race condition vs data race.
- [ ] **Ch. 28 — Locks.** Check: compare test-and-set, compare-and-swap, fetch-and-add as lock primitives. When is a spinlock the right choice vs a blocking lock?
- [ ] **Ch. 29 — Lock-Based Data Structures.** Check: what is lock coupling (hand-over-hand)? Why does a sloppy/approximate counter scale where a single-lock counter doesn't? (Same idea as your sharded LRU cache.)
- [ ] **Ch. 30 — Condition Variables.** Check: why must `wait()` be called in a `while` loop, not `if`? What is a spurious wakeup? Producer/consumer with two CVs — why two?
- [ ] **Ch. 31 — Semaphores.** Check: implement a lock and a CV-equivalent with semaphores. What initial value means what?
- [ ] **Ch. 32 — Concurrency Bugs.** Check: atomicity violation vs order violation with an example of each. State the four conditions for deadlock and which one lock ordering breaks.

### What Every Programmer Should Know About Memory — Drepper 2007 (free PDF)

> Read §3, §4, §6 carefully; skim §2 and §5 (§5 becomes required in Phase 5/NUMA).
- [ ] **§3 — CPU Caches.** Check: define set associativity and compute which set an address maps to. Write-back vs write-through? Explain cache line bouncing between cores — connect to your false-sharing benchmark.
- [ ] **§4 — Virtual Memory.** Check: what does a 4-level page walk cost, and how do hugepages reduce TLB pressure? (Connect to `perf stat -e dTLB-load-misses`.)
- [ ] **§6 — What Programmers Can Do.** Check: why does sequential access beat random access even when everything fits in RAM (prefetcher)? Give two data-layout changes that improve cache use (AoS→SoA, padding to line size).

### 100 Go Mistakes and How to Avoid Them — Harsanyi (Ch. 1–9)

- [ ] **Ch. 2 — Code/Project Organization.** Check: when is an interface pollution (define interfaces on the consumer side, not producer)? Why does returning an interface hurt?
- [ ] **Ch. 3 — Data Types.** Check: slice length vs capacity — show how re-slicing a large slice leaks memory. What does `copy` require that assignment doesn't?
- [ ] **Ch. 4 — Control Structures.** Check: what does `for range` copy on each iteration? The classic goroutine-captures-loop-variable bug — why does it happen and how is it fixed (pre-1.22 vs 1.22+)?
- [ ] **Ch. 5 — Strings.** Check: iterating a string yields bytes or runes — when? Why can `len(s)` disagree with character count? Why is repeated `+=` concatenation O(n²) and what replaces it?
- [ ] **Ch. 6 — Functions & Methods.** Check: value vs pointer receiver — when does it matter for mutation and for interface satisfaction? What does `defer` evaluate immediately vs at return? The defer-in-loop resource leak.
- [ ] **Ch. 7 — Error Management.** Check: `%w` vs `%v` in `fmt.Errorf` — what do `errors.Is`/`errors.As` need? Why panic only for programmer errors?
- [ ] **Ch. 8 — Concurrency: Foundations.** Check: data race vs race condition in Go terms. Why is a buffered channel of size 1 not a mutex? What does `context.Context` propagate and when must you check `ctx.Done()`?
- [ ] **Ch. 9 — Concurrency: Practice.** Check: three ways to leak a goroutine (blocked send on unread channel, forgotten receiver, missing cancellation) and the fix for each. When does `sync.Pool` help and when does it hurt?

### PostgreSQL 14 Internals — Rogov (free at postgrespro.com)

- [ ] **Ch. 1 — Introduction.** Check: sketch the process architecture — postmaster, backend per connection, checkpointer, WAL writer, autovacuum workers. Where does shared memory sit?
- [ ] **Part I — Isolation & MVCC (Ch. 2–8).**
  - [ ] Isolation chapters — Check: which anomaly does each PG level allow (map to your two-psql-sessions labs)? Why is PG's Read Uncommitted actually Read Committed?
  - [ ] Pages & tuples — Check: what's in a page header, an item pointer (line pointer), a tuple header (xmin, xmax, ctid)? How large before TOAST kicks in?
  - [ ] Snapshots — Check: what three things define a snapshot (xmin, xmax, active xid list) and how is tuple visibility decided from them?
  - [ ] HOT updates & page pruning — Check: what two conditions allow a HOT update, and why does it avoid index bloat?
  - [ ] Vacuum & autovacuum — Check: write the autovacuum trigger formula (threshold + scale_factor × reltuples). What does vacuum reclaim vs what does it just mark?
  - [ ] Freezing — Check: why does xid wraparound exist (32-bit xids) and what would happen without freezing?
- [ ] **Part II — Buffer Cache & WAL (Ch. 9–11).**
  - [ ] Buffer cache — Check: walk clock-sweep eviction with usage counts. Why does a Seq Scan use a ring buffer instead of flooding shared_buffers?
  - [ ] WAL — Check: what is an LSN? Why must WAL flush *before* the dirty page (the actual write-ahead rule)? What are full-page writes and why after each checkpoint?
  - [ ] Checkpoints — Check: narrate crash recovery from the REDO pointer (your Depth Bank answer, now with LSN detail).
- [ ] **Part III — Locks (Ch. 12–15).** Check: table-level lock modes — which conflict with what? Row locks live in tuple headers, not memory — why does that matter? What is a deadlock detection cycle in PG?
- [ ] **Part IV — Query Execution (Ch. 16–20).** Check: cost model — what do seq_page_cost/random_page_cost encode? For each join (nested loop, hash, merge): when does the planner pick it and what makes it degrade? Why do stale statistics produce bad plans (`ANALYZE`)?

### Designing Data-Intensive Applications — Kleppmann (Ch. 5, 7, 8, 9)

> Your highest-leverage book for Grab system design rounds. One chapter per week, notes in `design-data-intensive-applications/`.
- [ ] **Ch. 5 — Replication.** Check: single-leader vs multi-leader vs leaderless — one use case each. Define read-your-writes, monotonic reads, consistent prefix, and one implementation for each. How do leaderless quorums (w + r > n) still return stale data?
- [ ] **Ch. 7 — Transactions.** Check: define dirty write, read skew, write skew, phantom — with a concrete money example each. How does 2PL differ from SSI in *how* it prevents write skew (blocking vs abort)?
- [ ] **Ch. 8 — The Trouble with Distributed Systems.** Check: why can't wall-clock time order events (NTP skew, leap smearing)? What is a fencing token and what failure does it prevent (paused process with expired lock)? Why are process pauses (GC, VM migration) indistinguishable from crashes?
- [ ] **Ch. 9 — Consistency and Consensus.** Check: linearizability vs serializability — which is about single-object recency, which about multi-object transactions? Why is total order broadcast equivalent to consensus? Restate CAP precisely (during a partition: consistency or availability).

### Java Concurrency in Practice — Goetz (Ch. 1–5, 10–12)

- [ ] **Ch. 2–3 — Thread Safety & Sharing Objects.** Check: what makes a class thread-safe? Explain publication and escape — why is starting a thread in a constructor dangerous? List the safe-publication idioms (final field, volatile, lock, static initializer).
- [ ] **Ch. 4–5 — Composing Objects & Building Blocks.** Check: why is a class built from thread-safe components not automatically thread-safe (check-then-act across calls)? What do `ConcurrentHashMap`'s atomic compound ops (`computeIfAbsent`) buy you?
- [ ] **Ch. 10–11 — Liveness & Performance.** Check: show a lock-ordering deadlock and the fix. What is lock contention's real cost (context switches, cache traffic)? Lock splitting vs lock striping.
- [ ] **Ch. 12 — Testing.** Check: why do concurrency bugs hide under test (JIT, weak schedules) and what raises the odds (more threads than cores, barriers to synchronize start)?

### C++ Track (Phase 2)

- [ ] **A Tour of C++ — Stroustrup, Ch. 1–5.** Check: RAII in one sentence. What does `=delete` on copy operations express? Value vs reference semantics of containers.
- [ ] **Effective Modern C++ — Meyers, Ch. 1 + 5 + 7.**
  - [ ] Ch. 5 (move semantics, items 23–30) — Check: why does `std::move` move nothing? Universal (forwarding) reference vs rvalue reference — how does `T&&` differ in a template? When does perfect forwarding fail? Why can moving disable RVO?
  - [ ] Ch. 7 (concurrency, items 35–40) — Check: `std::atomic` vs `volatile` — which is for concurrency, which for memory-mapped I/O? What does a joinable `std::thread` destructor do (terminate!) and how do you guard it?
- [ ] **C++ Concurrency in Action — Williams, Ch. 7.** Check: implement lock-free stack push in pseudocode with correct orderings. Where exactly does ABA bite it? Why is `compare_exchange_weak` in a loop preferred?
- [ ] **The Art of Multiprocessor Programming — Herlihy & Shavit, queue + reclamation chapters.** Check: define linearization point; identify it for MS-queue enqueue and dequeue. Why can't a lock-free structure just `free()` removed nodes?
- [ ] **Linux Kernel Development — Love, Ch. 4 + 13.** Check: how does CFS pick the next task (leftmost node) in O(log n)? What are the VFS four objects (superblock, inode, dentry, file) and what does each own?
- [ ] **BPF Performance Tools — Gregg, Ch. 1–5.** Check: kprobe vs uprobe vs tracepoint vs USDT — stability and overhead of each. Why is off-CPU analysis needed when CPU flame graphs look flat?

### Papers — each with checks

- [ ] **Raft — Ongaro & Ousterhout 2014** (read twice). Check: why randomized election timeouts (split votes)? State the Log Matching property and how AppendEntries' prev-index/term check maintains it. Figure 8: why can a leader *not* commit a previous term's entry by counting replicas — what's the rule?
- [ ] **Michael & Scott queue — 1996.** Check: why can `tail` lag behind the real last node, and how does "helping" fix it? Identify both linearization points. Why does dequeue read `head`, `tail`, *and* `next`?
- [ ] **Hazard Pointers — Michael 2004.** Check: walk the protocol — publish hazard pointer, validate, use. Why is validation (re-read after publish) mandatory? When does a retired node actually get freed?
- [ ] **LSM-Tree — O'Neil 1996.** Check: define write amplification, read amplification, space amplification — and state which one leveled compaction optimizes at the cost of which. Why do sequential writes beat random even on SSDs?
- [ ] **A Critique of ANSI SQL Isolation Levels — Berenson 1995.** Check: why were the ANSI anomaly definitions ambiguous (strict vs broad interpretation)? Define snapshot isolation and show the A5B write-skew history that proves SI ≠ serializable.
- [ ] **Time, Clocks — Lamport 1978.** Check: define happened-before. Why do Lamport clocks give `a→b ⇒ C(a)<C(b)` but not the converse — and what do vector clocks add that fixes it?
- [ ] **Dynamo — DeCandia 2007.** Check: why did Amazon choose availability over consistency for the cart? Sloppy quorum + hinted handoff — what guarantee is weakened? How do vector clocks surface conflicts and who resolves them? What are Merkle trees for?
- [ ] **FLP — Fischer, Lynch, Paterson 1985.** Check (concept-level is enough): what exact model does it assume (async, deterministic, one crash)? What does "bivalent configuration" mean intuitively? What does it *not* say (consensus usually works in practice — why)?

### Courses & Online

- [ ] **MIT 6.824** — pdos.csail.mit.edu/6.824. Watch lectures 1–8 before/alongside labs.
  - [ ] Lec 2 (RPC/threads) — Check: why does the lab use condition variables + a mutex per Raft peer?
  - [ ] Lec 3 (GFS) — Check: what consistency does GFS actually give appends, and why was that acceptable?
  - [ ] Lec 4 (Primary/Backup) — Check: why must the backup see *every* nondeterministic input?
  - [ ] Lec 6–7 (Raft) — Check: answers to all Raft paper checks above, plus: why snapshot instead of infinite log?
- [ ] **JVM Anatomy Quarks** — Shipilev, any 5 posts. Check per post: write the one-paragraph takeaway in your own words in `programming-languages/java/` notes.
- [ ] **Brendan Gregg** — brendangregg.com. Check: explain what a flame graph's x-axis is (population, *not* time) and what off-CPU flame graphs add.
- [ ] **NeetCode 150** — neetcode.io. Pattern coverage tracker for LC track.
- [ ] **Codeforces EDU** — Binary Search, Segment Tree, DSU, Flows sections.
- [ ] **Atcoder DP Contest** — 26 DP archetypes.
- [ ] **cp-algorithms.com** — reference while solving, not linear reading.
- [ ] **Competitive Programmer's Handbook** — Laaksonen. Reference alongside CF ladder, not cover-to-cover.

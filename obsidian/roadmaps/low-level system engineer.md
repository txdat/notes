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

- [ ] Read OSTEP Ch. 13-23 — full Virtualization section (Address Spaces, Address Translation, Segmentation, Free Space, Paging, TLBs, Smaller Tables, Swapping)
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

## Resources

### Books
- [ ] **OSTEP** — ostep.org (free). Read Virtualization fully, Concurrency in Phase 2.
- [ ] **What Every Programmer Should Know About Memory** — Drepper 2007. Free PDF.
- [ ] **100 Go Mistakes and How to Avoid Them** — Harsanyi. Ch. 1–9.
- [ ] **Effective Modern C++** — Scott Meyers. Ch. 1–5 (move semantics), Ch. 7 (concurrency).
- [ ] **A Tour of C++** — Stroustrup. Read before Effective Modern C++.
- [ ] **The Art of Multiprocessor Programming** — Herlihy & Shavit. Queue and memory reclamation chapters.
- [ ] **C++ Concurrency in Action** — Williams. Ch. 7 (lock-free data structures).
- [ ] **Java Concurrency in Practice** — Goetz. Ch. 1–5 + Ch. 10–12.
- [ ] **PostgreSQL 14 Internals** — Rogov. Free at postgrespro.com. Ch. 1–6, 9, 12.
- [ ] **Designing Data-Intensive Applications** — Kleppmann. Ch. 5, 7, 8, 9.
- [ ] **Competitive Programmer's Handbook** — Laaksonen. Free PDF. CF algorithm reference.
- [ ] **BPF Performance Tools** — Brendan Gregg. Ch. 1–5.
- [ ] **Linux Kernel Development** — Robert Love. Ch. 4 (scheduling), Ch. 13 (VFS).

### Papers
- [ ] In Search of an Understandable Consensus Algorithm — Ongaro & Ousterhout 2014
- [ ] Simple, Fast, Practical Non-Blocking Queue — Michael & Scott 1996
- [ ] Hazard Pointers: Safe Memory Reclamation — Michael 2004
- [ ] The Log-Structured Merge-Tree — O'Neil 1996
- [ ] A Critique of ANSI SQL Isolation Levels — Berenson et al. 1995
- [ ] Time, Clocks, and the Ordering of Events — Lamport 1978
- [ ] Dynamo: Amazon's Highly Available Key-Value Store — DeCandia et al. 2007
- [ ] FLP Impossibility — Fischer, Lynch, Paterson 1985

### Online
- [ ] **MIT 6.824** — pdos.csail.mit.edu/6.824. Labs 2A–2D with test harness.
- [ ] **NeetCode 150** — neetcode.io. Minimum viable interview problem set.
- [ ] **Codeforces EDU** — codeforces.com/edu/courses. Binary Search, Segment Tree, DSU, Flows.
- [ ] **Atcoder DP Contest** — atcoder.jp/contests/dp. 26 DP archetypes.
- [ ] **cp-algorithms.com** — E-Maxx algorithm reference in English.
- [ ] **JVM Anatomy Quarks** — Shipilev. Read any 5 posts.
- [ ] **Brendan Gregg** — brendangregg.com. Flame graphs, eBPF, off-CPU analysis.

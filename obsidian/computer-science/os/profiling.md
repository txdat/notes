# Profiling and Benchmarking

# rdtsc
- serialization: lfence; rdtsc; lfence

# PMU Hardware Counters
- cycles, instructions (→ IPC), cache-misses, branch-misses
- perf stat -e cycles,instructions,cache-misses,branch-misses

# Identifying Bottleneck
- compute-bound vs memory-bound vs branch-bound

# HdrHistogram
- p50 / p99 / p99.9 / max in nanoseconds

# Profile-Guided Optimization (PGO)
- -fprofile-generate → run workload → -fprofile-use

# Branch Hints
- [[likely]] / [[unlikely]] on error handling branches

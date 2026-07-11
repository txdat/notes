# NUMA and CPU Affinity

# NUMA Topology
- numactl --hardware

# Local vs Remote NUMA Node Latency

# CPU Pinning
- sched_setaffinity
- taskset

# numa_alloc_onnode

# Hugepages
- madvise(ptr, size, MADV_HUGEPAGE)
- dTLB-load-misses before/after

# Hyperthreading
- physical core with sibling idle vs busy
- p99.9 difference

# isolcpus kernel parameter

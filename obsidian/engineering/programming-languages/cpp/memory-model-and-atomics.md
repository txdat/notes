# C++ Memory Model and Atomics

# std::atomic

# Memory Orderings
- memory_order_relaxed
- memory_order_acquire / memory_order_release
- memory_order_acq_rel
- memory_order_seq_cst

# Spinlock
- acquire/release atomics
- why seq_cst is over-specified here

# ABA Problem
- tagged pointers as fix

# ASAN / UBSAN
- -fsanitize=address,undefined

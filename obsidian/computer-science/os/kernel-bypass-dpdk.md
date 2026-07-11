# Kernel Bypass and DPDK

# SO_BUSY_POLL + Interrupt Coalescing

# DPDK Architecture
- PMD (Poll Mode Driver)
- hugepages
- userspace NIC driver
- RSS (Receive Side Scaling)

# DPDK Packet Path
- NIC ring buffer → application memory (no kernel)

# UDP Multicast
- subscribe to multicast group
- sequence number gap detection
- gap-fill recovery flow

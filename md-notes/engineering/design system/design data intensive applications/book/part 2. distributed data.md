- distribute a database across multiple machines for scalability, fault tolerance, high availability, latency, ...
- vertical scaling/scale up: shared memory,disk,..
- horizontal scaling: shared nothing -> each machine (node) has its own cpu, memory, disk
# replication
- keeping a copy of the same data on several nodes -> redundancy -> improve performance
- difficulty of replication is handling changes to replicated data
### leaders-followers

# partitioning
- split data into subsets (partitions), and assign them to different nodes (sharding)

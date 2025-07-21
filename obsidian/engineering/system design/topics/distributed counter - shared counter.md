[systemdesign.one](https://systemdesign.one/distributed-counter-system-design/)

# high level design
- support high concurrency and write-heavy load
- high availability > consistency
### probabilistic data strucutres
- hash set -> constant time complexity at expense of increased memory usage
- redis' hyperloglog -> estimate/approximate the cardinality of set (count), and **doesnt support delete operation**

### relational database
- acquire lock (mutex) before counter is increased
- reader-writer lock can be used to reduce lock granularity and improve performance of reads
-> strong consistency
- support batch update count events from cache, it may cause delay in updating counter -> inaccurate count, fault tolerance is reduced because counter cannot be recalculated if value is not written to DB
- store each update event in a single record -> high concurrent writes (no need for locks), but require reads aggregate on entire table, and more cost of storage
- DB can be partitioned/shared (consistent hashing) or replicated (leader-followers + failover) to scale counter

#### shared counter
![[Pasted image 20250603110951.png | 600]]
- probability of lock conflicts is reduced through partitioning
- when page/... becomes more popular, userId/... can be used as key for partition
- multiple counters are initialized, updated in parallel, and final value is summed from all shards (scatter/gather) -> only optimal for **low data volume access**
- DB replication causes write congestion and poor latency. it still needs resolve conflicts

-> NOT USE

### nosql database
- apache cassandra supports partitioning using gossip protocol and consistent hashing -> high available
- disk access may be bottleneck of read performance, use cache (cache-aside pattern) can improve performance of read -> data consistency cannot be guaranteed
- counter type of cassandra (race-free) can be utilized for distributed counter
- operation complexity is high and lack of repeatability (idempotency - perform an operation multiple times -> same result)

-> NOT USE
### message queue
![[Pasted image 20250604101702.png | 600]]
- used as buffer the count update events from clients, database is asynchrnously updated at periodic intervals -> use serverless function to query and update DB (**pull model**)
- pull model increase operation complexity and may return inaccurate counter due to asynchronous update
#### lambda
![[Pasted image 20250604102805.png | 600]]
- seperate count update events (source of truth) and aggregation count (increase storage usage)
- batch processing service recompute counter accurately at periodic intervals
- the final result of counter is merged from both batch service and real-time service
- use cache to reduce load on reads -> improve performance

-> NOT USE

### redis
- high performance, throughput -> use for write-intensive distributed counter?
- use **write-behind** cache pattern (app -> cache -> DB) to persist counter for durability
- update operations must be idempotent for conflict-free synchronization, but redis' update operations are not idempotent, and non-trival

-> NOT USE

### conflict-free replicated data type (CRDT) distributed counter
- CRDT is data type that ensures data always converge to consistent state among nodes
- allows lock-free for reads and writes, and use mathematically proven rules for conflict resolution
- prevents data duplication and doesnt rely on the order of replications?
- relaxes consistency contraints, tolerates network partition (accepts writes to disconnected nodes, merges later) -> high performance/throughput, low latency for both reads and writes
- CRDT exchanges data and operations including orderding and causality
- 3 types
	- G-Counter (grow/increase only)
		- needs to know number of replicas
	- PN-Counter (positive/negative)
		- supports read-your-write (reads after write) and monotonic reads for strong consistency, and arbitrary number of replicas for high scalability
	- G-sets
	- Handoff counter
		- is eventually consistent, more stable than PN-counter

- support count synchronization with reduced storage, low latency and high performance, and converge to consistent state (eventual consistency)
- each replica stores its own counter and update operations instead of global counter -> use vector clock/version to idenify causality of operations amount replicas
- ![[Pasted image 20250604110451.png | 600]]

#### CRDT workflow
[[distributed counter]]


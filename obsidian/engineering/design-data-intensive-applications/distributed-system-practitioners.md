# basic concepts and theorems

### partitioning
- split DB into multiple smaller datasets and store them in different nodes
- vertical splitting
	- multiple tables with fewer columns
- horizontal splitting (sharding)
	- stores a percentage of rows of initial tables -> potential for loss of transaction sematics
	- range partitioning
	- hash partitioning
	- consistent hashing
		- potential of non-uniform distribution of data (imbalance)

### replication
- increase availability by copying data to other nodes (data must be maintained and kept in sync)
- pessimistic replication
	- keep replicas identical to each other
- optimistic (lazy) replication - eventually consistency
	- allow replicas diverge, and converge again if they don't receive update for a period of time

#### (single) master-slave
- 1 node is master (writable) and other nodes are slave (readable)
![[Pasted image 20260711142406.png | 600]]

#### multi-master
- prefer high availability and performance to data consistency
- all nodes are writable/readable -> conflicts
	- expose conflict resolution to clients
	- last-write-wins (local clock?) -> unexpected behaviors
	- causality tracking algorithm

#### quorums
- quorum condition
	- Vr + Vw > V
	- Vw > V/2
- why Vr > V/2 needn't?
	- Vr needn't be a majority but large enough to collide every possible write quorum

### CAP theorem
![[Pasted image 20260711151010.png | 600]]

#### PACELC theorem
- extend CAP
- in case of network partition (P), system has to choose between availability (A - AP) and consistency (C - CP), else (E) system has to choose between latency (L) and consistency (C)

### consistency / isolation

![[Pasted image 20260711161149.png | 600]]

#### consistency model
- linearizability = strong consistency
	- synchronous replication
	- operations appear to be instantaneous to external clients (subsequent reads will see the result of latest write) when thinking about a distributed system as a single node
	- writes take longer (propagate to other nodes)
	- is consistency C in CAP theorem (give up availability A in CAP)
- sequential consistency
	- no realtime guarantee
	- all operations must be seen in the same order (global order)
- causal consistency
	- only operations that are causally related need to be seen in the same order (not global order)
- eventual consistency = weak consistency
	- no guarantee for order of operations

#### isolation level
![[Pasted image 20260711215537.png | 600]]
- **anomalies**
	- dirty writes
		- a transaction overwrites a value that has previously been written by another transaction that is not committed -> violate integrity -> no rollback
	- dirty reads
		- a transaction reads a value that has been writen by another transaction that has not been committed
	- non-repeatable reads
		- a transaction reads a value twice with different values (acting on stale data)
	- phantom reads
		- a transaction does a predicate-based read (query) and another transaction updates matched items while the first transaction is running
	- lost updates
		- 2 transactions read the same value and try to update with different value
	- read skew
		- a transaction can only see partial result of another transaction
	- write skew
		- 2 transactions read the same data but modify disjoint set of data

- serializability
- repeatable read
- snapshot isolation
- read committed
- read uncommitted

# distributed transactions

### ACID of DB transaction
- Atomicity: a transaction composed of multiple operations is treated as a single unit (all or none)
- Consistency: a transaction only transitions DB from 1 valid state to another valid state, maintaining DB invariants
- Isolation: if transactions happen at a time, there is no interference between them
- Durability: once transaction is committed, it will remain committed even in the case of failure
# concensus

# time - order

# case studies and practice patterns
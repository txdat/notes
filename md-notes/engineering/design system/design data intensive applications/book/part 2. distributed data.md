- distribute a database across multiple machines for scalability, fault tolerance, high availability, latency, ...
- vertical scaling/scale up: shared memory,disk,.. -> all components are treated as a single machine
- horizontal scaling: shared nothing -> each machine (node) has its own cpu, memory, disk
### replication
- keeping a copy of the same data on several nodes -> redundancy -> improve performance
- difficulty of replication is handling changes to replicated data
### partitioning
- split data into subsets (partitions), and assign them to different nodes (sharding)

# replication
- goals
	- keep data geographically close to users (reduce latency)
	- keep system to continue working even if some of its parts are failed
	- scale out to serve more read queries
- challenges
	- handle changes to replicated data
### leaders and followers
- each node stores a copy of data (replica)
- every write operation needs to be processed by every replica -> leader based replication (active/passive, or master/slave)
![[Pasted image 20240904114233.png | 600]]
### synchronous replication
- replication is quite fast (< 1s), but no guarantee
- advantages
	- the replicas have up-to-date data (consistent with the leader)
- disadvantages
	- the write operation cannot be processed if the follower doesnt response -> semi-synchronous system (1 replica is synchronous and others are asynchronous): at least 2 nodes have up-to-date data
### asynchronous replication
- leader-based replication is configured completely asynchronous (any write hasn't been replicated can be lost) -> no data guarantee even if it has been confirmed to client
### implementation
- setting up new followers
	- to increase number of replicas or replace failed nodes
	- no consistent data for simply copying (locking data is invalid high-availability policy)
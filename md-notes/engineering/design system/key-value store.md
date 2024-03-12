- is key-value (nosql) database
# scope
- ability to store big data
- high availibility (responds quickly, even during failures) / scalability (large dataset)
- automatic scaling (based on traffic)
- low latency
- tunable consistency
# single server
- optimization:
	- data compression
	- store frequently used data in memory, the rest on disk
# multiple servers (distributed data store)
- [CAP](https://www.youtube.com/watch?v=BHqjEjzAicA)
	- consistency: all clients see same the data at the same time no matter which server is connected
	- availability: always get data even one or more servers are down
	- partition tolerance: the system continues to operate despite network partitions (disconnection between network's components)
	-> in distributed system, partitions cannot be avoided, and we have to choose between consistency and availability
		if choose cp system (eg. bank, ...):
			- reject all write operations (which cause data inconsistency)
			- return error before inconsistency is resolved (system is unavailable)
		if choose ap system:
			- accept write operations to running servers
			- sync new data to new servers after partition is resolved
# system components
### data partition
- goal:
	- distribute data across servers evenly
	- minimize data movement when adding/removing servers
	- auto scaling (add/remove nodes) based on traffic
-> using consistent hashing
### data replication
- goal:
	- data must be replicated between all servers
### consistency
- quorum - leaderless replication
	- clients send write operations to set of servers directly or through coordinators
	- 
- quorum concensus can guarantee consistency for both read and write operations
	- N: number of replicas
	- W: number of `ACK` from replicas to consider write operation is success
	- R: number of `ACK` from replicas to consider read operation is success
-> use versioning and vector locks to solve inconsistency
- versioning
	- treat each a data modification as a new immutable version of data -> need system to detect and resolve conflicts

### handling failure
- failure detection
	- require at least 2 different sources to mark server down
	- use **gossip protocol**
		- maintain a list of node membership which contains node's id and heartbeat counter
		- periodically increase its heartbeat, send its heartbeat to set of nodes and propagate to another sets
		- if a node's heartbeat doesn't increase for 1 or more periods, it is marked as offline
- handle temporary failure
	- use sloppy quorum (instead of strict quorum): select first W healthy servers to write, and first R healthy servers to read on hash ring (offline servers are ignored)
	- if a server is down, its requests will be handled by another servers temporarily, and push back when it is healthy (hinted handoff)
- handle permanent failure
	- use anti-entropy protocol to keep replicas in sync (by comparing each piece of data on replicas and updating data to newest version)
		- use **merkle tree** for inconsistency detection and minimizing amount of data transfered
			- merkle tree: each node is labeled by hash of its children's labels or values (leaf), and use dfs to compare 2 trees
### bloom filter

### etcd - Raft distributed concensus
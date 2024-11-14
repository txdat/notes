- distribute a database across multiple machines for scalability, fault tolerance, high availability, latency, ...
- vertical scaling/scale up: shared memory,disk,.. -> all components are treated as a single machine
- horizontal scaling: shared nothing -> each machine (node) has its own cpu, memory, disk
### replication
- keeping a copy of the same data on several nodes -> redundancy -> improve performance
- difficulty of replication is handling changes to replicated data
### partitioning
- split data into subsets (partitions), and assign them to different nodes (sharding)

# replication
- keeping a copy of same data on multiple machines that are connected via a network
- goals
	- keep data geographically close to users (reduce latency)
	- keep system to continue working even if some of its parts are failed
	- scale out to serve more read queries
- challenges
	- handle changes to replicated data
### leaders and followers
- each node stores a copy of data (replica)
- every write operation needs to be processed by every replica -> leader based replication (active/passive, or master/slave). replicas apply same order of writes as the leader (writes only are accepted on the leader)
![[Pasted image 20240904114233.png | 600]]
### synchronous replication
- replication is quite fast (< 1s), but no guarantee
- advantages
	- the replicas have up-to-date data (consistent with the leader)
- disadvantages
	- the write operation cannot be processed if the follower doesnt response (the leader may block all writes and wait the replica is ready again) -> semi-synchronous system (1 replica is synchronous and others are asynchronous): at least 2 nodes have up-to-date data
### asynchronous replication
- leader-based replication is configured completely asynchronous (any write hasn't been replicated can be lost) -> no data guarantee even if it has been confirmed to client
### implementation
- setting up new followers
	- to increase number of replicas or replace failed nodes
	- no consistent data for simply copying (locking data is invalid high-availability policy)
- setting up without downtime
	- take the consistent snapshot of leader without locking, write to the replicas and take changed data from since snapshot was taken from leader
- handling node outages
	- follower (catch-up recovery)
		- each follower keeps a log of the data changes from leader -> recovery from the logs before the fault occurred, and requires new data from the leader during the connection is lost
	- leader (failover)
		- one of followers is promoted as new leader, clients need to be reconfigured to the new leader, and other followers need to start consuming data changes from new leader
		- problems
			- new leader may not have full data from old leader before it failed
			- other storage systems outside of database need to be coordinated with database
			- in some scenarios, more than 1 node believe they are the leader
- replication logs
	- statement-based
		- leader logs all write requests and send to its followers
		- leader can replace any nondeterministic function calls with a return value when statement is logged (remove side effects on each replica)
	- write-ahead log
		- is an append only sequence of bytes containing all writes (using SSTables - LSM Trees) -> describe data on the low level (details of which bytes were changed), coupled to storage engine (hard to migrate)
	- logical (row-based) log
		- is a sequence of records describing writes at the granularity of a row, each log record for one row -> decouple replication logs from storage engine
			- insert: new values of all columns
			- update/delete: contains enough information to identify updated row, and values of changed/all columns
	- trigger-based
- replication lag problems
	- leader-based replication requires all writes go to a single node (primary) and reads can go to any replicas -> if read from asynchronous replica, it may return outdated data
	- read-scaling architecture realistically works with asynchronous replication
	- inconsistent state is temporary -> eventual consistency (no limit to how far replica can fall behind)
	- read-after-write consistency
		- if users reload page, they will always see any update they have made themselves (read from replica instead of leader) -> decide when reading from leader
	- monotonic reads
		- users can see things moving backward in time (greater lag): reads go to random replicas -> monotonic reads means if users make several reads in sequence, they will not see time go backward (outdated data)
		- eventualy consistency < monotonic reads < strong consistency
	- consistent prefix reads
		- it guarantees that if a sequence of writes happens in a certain order, then anyone reading those writes will see them in the same order
### multi leader replication
- use cases
	- multi datacenter
		- have a leader in each datacenter, and replicates each change to another datacenter leaders
		- same data may be concurrently modified in 2 different datacenters, -> write conflicts occur, must be resolved
		- advantages
			- writes can be processed in local leader -> inter-datacenter network delay is hidden from user
			- each datacenter operates independently from each others
			- tolerates network problems between datacenters better
![[Pasted image 20240923112014.png | 600]]
![[Pasted image 20240924165001.png | 600]]

- handling write conflicts
	- conflict avoidance
		- all writes for a particular record go through same leader
	- converging toward a consistent state
		- single leader database applies writes in sequential order
		- no defined ordering of writes, no final value -> DB must resolve the conflict in a convergent way (all replicas have same final value when all changes are replicated)
- topologies
	- > 2 leaders: circular, star, and all-to-all
	- all-to-all topology
		- incorrect order of replication messages -> version vector technique, clocks cannot be trusted in sync
![[Pasted image 20240924222102.png | 600]]

### leaderless replication
- abandon the concept of leader, allow any replica accepts writes from clients
- some database systems use the coordinator, but not enforce the order of writes
- fallover doesn't exist in leaderless replication
- to read unavailable/staled data from disconnected node, client/coordinator sends multiple requests in parallel, and can get different data -> version number is used to determine which data is new
- mechanisms to make data is up-to-date between nodes
	- read repair
	- anti-entropy (background process checks missing data and copies from another replica)
![[Pasted image 20241027225501.png | 600]]

- reading/writing quorums
- 
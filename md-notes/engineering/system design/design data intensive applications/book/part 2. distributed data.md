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
- some database systems use the coordinator, but not enforce the order of writes. different from leader replication, a leader determines the order of writes and followers apply in same order
- **fallover doesn't exist in leaderless replication** (using quorum consensus for multiple writes)
- to read unavailable/staled data from disconnected node, client/coordinator sends multiple requests in parallel, and can get different data -> version number is used to determine which data is new
- mechanisms to make data is up-to-date between nodes
	- read repair
		- send new data writes to nodes which have stale data
	- anti-entropy
		- background process checks missing data and copies from another replica
![[Pasted image 20241027225501.png | 600]]

#### reading/writing quorums
	- "if there are n replicas, every write must be confirmed by w nodes to be considered successful and must query at least r nodes for each read" -> if `w+r>n`, we expect to get an up-to-date data -> among the nodes we read, there must be at least 1 node with up-to-date data
	- common choice of w,r,n is n is odd and w, r are ceil(n/2) = majority selection. but quorums are not neccessary majorities -> sets of ndoes for read/write must overlap in at least 1 node
	- w+r > n && min(w,r) > n/2
- limitations of quorum consistency
	- if sloppy quorum is used, the w writes may end up on different nodes than the r reads -> no guarenteed overlap between write/read nodes
	- if 2 writes occur concurrently, not clear which one happened first -> merge concurrent writes
	- if a write succeeded on less than w replicas, it's not rolled back on the replicas where it succeeded -> subsequent reads may/may not return data from failed write (succeeded writes can not be rolled back)
	- if node has new value fails, its data is restored by a stale value from other replicas -> can break quorum condition
- monitoring staleness
	- there is no fixed write order -> hard to monitor the replication lag between replicas
- sloppy quorums, hinted handoff
	- leaderless replication appealing for HA and low latency system with occasional stale reads
	- sloppy quorum:
		- writes and reads still require w/r successful responses, but those may include nodes (not in n designed nodes - temporarily), and send back to home nodes when internet interruption is fixed (handoff)
		- useful for increasing write availability (write to at least w nodes), but may get stale data (write to not designed nodes)
#### concurrent writes
- some database (like dynamo) allow concurrent writes (no well-defined ordering) for same key -> conflict even if using strict quorums -> inconsistent if keeping write order
- last write wins - LWW (discarding concurrent writes)
	- only keep most recent value and allow older values to be overwriteten and discarded -> unambigously determining most recent value -> eventually converage
	- concurrent writes dont have a natural ordering -> force an arbitrary order: attach timestamp to each write
	- safe way to use LWW in database is avoiding any concurrent updates to the same key -> use UUID as key
- the "happens-before" relationship
	- 2 operations should be called concurrent if they occur at the same time. in fact, 2 operations are concurrent if they are both unaware of each other
	- each replica in replication system uses its own version number and keeps track of version numbers from other replicas -> version vector
![[Pasted image 20241222220907.png | 700]]

- algorithm
	- maintain a version number for every key, increase this key each tim it is written, and store it with new value
	- server returns all values that have not been overwritten and the latest number version
	- when client writes key, it must include prior version number and merge all received values from prior read
	- when server writes with a particular version, it overwrites all below number version data (has been merged into new value, eg. merge siblings by client) and keep all higher version data
# partitioning
- partitioning is usually combined with replication (copies of each partition are stored in multiple nodes). a node may store more than 1 partitions -> leader for some partitions and follower for others
### key-value data partition
- key range
	- `I0 <= ... < I1 | I1 <= ... < I2`
	- assign continuous range of keys to each partition
	- disadvantage:
		- certain access partern can lead to hotspot (a node is busy while other nodes arent)
- hash of key
	- `key % M`
	- a good hash function takes skewed data and makes it uniformly distributed
	- disadvantage:
		- loss ability of range query -> send range query to all nodes (in mongodb)
### secondary indexes partition
![[Pasted image 20250114110527.png | 600]]
- each partition contains its own indexes -> when updating data, only need to deal with the parition that contains its ID (local index)
- reading from document-partitioned index -> send requests to all replications `scatter/gather`
#### global secondary indexes - term partition
- must also be partitioned, updates are asynchronous
- advantages
	- make reads more efficient
- disadvantages
	- writes are slower and more complicated
### rebalancing

- fixed number of partitions (not change afterward) -> entire partitions are moving between nodes
- dynamtic partition
	- split/merge parititions automatically
	- fixed number of paritions per node (the bigger node is, the smaller partition is)
### request routing
- partitions are rebalanced, the assignment of partitions changes
![[Pasted image 20250114150931.png | 700]]
- some databases rely on coordination service (zookeeper) to track cluster metadata (type 2)
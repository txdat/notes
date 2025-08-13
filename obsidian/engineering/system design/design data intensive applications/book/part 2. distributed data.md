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
- the leader waits until all writes to replicas are success
- replication is quite fast (< 1s), but no guarantee
- advantages
	- the replicas always have up-to-date data (consistent with the leader)
- disadvantages
	- the write operation cannot be processed if the follower doesnt response (the leader may block all writes and wait the replica is ready again) -> semi-synchronous system (1 replica is synchronous and others are asynchronous): at least 2 nodes have up-to-date data
### asynchronous replication
- leader-based replication is configured completely asynchronous (any write hasn't been replicated can be lost if the leader fails) -> no data guarantee even if it has been confirmed to client
### implementation
- setting up new followers
	- to increase number of replicas or replace failed nodes
	- no consistent data for simply copying (locking data is invalid high-availability policy)
- setting up without downtime
	- take the consistent snapshot of leader without locking entire database, write to the replicas and take changed data from since snapshot was taken from leader
- handling node outages
	- follower (catch-up recovery)
		- each follower keeps a log of the data changes from leader -> recovery from the logs before the fault occurred, and requires new data from the leader during the connection is lost
	- leader (failover)
		- one of followers is promoted as new leader, **clients need to be reconfigured to the new leader**, and other followers need to start consuming data changes from new leader
		- problems
			- new leader may not have full data from old leader before it failed
			- other storage systems outside of database need to be coordinated with database
			- in some scenarios, more than 1 node believe they are the leader -> split brain (leader nodes accept writes and no process for resolving conflicts)
- replication logs
	- statement-based
		- leader logs all write requests (statements) and send to its followers
		- leader can replace any nondeterministic function calls with a return value when statement is logged (not run these functions on replica nodes to remove side effects on each replica)
	- write-ahead log
		- log is an append only sequence of bytes containing all writes (using SSTables - LSM Trees)
		- disadvantage is the log describes data on the low level (details of which bytes were changed), coupled to storage engine (hard to migrate)
	- logical (row-based) log
		- decoupled from storage engine internals -> logical only
		- is a sequence of records describing writes at the granularity of a row, each log record for one row
			- insert: new values of all columns
			- update/delete: contains enough information to identify updated row, and values of changed/all columns
	- trigger-based
- replication lag problems
	- leader-based replication requires all writes go to a single node (primary) and reads can go to any replicas -> if read from asynchronous replica, it may return outdated data
	- read-scaling architecture realistically works with asynchronous replication
	- inconsistent state is temporary -> eventual consistency (no limit to how far replica can fall behind)
	- **read-after-write consistency**
		- if users reload page, they will always see any update they have made themselves (read from replica instead of leader) -> decide when reading from leader
	- monotonic reads
		- users can see things moving backward in time (greater lag): reads go to random replicas -> monotonic reads means if users make several reads in sequence, they will not see time go backward (later read comes to greater lag replica -> outdated data)
		- eventualy consistency < monotonic reads < strong consistency
	- consistent prefix reads
		- replication lag can cause violation of causality 
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
		- single leader database applies writes in sequential order -> last write wins
		- in multi-leader, no defined ordering of writes, no final value -> DB must resolve the conflict in a convergent way (all replicas have same final value when all changes are replicated)
- topologies
	- > 2 leaders: circular, star, and all-to-all
	- all-to-all topology
		- incorrect order of replication messages (violation of causality) -> **version vector technique**, clocks cannot be trusted in sync
![[Pasted image 20240924222102.png | 600]]

### leaderless replication
- abandon the concept of leader, allow any replica accepts writes from clients
- some database systems use the coordinator, but not enforce the order of writes. different from leader replication, a leader determines the order of writes and followers apply in same order
- **failover doesn't exist in leaderless replication** (using quorum consensus for multiple writes)
- to read unavailable/staled data from disconnected node, client/coordinator sends multiple requests in parallel, and can get different data -> version number is used to determine which data is new
- mechanisms to make data is up-to-date between nodes
	- read repair
		- send new data writes to nodes which have stale data
	- anti-entropy
		- background process checks missing data and copies from another replica
![[Pasted image 20241027225501.png | 600]]

#### reading/writing quorums
- "if there are n replicas, every write must be confirmed by w nodes to be considered successful and must query at least r nodes for each read" -> if **w+r>n**, we expect to get an up-to-date data -> among the nodes we read, there must be at least 1 node with up-to-date data
	- common choice of w,r,n is n is odd and w, r are ceil(n/2) = majority selection. but quorums are not neccessary majorities -> sets of ndoes for read/write must overlap in at least 1 node
	- w+r > n && min(w,r) > n/2
	- normally, reads and writes are sent to all relicas, but client waits at least r replicas for each read and w replicas for each write
- limitations of quorum consistency
	- if sloppy quorum is used, the w writes may end up on different nodes than the r reads -> no guarenteed overlap between write/read nodes
	- if 2 writes occur concurrently, not clear which one happened first -> merge concurrent writes
	- if a write succeeded on less than w replicas (there is at least 1 replica that fails), it's not rolled back on the replicas where it succeeded -> subsequent reads may/may not return data from failed write (succeeded writes can not be rolled back)
	- if node has new value fails, its data is restored by a stale value from other replicas -> can break quorum condition
- monitoring staleness
	- there is no fixed write order -> hard to monitor the replication lag between replicas
- sloppy quorums, hinted handoff
	- leaderless replication appealing for HA and low latency system with occasional stale reads
	- sloppy quorum:
		- writes and reads still require w/r successful responses, but those may include nodes (not in n designed nodes - temporary nodes), and send back to home nodes when network interruption is fixed (hinted handoff - [[sloopy quorum - hinted handoff]])
		- useful for **increasing write availability** (write to at least w nodes), **but may get stale data** from interrupted nodes (write to not designed nodes)
#### concurrent writes
- some database (like dynamo) allow concurrent writes (no well-defined ordering) for same key -> conflict even if using strict quorums -> inconsistent if keeping write order (get value from latest write)
- last write wins - LWW (discarding concurrent writes)
	- only keep most recent value and allow older values to be overwriteten and discarded -> unambigously determining most recent value -> eventually converage
	- concurrent writes dont have a natural ordering -> force an arbitrary order: attach timestamp to each write to pick most recent = last write wins (LWW)
	- safe way to use LWW in database is avoiding any concurrent updates to the same key -> use UUID as key
- the "happens-before" relationship
	- 2 operations should be called concurrent if they occur at the same time. in fact, **2 operations are concurrent if they are both unaware of each other**
	- each replica in replication system uses its own version number and keeps track of version numbers from other replicas -> version vector
![[Pasted image 20241222220907.png | 700]]

- algorithm
	- maintain a version number for every key, increase this key each time it is written, and store it with new value
	- server returns all values that have not been overwritten and the latest number version
	- when client writes key, it must include prior version number and merge all received values from prior read
	- when server writes with a particular version, it overwrites all below number version data (has been merged into new value, eg. merge siblings by client) and keep all higher version data (data with higher version contains all data from lower versions)
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
# transactions
- group several reads and writes on multiple objects into a logical unit -> execute as one operation: succeed (commit) or fails (abort, rollback)
- transactions keep correctness guarantees
### ACID
- Atomic
	- cannot be broken down into smaller parts
	- if transaction cannot be completed (committed), the transaction is abort and DB discards any writes in transaction -> all-or-nothing guarantee
- Consistency
	- notion of database is in good state = some statements about data must be true after each transaction execution
- Isolation
	- concurrently transaction executions are isolated from each other (*serializability* in some old DBs)
	- each transaction can be pretend that it is the only one transaction running on the entire DB
- Durability
	- once a transaction has committed successfully, its results won't be forgotten (using logs?)
![[Pasted image 20250812103621.png | 600]]
### isolation levels
- in theory, isolation pretends that no concurrency is happening, serialize isolation guarantees that concurrent transactions have same effect as if they run serially (without concurrency)
- [blog1](https://dogy.io/2020/12/29/transaction-isolation-part-1/), [blog2](https://dogy.io/2021/01/01/transaction-isolation-part-2/)
- ![[Pasted image 20250812103720.png | 600]]
**exclusive lock/shared lock**
- exclusive lock
	- is held by a single transaction to write data to an object
- shared lock
	- is held by one/many transactions to read data from an object
#### read uncommitted
- non-repeatable read/read skew: read DB in temporary inconsistent state
- transaction performs in non-locking situation -> dirty reads (inconsistent data) (no lock on reading, but acquire exclusive lock on writing?)
#### read committed -> no dirty reads/writes, but not read skew
- only read data that has been commmited (no dirty read)
	- any writes by a transaction become visible when that transaction commits
- only overwrite data that has been commited (concurrent transactions try to update same object) (no dirty write)
- read committed uses a separate snapshot for each query, queries in transaction may have different results
- implementation
	- prevent dirty write by using **row-level lock** : transaction must acquire a lock on an object before updating it -> transaction must wait until previous transaction is commited/aborted (release lock)
	- prevent dirty read by storing both old commited value (returns this value to reads if any write is ongoing) and new commited value
#### snapshot isolation - repeatable read -> no dirty reads/writes, read skew, but not lost updates, write skew (race conditions)
- transaction reads from consistent snapshot of DB (only see committed data from particular point in time), single snapshot for entire transaction
- implementation
- write lock to prevent dirty writes (like read committed)
- no lock for reads, but DB keeps several committed versions of an object -> multi version concurrency control (MVCC)
- visibility rules
	- transaction id is used to decide which objects it can see
	- an object is visible if at the time a transaction started
		- the transaction that created object had committed
		- the transaction that requested object deletion had not committed 
#### serializable
- is stronger snapshot isolation, all rows are locked -> no update during transaction progress (snapshot isolation allows updating on objects that aren't used by transaction?)
### preventing lost updates - dirty writes (in concurrent writing transactions)
![[Pasted image 20250812105154.png | 500]]
- dirty write/lost update -> concurrent updates on single object
- atomic write operations
	- if atomic operation can be used, it is best choice
	- can be implemented with exclusive locking -> no read until the update (read-modify-write cycle) has been applied
- explicit locking
	- use locking from application to prevent updating object from concurrent transactions
- automatically detecting lost updates
	- atomic writes and lock force read-modify-write cycles happen sequentially
	- if DB transaction manager detects a lost update, abort transaction and retry it
- compare and set
	- allow an update to happen only if the data hasn't changed since last read
	- if read comes from snapshot/replication (stale data), this operation may not work
- conflict resolution and replication
	- lock, compare-and-set assume that there is a single update-to-date copy of data, while multi-leader/leaderless DB allow writes to happen concurrently and replicate them asynchronously -> allow conflicting versions of data and resolve them
	- last write wins (LWW) is default in many DB, but it may lost updates
### write skew, phantoms
#### skew write
- 2 concurrent transactions read from same objects but they update some of these objects (race condition), generalization of lost update
- 2 solutions
	- serializable
	- set lock to all rows that transaction depends on
#### phantom
- a write in a transaction changes result of search query in another transaction
- snapshot-isolation avoids phantom in read-only queries but not read-write transactions
#### materializing conflicts
### serializability (without serial order)
- strongest isolation level
- guarantees that the final result of parallel transactions is same as if they were executed one at a time, serially without any concurrency
#### actual serial execution
- remove the concurrency
	- every transaction must be small and fast, slow transaction can stand all transaction processing
	- use case: when entire database must be in memory (eg. cache, ) for performance issue
- in the interative style of transaction, lots of time is spent in network communication between application and DB -> DB must wait -> single-threaded DBs dont allow interactive multi-statement transactions -> stored procedure without waiting network and IO
- use partition to scale DB to multiple CPUs, nodes, ...
![[Pasted image 20250203105334.png | 600]]
#### two-phase locking (2PL)
- use locking to prevent dirty writes -> only one write transaction at any time, but with much stronger requirements
	- if transaction A has read an object and transaction B want to write -> B must wait until A commits/aborts
	- if transaction A has written an object and transaction B want to read -> B must wait until A commits/aborts
-> writers block both other readers/writers and vice versa
- 2PL performance is worse than weak isolation (due to acquiring/releasing locks and reduced concurrency) -> unstable latencies and deadlocks
- predicate locks
	- prevents phantoms (not existing objects) in serialization model
	- belongs to all objects that match search condition
- index-range locks
	- approximation of predicate locks (applied to larger set than predicate locks) -> fast lock matching
#### serialization snapshot isolation (SSI)
- two-phase locking doesnt perform well, and serial execution doesnt scale well
- SSI is based on snapshot isolation and provides full serializability + small performance penalty -> use both in single node/multiple nodes DB
- currency control
	- pessimistic
		- 2PL waits until the situation is safe before do anything (like mutual exclusion)
		- serial execution transaction has its own lock to entire database (extreme pessimistic)
	- optimistic
		- SSL continues transaction and HOPE that everything will be OK :D, and checks state when transaction commits
		- disadvantage
			- performs badly if there is high contention (many transasctions try to access same object) -> large proportion of transasction are aborted, but contention can be reduced with commutative atomic operations
- decision based on an outdated premise
	- premise is a query result -> any transaction acts on outdated premise must be aborted
	- detecting stale MVCC reads
		- when a transaction reads from consistent snapshot (snapshot isolation), it ignores all writes that haven't been committed when snapshot was taken -> DB tracks when a transaction ignores other writes due to MVCC visiablity rules, if any ignored write is has been committed, transaction must be aborted
	- detecting writes that affect/change prior reads
		- similar to 2PL with index-range locks, but instead of blocking until reader commit, DB tells to transaction that its data may not be up-to-date
- advantage
	- not blocking transaction when lock is held by other transaction (2PL)
	- scale up to multi CPUs, nodes (serial execution)
	- work well with short read/write and long read-only transactions
- disadvantage
	- less sensitive than 2PL and serial execution for slow transactions
# consistency - consensus
- **consensus: getting all of the nodes to agree on something
- most DBs provide **eventually consistency** - if stop writing to database and wait **unspecified** length of time, eventually all reads return same value (consistency) or convergence

### linearizability = serializability with causality (real-time order)?
- make a DB appear as if there were only one copy of data, and all operations are atomic
- linearizability is **recency guarantee** (read after write - once a new value has been written or read, all subsequent reads see that value, until it is overwritten again) -> operations are executed in **well-defined order**
- DB that guarantees linearizability is slow -> many DBs don't provide linearizability guarantee
![[Pasted image 20250208233035.png | 600]]
- linearizability vs serializability
	- serializability: isolation property of transaction, guarantee that concurrent transactions run as without concurrency (in serial order)
	- linearizability: recency guarantee
	- -> combination: **strict serializability** or **strong one-copy serializability**
- implementation
	- single-leader replication (potentially linearizable - only one leader accepts writes)
	- consensus algorithm (linearizable)
	- multi-leader replication (not linearizable - multiple nodes accept writes)
	- leaderless replication (potentially not linearizable - quorums conditions aren't met)
#### CAP theorem
- consistent or available when partitioned >> consistency, availiability, partition tolerance
- when a network fault occurs (network partition) -> choose between linearizability or availability
- CAP theorem doesn't mention other network problems -> little practical value
### ordering guarantees
#### ordering and causality
- **consistent with causality** (consistent snapshot isolation)
	- if the snapshot contains an answer (effect), it must contain the question being answered (cause)
- causal order is not total order (partial order), while linearizability is total order -> linearizability > causuality consistency
	- linearizability: system behaves as if there is a single copy of data, every operation is atomic
	- causality: 2 operations are incomparable, if they are concurrent
		- is **strongest consistency model** not slow down due to network delay
- maintain causality (ensures messages respect cause-and-effect, but unrelated messages can shuffle differently across nodes) = know which operation happened before other operation -> keep this order in all relicas
#### sequence number ordering
- assing a sequence number/timestamp to each operation -> total order (2 operations are comparable)
- if a follower (single leader DB) applies replication log in same order -> causally consistency
- Lamport timestamp
	- keep pair of (counter/timestamp, nodeid) -> unique timestamp for each operation between multiple nodes -> total order
	- a node keeps track of maximum counter value in request (may come from another node), if this value is greater than current counter value, set current counter value to this value
#### total order broadcast
- is a protocol for exchanging messages between nodes, with reliable delivery (no message is lost) and totally ordered delivery (delivered messages are in same order for all nodes) -> guarentees linearizable writes, not linearizable reads
- every replica processes the same writes to the DB in same order -> replicas remain consistent with each other -> fixed order at the time messages are delivered
- total order broadcase is asynchronous: guarantees to delivery messages in a fixed order, but not the time when messages are delivered
### distributed transactions and consensus
- consensus: "get several nodes agree on something"
#### atomic commit / two-phase commit (2PC)
- algorithm for atomic transaction commit across multiple nodes
![[Pasted image 20250215204428.png | 600]]
- includes 2 phases
	- prepare
		- coordinator sends prepare requests to all participants, 
		- participant makes sure it can commit **under all circumstances** (including node crash, networking, ...), if any participant responses "no", transaction is aborted on all participants
	- commit
		- coordinator receives responses from participants and decides to commit transaction or not, and write its decision to transaction log (coordinator must write decision to transaction log before sending "commit" request)
		- send commit/abort for this transaction to all participants, retry sending request until it succeeds
- if coordinator crashes
	- before sending "prepare" -> all participants abort transaction
	- before sending "commit" -> all participants have to wait coordinator response -> may cause inconsistence between participants
- three-phase commit - nonblocking atomic commit protocol -> perfect failure detector for telling whether node has crashed or not?
#### XA transaction
- a standard for implemeting 2PC across heterogeneous technologies (from 2 or more different technologies)
#### fault-tolerant consensus
- consensus: getting several nodes to agree on something (full agreement, not partial), consensus algorithm helps to select final value from some proposed values
- **partial consensus**
	- quorum-based (majority agreement)
	- fault-tolenrant: tolerate node failing or disagreeing
	- eventually consistency
- consensus' properties
	- uniform / full agreement: no 2 nodes decide differently
	- integrity: no node decides twice
	- validity: if a node dicides a value, this value must be proposed by some node
	- termination: every node doesnt crash eventually decides some value -> process doesnt get stuck, even if some node fails, the system must reach a decision -> requires **at least a majority of nodes** to be functioning correctly
- single-leader replication - consensus
	- 2 rounds of voting leader: choose a leader + vote on a leader's proposal; requires quorums of 2 rounds must overlap (at least 1 node votes for both most recent leader and its proposal)
#### membership and coordination services

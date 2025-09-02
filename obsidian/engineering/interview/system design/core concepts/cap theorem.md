[hellointerview](https://www.hellointerview.com/learn/system-design/deep-dives/cap-theorem)

**important concept in non-functional requirements** -> the first thing in non-functional requirements
# CAP theorem
- consistency: all nodes see same data at the same time -> no stale data
- availability: every request to a non-failing node receives a response (without guarantee that data is latest)
- partition tolerance: the system continues to operate despite data loss or failure of part of the system (eg. network partition between nodes, ...)

=> when partition happens (it always happens in distributed system), choose consistency (C) or availability (A)?

### when to choose consistency
- ticket booking, e-commerce inventory, financial, ... -> transaction system
- the design should includes
	- distributed transaction (with 2-phase commit)
	- single-node solution (no distributed system)
	- traditional DBMS (support transaction + rollback)

### when to choose availability
- social network, content platform (streaming), review sites, ... -> social/network
- the design should includes
	- multiple replicas (replication + partition (sharding))
	- change data capture (CDC)
		- track changes in primary DB and propagate them **asynchronously** to replicas, caches, ...
	- DBMS support replication + partition

# levels (spectrum) of consistency (highest to lowest)
1. strong consistency
	- all reads reflect the most recent write -> expensive, but is neccesary for banking system (account balance) 
2. causal consistency
	- related events are in same order for all users
3. read-your-own-writes consistency
	- users always see own updates, though other users might see state data
4. eventual consistency
	- the system becomes consistent over time, but may temporarily be inconsistent
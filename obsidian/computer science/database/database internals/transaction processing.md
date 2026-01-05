# ACID
- atomic: transaction steps are indivisible, all or none of them are successful (transaction commits or aborts)
- consistency: an application-specific guarantee
- isolation: multiple concurrently transactions run without interference (changes may become visible to other concurrent transactions)
- durability: when transaction is committed, all modifications must be persisted

# caching
### cached page
- cache pages read from disk in memory
- any changes are made to cached page, it is 'dirty' until it is flushed back on disk (before eviction)
### page replacement
- LRU (two-queue LRU)
- CLOCK (circular buffer)
- LFU
	- more frequently accessed items have higher chance of retention and vice versa
# recovery
- write-ahead log (WAL) (commit log) is **append-only** disk-resident structure for crash and transaction recovery
- every record in WAL has unique and monotonically increaseing log sequence number (LSN) -> all logs records have to be flushed on disk in LSN order

# transaction isolation
### read/write anomalies
- a dirty read
	- reads uncommitted changes from other transactions
- a nonrepeatable read
	- queries same row twice but get different results
- a phantom read
	- queries same set of rows twice but get different results
- a lost update
	- both transactions T1 and T2 update value of V -> update of either T1 and T2 will be lost
- a dirty write
	- get uncommitted value, modify and save it
- a write skew
	- combination of transactiosn does not satisfy invariants (but each transaction does)

### isolation levels
||dirty read|non-repeatable read|phantom read|
|---|---|---|---|
|read uncommitted| &#x2714 | &#x2714 | &#x2714 |
|read committed| | &#x2714 | &#x2714 |
|repeatable read (lock reading rows -> blocking)| | | &#x2714 |
|snapshot isolation (row versioning -> non-blocking -> write skew)| | | |
|serializable| | | |
# concurrency control
### optimistic concurrency control (OCC)
- all transactions to execute concurrent read/write operations and determines whether or not the result of execution is serializable
### multiversion concurrency control (MVCC)
- guarantees a consistent view of DB at some point in past (timestamp)
### pessimistic/conservation concurrency control (PCC)
- timestamp ordering
	- read value with timestamp < max_write_timestamp -> abort transaction of reads
	- write with timestamp < max_read_timestamp -> conflict with recent reads
- locking
	- two phase locking - 2PL
		- growing phase: all locks are acquired
		- shrinking phase: all locks are released
	- deadlock
		- timeout + abort long-running transactions
	- locks (logical) & latches (physical)
		- lock isolates and schedules overlapping transactions and manage DB contents -> is held for duration of transaction (visible to user)
		- latch guards physical representation (leaf-page contents are modified during operations, page contents and tree structure) -> is held for duration of physical operation (hidden from user)
			- latch crabbing
				- grab all latches on road from root to target node (straightforward but not practical)
				- LC holds latches for less time and release them ASAP (not require anymore)
	- reader-write lock (RWL)
		- multiple readers access object concurrently, only writes have to obtain exclusive access to object
		- readers acquire shared latch (SH), and write acquires exclusive latch (EX, EX only is held by 1 thread)
		![[Pasted image 20260105133440.png | 600]]
- nonlocking

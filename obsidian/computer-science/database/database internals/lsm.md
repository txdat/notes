# lsm trees
- use buffering and append-only storage to achieve sequential writes
- immutable structures needn't locate data on disk to update, duplicate contents are allowed and conflicts are resolved during read time -> writes are commoner than reads
### 2 components lsm tree
- mutable memory-resident (memtable)
	- it buffers data records and serves as a target for read/write operations
	- its data is flushed on disk when its size grows up to a threshold
- immutable disk-resident
	- it is built by flushing data from memtable -> read-only
#### flushing process
- all new writes go to new memtable when flushing starts
- both disk/memory-resident data must be accessible for reads during flushing
- unmerged disk/memory-resident must be discarded after flushing
### multi components lsm tree
### lsm updates
- use **tombstone** marker to mark deleted records (because SS-tables are immutable), and it is removed during compaction
### lsm lookups
- during lookup, multiple contents are merged and reconciled before returning to client
#### merge-iteration
- merge data from multiple sources using iterators and priority-queue (output is sorted)
#### reconciliation/conflict resolution

### compaction
- it reads and merges contents from some tables, replaces old tables with new merged table
![[Pasted image 20260220164004.png | 600]]

#### leveled compaction
- it separates disk-resident tables into levels
- level-0 tables are created by flushing memtable contents, they are merged to level-1 tables and so on
- key ranges for tables on level 1 and higher level do not overlap (in same level)
- when search a value: search on write buffer, multiple segments on level 0 (they can overlap), 1 segment on each next level
![[Pasted image 20260221163813.png | 600]]
#### size-tiered compaction
- group tables by size instead of level
- one of problems is table starvation (compacted tables are small enough after compaction)

### sorted string tables (SS-table)
- data records in SS-tables are sorted
### bloom filter
- is a space-efficient probabilistic data structure to test whether an element is a member of set or not. it can produce false-positive/false-negative result
- it uses a large bit array and multiple hash functions. if an element is a member of set, all of hash functions' bit are set
- probability of false positives are managed by size of bit set and number of hash functions

### skip list (singly-linked list)
- it is a data structure for keeping sorted data in memory
- it has better concurrency than b-tree in memory, b-tree is cache-friendly
- it use **probabilistic balancing** when a new node is inserted (how many levels/express lanes?), b-tree uses deterministic balancing
- its structure is simpler (resembling a singly-linked list)
	- lowest level: contains all sorted items
	- higher levels (express lanes): each higher level skips over items
![[Pasted image 20260221171610.png | 600]]
### concurrency in LSM
- main challenges are switching table views and log synchronization
- synchronization flow
	1. memtable switch: all writes go to new memtable (primary), the old one is available for reads
	2. flush finalization: replaces old memtable with a flushed disk-resident table in table view
	3. write-ahead log truncation: discards log segments that associate with a flushed memtable (after flushing is complete)
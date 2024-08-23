# introduction
- 3 concerns
		- reliability: the system should work correctly even in the face of adversity (faults, errors, ...) -> fault tolerance
	- scalability: there should be reasonable ways of dealing with the growth of data, traffic, ... (~ a system's ability to cope with increased load)
		- performance
			- when increase load parameters and keep system's resources unchange, how is the performance affected?
			- when increase load parameters, how much need to increase system's resources to keep the performance unchanged?
		- metric
			- average response time of service -> percentiles -> know how long users typically have to wait
			- high percentage of response time (tail latencies) -> effect user's experience of service
			- SLO (service level objectives)
			- SLA (service level agreements)
				- service is up if median (p50) response time less than 200ms and 99th percentile (p99) under 1s
		- cope with load
			- scaling up (vertical) / out (horizontal)
	- maintainablilty

# data models and query languages
- relational vs document model
	- relational
		- data is ogranized in relations (tables) and each relation is an unordered collection of tuples (rows)
		- theoretical proposal
		- schema-on-write (structure is explicit)
		- query optimizer decices which parts of query to execute first and which indexes to use
	- nosql
		- greater scalability (very large dataset, very high write throughput, ...)
		- dynamic and expressive data models
		- schemaless -> schema-on-read (structure is implicit)
		- need more works to keep data consistency (in many-to-many relationship)
	- many-to-one, many-to-many relationships
		- if something has no meaning to human, it never needs to change (ie. id). something is meaningful to human, it may be changed in the future -> write overhead, inconsistencies, ...
- mapreduce

# storage and retrieval
- storage engines are optimized for transactional workloads and analytics?
## index
- find the value for a particular key more efficient
- additional data structure, that is derived from the primary data
### hash index
- lots of writes (per key), but not many distinct keys (keep all keys in memory)
- split to segments, each segment has its own in-memory hash table
- append-only design is good at
	- sequential write operations are much faster than random writes
	- concurrency and crash recovery are much simpler if segment files are append-only or immutable
	- avoid data fragmentation over time
### SSTables
![[Pasted image 20240813221121.png | 600]]
- each log segment is a sequence of key-value pairs, later value overwrites previous values of same key
- sequence of key-values pairs is sorted by key
- each key appears once within each merged segment file
- construction
	- red-black tree/AVL tree -> insert keys in any order and read them in sorted order
- advantages
	- merging segments is simple and efficient (similar to mergesort). if same key appears in several input segments -> keep value from most recent segment and discard others
	- jump and scan key without exact offset of key in segment (due to sorted keys) -> sparse in-memory index
	- group records to block before writing to disk -> reduce IO
- disadvantages
	- if database crashes, the most recent writes (in memtable, not disk) are lost -> keep logs on disk (without ordering for crash backup)
### LSM-tree
- used in embedded key-value storage engine like RocksDB, LevelDB,
- based on principle of merging and compacting sorted files
- support high write throughput applications
- use Bloom filter for optimize data access -> check key doesn't exist
- the order and timing how SSTables are compacted and merged
	- size-tiered
		- newer and smaller SSTables are merged into older and larger SSTables
	- leveled
		- split up into smaller SSTables and older data is moved into separate levels
### B-Tree
![[Pasted image 20240813223622.png | 600]]
![[Pasted image 20240813223647.png|600]]
- B-tree with n keys always has a depth of O(logn) -> most of databases can fit into 3 or 4 levels depth
- the overwrite data doesn't change the location of page (ref), different from LSM (append only)
- implement write-ahead log (WAL) (append-only before modify tree itself) to make database more resilient to crashes
- B-tree index key locates in exactly one place in the index, whereas LSM can store multiple copies of the same key in different segments
### difference between online transaction processing (OLTP) - online analytic processing (OLAP)
![[Pasted image 20240815221711.png | 600]]
### column-oriented storage - #todo 
# encoding - #todo 
### JSON, XML, binary variants
### thrift, protobuf, avro: binary encoding
- requires a schema for any data
### asynchronous message passing dataflow
- message broker
	- sends a message to a named queue/topic, and ensures that the message is delivered to consumers/subscribers to that queue/topic -> one-way dataflow
- 

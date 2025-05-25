# pages
- page - fixed size block of data (with unique identifier - pageId)
### heap file
- unordered collection of pages
- page directory: special pages store location of data pages

### page layout
- tuple-oriented
	- slotted pages: map slots to the tuples' starting position -> keeps track of number of used slots, and offset of last (most recent?) used slot
	![[Pasted image 20250517164033.png | 300]]
	- tuple (sequence of bytes) layout
		- stored in the order specified when creating table
		- DBMS can **denormalized** (pre-join) and store related tuples in same page -> make update more expensive

- log-structured
	- DBMS applies changes to in-memory data (MemTable) and writes out the changes sequentially to disk (SSTable)
	- DBMS appends log records to EOF, without checking previous log records
	- DBMS compacts SSTable periodically to reduce wasted space, and speed up reads
	![[Pasted image 20250517164727.png | 500]]
- index-organized
	- DBMS stores a table's tuples as value of an index (leaf nodes in tree)
### storage models for workload
- workload: OLAP (online analysis processing - complex, aggregation on many records) and OLTP (online transaction processing - simple, writes on single or few records)
- n-ary storage model (NSM)
	- store almost all attributes of a single record in one page -> OLTP
	- advantages
		- fast insert,update and delete
		- good for queries need entire tuple
	- disadvantages
		- not good for scanning large portions of table/subset of attributes

- decomposition storage model (DSM)
	- store a single attribute of all tuples contigously in a block of data -> column store -> ideal for OLAP (read only queries perform large scans over subset of attributes)
	- store attributes and metadata in separated fixed-length arrays
	- advantages
		- reduce IO cost per query because DBMS only reads the data that it needs
		- faster query processing because of locality and cached data reuse
	- disadvantages
		- slow for insert,update and delete
- pax storage model (hybrid)
	- vertically partitions attributes within a database page (eg. Parquet, arrow, ...)
	- horizontally partition data into row groups -> vertically partition their attributes into column chunks

### data compression
# database storage
- spatial control
	- where to write pages on disk
	- keep pages that are used together close together on disk
- temporal control
	- when to read pages into memory and when to write them to disk
	- minimize number of stalls from having to read data from disk
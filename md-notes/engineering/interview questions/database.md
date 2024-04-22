1. SQL vs noSQL?
	- SQL
		- SQL or relational DB are row-store, describes the relation between objects. it is organized with schemas and tables. 
		- all records in a table have same structure, follow same constraints
		- guarantees ACID characteristics
	- noSQL
		- store data in more free froms, compared to SQL
		- some main types:
			- key-value: redis, memcache,
				- different between redis and memcached?
					- redis: use single thread, supports more data structures
					- memcached: support multiple processing/threading, store data in string format
			- document: mongodb
			- columnar: cassandra
			- graph: neo4j
			- ...
	- architecture
		- standalone
		- master - slave:
			- 1 server is master server, and others are slave servers (data replication). write operations are only executed on master server, read operations are distributed between servers
			- when a server is down, a new server will be created with same data. if master server is down, one of slave servers is promoted as master, and a new slave server is created
		- cluster?
			- redis: 
	- scaling?
		- usually scale up vertically (add more CPUs, memory, storage)
		- some databases support horizontal scaling (add/remove more servers to scale up/down). eg. cassandra supports horizontal scaling with consistent hashing
2. What is a transaction in SQL? When is a transaction considered successful?
	- a transaction is unit of work, contains one or more operations. an executed transaction changes database from current state to another state.
	- when a transaction is successful, all its operations have to run completely, without any error. if any operation is failed, a transaction is failed
3. ACID
	- are properties of transaction
	- A - atomicity
		- all of transaction's operations must be executed or not together, this ensure that no transaction is completed partially -> transaction is single unit
	- C - consistency
		- keep data consistent before and after executing transaction -> a transaction change data from a consistent state to another consistent state
		- consistent state is state where data meets all constraints, rules and relationships defined in schema
	- I - isolation
		- 2 transactions must not interfere with each other (use same data at the same time)
	- D - durability
		- the changes made by a completed transaction is permanent. it ensures that the consistent state after executing transaction can be recovered after any system failure or crash
- ![[Pasted image 20240317220741.png | 600]]
4. CAP
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
5. SQL normalizations - 4 common types of normalization
[doc](https://opentextbc.ca/dbdesign01/chapter/chapter-12-normalization/)
	- set of specific rules for improving design of database
	- 1st
		- each attribute (table's cell) contains only one (singular) value -> eliminate duplicated data and simplify queries
	- 2nd
		- non-key attributes must be fully dependent on entire primary-key (not partial dependency)
	- 3rd
		- there is not transitive dependencies between attributes, a non-key attribute is not functionally dependent on another non-key attribute
	- boyte-codd (3rd+)
		- every determinant (a attribute can be used to determine value of other attributes) is a candidate key (uniquely identify rows)
7. Data sharding
8. Indexing
	- requires own disk space and holds a copy of data -> redundant data
	- creating index does not change data
9. Database models
- flat model
	- store data in table (row - record/entity, column - attribute) -> lack of ability to handle relationship between entities
- hierarchical model
	- store data in tree-like data structure -> struggles with many-to-many relationsips
- relational model
	- represents data in tables (relations) -> support data integrity, avoid redundancy, support many-to-many relationships, and complex queries and transactions
- star schema
- snowflake model
- network model
10. Caching

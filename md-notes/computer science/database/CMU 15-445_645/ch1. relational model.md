[CMU 15-445/645](https://15445.courses.cs.cmu.edu/spring2024)
# chap 1: relational model
[lec](https://15445.courses.cs.cmu.edu/spring2024/notes/01-relationalmodel.pdf)
- organized collection of inter-related data that models some aspect of real world
- database system management (DBMS)
	- software to store and analyze information in database
	- supports the definition, creation, querying, update and administration of databases
- data model and schema
	- data model
		- collection of concepts describing the data
	- schema
		- description of particular collection of data (data model)
	- relational model
		- unordered set contains the relationship of attributes represent entities
		- defines database abstration based on relations to avoid maintenance overhead (reduce cost?)
		- structure: the definition of database's relations and their contents
		- integrity: ensure database's contents satisfy constraints
		- manipulation: provide programming interface for modifying database's contents
		- data independence
			- isolate user/application from low-level data representation
![[Pasted image 20240420170332.png | 600]]
- relational model
	- primary keys
		- uniquely indentifies a single tuple
		- types:
			- indentity (sql standard)
			- sequence (postgresql/oracle)
			- increment (mysql)
	- foreign keys
		- specifies that an attribute from relation maps to a tuple in another relation
	![[Pasted image 20240420170839.png | 600]]

	- constraints
		- user-defined conditions that must hold for any instance of database
- data manipulation languages (DML)
	- procedural (relational algebra) -> find desired results
		- operations:
			- select, projection, union, intersection, difference, product (generate all combinations of tuples, neednt common values - cross join)
			- join:
				- generate tuples are combination of two tuples with common values
		- define high-level steps to compute a query
	- non-procedural (declarative - relational calculus) -> specify what data is wanted
- queries
	- relational model is independent of any query implementation
- conflict-free replicated data type (CRDT)
	- for distributing data structure that allows local updates to be made independently, and the states eventually converage
	- a family of replicated data types with a common set of properties that enable operations to always converage to a final state consistent among all replicas
	- perform replication as commutative operations (the order doesnt matter)
	- eventual consistency vs strong consistency?
		- strong consistency propagates any update to all copies of data (keep the same order). when a entity makes update, all other replicas are locked to avoid conflicts -> neednt for real-time performance -> eventual consistency (regardless of the order of update events -> resolve conflicts of concurrent updates) 
- another data models
	- document
		- collection of record documents containing a hierarchy of named field/value pairs
		- tightly coupling objects and databases
		- some databases: mongodb, ...
	- vector
		- use for nearest neighbor searching by embedded vectors (exact or approximate), maily for ML systems

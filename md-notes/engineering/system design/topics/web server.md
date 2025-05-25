# Database
1. Relational DB or Non-relational DB
- Relational DB (RDBMs) or SQL
- Non-relational DB (NoSQL)
	- **JOIN is generally not supported**
	- 4 categories:
		- key-value: redis
		- graph: neo4j
		- column: cassandra
		- document: mongodb
	- use for:
		- super low lattency
		- only serialize/deserialize
		- data is unstructured, not having relations
		- store massive amount of data
2. Database replication
- master (supports write ops) / slaves (read only) model
- advantages:
	- better performance (multiple read operations at the same time)
	- reliability
	- high availability
		- if a slave server goes offline, operations will be directed to master server. a new server may replace old one.
		- if the master server goes offline, one of slave servers will be promoted to become master server. data recovery process may be need.
3. Database scaling
	1. vertical scaling
		- add more cpu/memory to server -> quota limit, greater risk of SPOF, more expensive
	2. horizontal scaling
		- sharding data: same schema, part of data
		- some problems:
			- resharding data: more data causes shard exhaustion (uneven data distribution)
			- excessive access to specific shard (example: data of Justin Bieber and Taylor Swift on the same shard)
			- join and denormalize operations
# Cache
- temporary in-memory storage for result of expensive operations or frequently accessed data
- dont use to store persistence data
- use expiration policy and syncing data between cache and database (consistency)
- is single point of failure (SPOF - if it fails, the whole system will be stopped) -> using cache cluster or master-slave
# Content delivery network (CDN)
- a network of geographically dispersed/distributed servers used to deliver static content.
- user ->> server ->> cdn servers ->> user
- use cache expiration for time-sensitive content
- cdn fallback: request resources from origin (server/database)
# Stateless/Stateful architecture
- stateful servers keep client data (state) from one request to the next, while stateless servers don't
- a stateless system is simpler, more robust and scalable
# Data centers
- geoDNS-routed: let to choose resources that serve traffic based on geographic location of users
# Message queue
- durable component, stored in memory, support asynchronous communication between producers/publishers and consumers/subcribers
- producers and subcribers can scale independently. when queue's size is large, more workers are added to reduce processing time and vice versa
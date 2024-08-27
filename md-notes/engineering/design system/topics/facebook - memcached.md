[bytebytego](https://blog.bytebytego.com/p/how-facebook-served-billions-of-requests)
- requirements
	- real-time communication
	- capabilities for on-the-fly content aggregation
	- handle billions of user requests
	- store trillions of items across multiple geographic locations

# memcached
- in memory key-value storage (hash table)
- query cache
	- reduce load on database
	- use memcached as demand-filled look aside cache (data is loaded into cache if client requests it)
- generic cache

# high-level design
### regions
- primary
- secondary -> redundancy, load balancing
### frontend clusters
- web servers (serve contents to users) + memcached (distributed caching)
- support horizontal scaling based on demand
### storage cluster
- data is replicated across multiple regions, employing primary-secondary architecture -> high availability, fault tolerance

# challenges
### within cluster
- reduce latency
	- memcached servers are deployed using consistency hashing
	- parallel requests and batching
		- process multiple data pieces in same request
	- use UDP for fetching requests (GET)
- reduce load
	- reducing frequency of fetching data from database
	- use **look-aside caching design** for memcached
	- caching issues
		- stale set
		- thundering herd
		- ![[Pasted image 20240826001228.png | 600]]
		- leasing technique
			- hands over a lease token to particular client to set data into cache when there is a cache miss
		- handling outages - gutter pool
### region level
- handling memcached's invalidation across all of regions
- 
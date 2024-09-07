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
		- stale set: read outdated cache
		- thundering herd: multiple cache miss triggers (multiple requests send to DB at same time) on highly concurrent environment
		- ![[Pasted image 20240826001228.png | 600]]
		- leasing technique
			- hands over a lease token to particular client to set data into cache when there is a cache miss
		- handling outages - gutter pool (in memcached cluster?)
### region level
- handling memcached's invalidation across all of regions (data can be cached in multiple servers of region)
- an invalidation pipeline - mcsqueal (post hook in DB)
	- a daemon process (mcsqueal) runs on each SQL server, reads commit logs and broadcasts to memcached servers through mcrouter (batch processing)
	- mcrouter iterates each delete operation and sends to correct memcached server
- global regions
	- writes from primary region - cache and replica race condition -> replica DB sends invalidation to memcached server (like mcsqueal)
	![[Pasted image 20240907231914.png | 600]]
	- writes from non-primary region - remote marker -> read data from primary DB instead of replica DB when marker exists
	![[Pasted image 20240907232831.png | 600]]
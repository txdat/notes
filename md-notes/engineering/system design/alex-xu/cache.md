[example](https://www.prisma.io/dataguide/managing-databases/introduction-database-caching)
- read strategies
	- read-aside
		- the cache is seperated from database -> the system can get data from database (if the cache crashes), and can store diffrent data models (compared to database)
		- the application gets missing data from database and writes to the the cache
		- data in cache may be inconsistent
		![[Pasted image 20240420221351.png | 600]]
	- read-through
		- the cache is between the application and the database, always requests data from the cache. for write operations, the application writes to the database directly
		- the cache does operations to get missing data
		![[Pasted image 20240420222123.png | 600]]
- write strategies
	- write-through
		- the application writes data to the cache first, and the cache writes to the database immediately
		- increase write latency because the action must go to the cache and the database
	- write-back
		- similar to write-through strategy, but the cache writes to the database after a delay (not immediately)
		- improve overall write performance, and reduce writes if batching is supported
		- can loss data if the cache is down
	- write-around
		- the application invalidates data in the cache (asynchronously), writes data to the database first, and the data goes to the cache (read-aside)
		![[Pasted image 20240420222927.png | 600]]
- cache validation strategies
	- time-based (expiration)
	- command-based (triggered directly)
	- event-based (triggered by event, may come from other services)
- cache invalidation is hard?
	- when should we to invalidate cache (by time-to-live TTL)?
	- race condition in concurrency
	- data relationship?
	- cache may be in anywhere (in distributed system)
- resolve data inconsistency in write-around strategy
	- [[cache-data-inconsistency]]
	-> read aside + write around (delete cache after writing to database)
		- write operations to cache are much faster than to database -> write around operations nearly unable to run between read - write back operations
		- use ttl to expire data (even distribution)
- cache scaling
	- cluster -> High Availability
	- rate limiter/circuit breaker
- cache breakdown
[systemdesign.one](https://newsletter.systemdesign.one/p/rate-limiter)

- control the rate of traffic sent by a client or service (= number of requests allowed to be sent in a period of time)
- prevents: denial of service (DDoS), reduce cost, prevent servers from being overloaded, ...
# requirements
- accurately limit excessive requests
- low latency
- low memory consumption
- distributed rate limiting (shared across multiple servers, processes)
- exception handling
- high fault tolerance
# high-level design
- rate limiter is implemented on server side. (clients are easily forged by malicious actors, and unable to be controlled)
- implemented on middleware, api gateway (supports rate limiting, ssl termination, ip whitelisting, ...)
- consider where to implement rate limiter: server-side (full of control) or api gateway (commercial)
# low-level design
- algorithms
	1. token bucket
		- a token bucket is a container that has defined capacity. tokens are put at preset rates periodically
		- a request costs a token. if there isn't any token, the request is dropped
		- pros:
			- easy to implement
			- memory efficient
			- allow a burst of traffic for short periods
		- cons:
			- hard to tune 2 parameters: bucket capacity and refill rate
	1. leaking bucket
		- requests are processed at fixed rate using FIFO queue. requests are pulled from queue and processed
		- a request will be dropped if the queue is full
		- pros:
			- memory efficient with limited queue size
			- suitable for use cases that stable outflow rate needed
		- cons:
			- a burst of traffic fills up the queue with old requests, recent requests will be rate limited
			- hard to tune 2 parameters: bucket size (queue size), outflow rate (number of requests processed in second)
	1. fixed window counter
		- devide the timeline into fix-sized time windows and assign a counter for each window
		- a request increases the counter by one. it will be dropped if counter reaches to predefined threshold, and wait to next window
		- pros:
			- easy to understand
			- memory efficient
			- fit certain usecases when reseting quota at the end of unit time
		- cons:
			- a burst of traffic at the edges of time windows could cause more requests than allowed quota go through
		- **MAJOR ISSUE:** allow to more requests at the edges of time window
	1. sliding window log
		- fix major issue of fixed window counter
		- the algorithm keep **sorted log** of requests' timestamp
		- when new request comes, remove all outdated timestamp (older than current time window) and add request's timestamp to log (even request may be dropped later)
		- if size of log is larger than allowed count, request will be dropped, and vice versa
		- pros:
			- very accurate, in any rolling window, requests cannot exceed the limit
		- cons:
			- consume lots of memory because it keeps dropped requests' timestamp
	1. sliding window counter
		- combine fixed window counter and sliding window log
		- the number of requests in rolling window is calculated by: `#requests_in_current_window + #requests_in_prev_window * overlap_percentage_rolling_prev_window`
		- pros:
			- smooth out spikes in traffic
			- memory efficient
		- cons:
			- only work for not-strict look back window
			- this algo assumes that requests are evenly distributed in previous window
# deep-dive
- rate limiter is a distributed system
- race condition
	- happen on highly concurrent environment
	- can be solved by lock (slow down system), or sorted set data structure in redis?
- synchronization issue
	- happen when using multiple rate limiter servers
	- can be solved by using same centralized data stores like redis
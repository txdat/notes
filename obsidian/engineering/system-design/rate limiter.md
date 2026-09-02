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

## algorithm comparison

| Algorithm | Memory | Accuracy | Burst Handling | Complexity | When to Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Token Bucket** | $O(1)$ | High | Allows bursts up to bucket capacity | Low | General-purpose API gateways, user request throttling (e.g., Stripe, AWS). |
| **Leaking Bucket** | $O(N)$ (queue size) | High | Smooths bursts into a constant outflow rate | Medium | E-commerce checkout, message queues, protecting downstream services requiring stable processing rates. |
| **Fixed Window Counter** | $O(1)$ | Low (edge burst up to $2\times$) | Discards excess traffic per window | Low | Daily/monthly tier quotas where boundary burst spikes are tolerable. |
| **Sliding Window Log** | $O(N)$ (request count) | Exact | Strictly enforces limit across any rolling window | High | High-security endpoints (e.g., auth, payment authorization) where precision is mandatory and traffic volume is moderate. |
| **Sliding Window Counter** | $O(1)$ | High ($\approx 99\%$ accurate) | Smooths traffic across window boundaries | Medium | High-scale distributed APIs requiring low memory footprint and boundary protection. |

## algorithms

1. **Token Bucket**
   - **Mechanism:** A bucket holds up to $N$ tokens and refills at a fixed rate of $r$ tokens/sec. Each request consumes 1 token. If no tokens remain, the request is dropped (HTTP 429).
   - **Pros:**
     - Memory efficient ($O(1)$ per key: counter + timestamp).
     - Allows bursts of traffic for short durations.
   - **Cons:**
     - Requires tuning two parameters: bucket capacity and refill rate.
   - **When to use:** General API rate limiting where bursty traffic from legitimate users is normal.

2. **Leaking Bucket**
   - **Mechanism:** Requests enter a fixed-size FIFO queue. A worker processes requests from the queue at a fixed, constant rate. If the queue is full, new requests are dropped.
   - **Pros:**
     - Ensures steady outflow rate and protects fragile downstream dependencies.
     - Memory bounded by queue capacity.
   - **Cons:**
     - Bursts fill the queue with older requests, increasing latency for recent requests.
     - Requires tuning queue size and outflow processing rate.
   - **When to use:** Background job processing, payment gateways, systems that need steady traffic shaping.

3. **Fixed Window Counter**
   - **Mechanism:** Timeline is divided into fixed time windows (e.g., 1 minute). Each window maintains an integer counter. Exceeding the threshold drops requests until the next window starts.
   - **Pros:**
     - Simple to understand and implement.
     - Low memory usage ($O(1)$).
   - **Cons:**
     - **Boundary issue:** A burst of traffic at the window boundary can allow up to $2\times$ the allowed limit within a 1-window duration.
   - **When to use:** Simple reset quotas (e.g., reset 1,000 requests at midnight).

4. **Sliding Window Log**
   - **Mechanism:** Maintains a sorted log of request timestamps (e.g., Redis Sorted Set). On each request, removes timestamps older than `now - window_size`. Adds current timestamp. If log size $\le$ limit, request is accepted; otherwise dropped.
   - **Pros:**
     - 100% accurate: guarantees requests in any sliding window never exceed the limit.
   - **Cons:**
     - High memory consumption: stores timestamps for all requests within the active window.
   - **When to use:** Critical security or financial limits where precision is mandatory and memory cost is acceptable.

5. **Sliding Window Counter**
   - **Mechanism:** Approximates sliding window by combining the current window count and the previous window count:
     $$\text{Estimated Requests} = \text{Current Count} + \text{Previous Count} \times \left(1 - \frac{\text{Current Window Elapsed Time}}{\text{Window Size}}\right)$$
   - **Pros:**
     - Low memory usage ($O(1)$ per key).
     - Smooths out traffic spikes at window boundaries.
   - **Cons:**
     - Approximation assumes requests in the previous window were distributed evenly ($\approx 0.003\%$ error in practice).
   - **When to use:** High-throughput distributed API gateways where scale and memory efficiency matter more than 100% exact precision.

# deep-dive

- **Distributed Rate Limiting:**
  - Synchronize counters across stateless API servers using a centralized cache (e.g., Redis).
- **Concurrency & Race Conditions:**
  - Multiple concurrent requests can cause dirty reads/writes.
  - Solutions:
    - Redis Lua scripts (executes atomically on single thread).
    - Redis sorted sets (`ZADD`, `ZREMRANGEBYSCORE`, `ZCARD`) for sliding logs.
    - Redis modules (e.g., `redis-cell` implementing Generic Cell Rate Algorithm - GCRA).
- **Performance & Fault Tolerance:**
  - Use multi-region Redis clusters with local fallbacks if Redis is unreachable.
  - Return informative HTTP headers: `X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `X-Ratelimit-Retry-After`.

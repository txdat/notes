# OSI model
- layered architecture
- ![[Pasted image 20250904094250.png | 600]]
### network layer (IP)
- handles routing and addressing
- breaks data into packets, forward them and providing best-effort delivery
- node's ip addresses are assigned by DHCP
### transport layer (TCP, UDP, QUIC)
- provides end-to-end communication services
- network load balancer (L4) works here

1. TCP (transmission control protocol)
	- is reliable but with overhead, requires handshake `SYN+ACK`
	- connection is stream and stateful connection between server and client
	- characteristics
		- connection-oriented (establishes connection before sending data)
		- guarantee of delivery (reliable) and ordering
		- flow + congestion control (prevent overwhelming + collapse)
	-> default connection protocol
2. UDP (user diagram protocol)
	- is very fast but not reliable
	- includes source IP, destination IP and binary blob of data
	- characteristics
		- low latency
		- conectionless (no handshake `SYN+ACK`)
		- no guarantee of delivery and ordering
	-> choose UDP if speed is more important than reliablity (eg. streaming, DNS lookup, ...)
### application layer (HTTP, DNS, websocket)
- built on top of TCP or UDP

# HTTP (hypertext transfer protocol)
- is stateless protocol (each request is independent and servers needn't maintain previous requests)
- supports TLS for encryption
- most common status codes
	- 2xx (success)
	- 3xx (permanent/temporary redirection)
	- 4xx (client errors): bad request, authorization, too many requests, ...
	- 5xx (server errors): internal errors, network (gateway) errors, ...
### rest
-> default option for interview
- most common API paradigm
- clients perform operations on their resources
### graphql
-> for flexible data fetching (barely required by interviewr for specific platforms)
- under-fetching: need multiple requests and round trips, add overhead and latency for page loading
- over-fetching: api needs long time to load and returns too much data

### rpc
-> for performant communication in microservices or service-to-service
- well-defined schema (using protobuf, thrift)

### sse (server-send events)
-> realtime push notification relies on HTTP, but is expensive to maintain connection
- allow server to stream many messages over time in a single response

=> if microsevices and performant API, then RPC, else REST
# websocket - high frequency, persistent, real time bidirectional communication
- websockets provide a persistent, tcp-style connection between client and server -> real-time bidirectional communication
- server and client push data to each other without being prompted by a new request

### comparison of polling, SSE and websocket
| Feature                        | Polling (Short & Long)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Server-Sent Events (SSE)                                                                                                                                                                                                                                   | WebSockets                                                                                                                    |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Communication Direction**    | **Unidirectional** (Client pulls)<br>Client requests; Server responds.<br>- Short polling: The client periodically sends HTTP requests to the server (e.g., every few seconds) to check for updates. If no data is available, the server returns an empty response immediately<br>- Long polling: The client sends a request, but the server holds the connection open and does not respond until data is available or a timeout occurs. Once the client receives a response, it immediately sends a new request to re-establish the wait | **Unidirectional** (Server pushes)<br>Client requests once; Server streams chunks.<br>The client opens a connection, and the server keeps it open to push text-based messages (events) whenever updates occur. It functions like a one-way radio broadcast | **Bidirectional** (Full-Duplex)<br>Client and Server talk simultaneously.                                                     |
| **Protocol & Handshake**       | **Standard HTTP**<br>Uses standard GET requests. Long polling holds the request open until data is available.                                                                                                                                                                                                                                                                                                                                                                                                                             | **HTTP**<br>Standard HTTP request where the server keeps the connection open and sends data as a stream of text.                                                                                                                                           | **TCP (via HTTP Upgrade)**<br>Starts as HTTP GET with `Upgrade` header, then switches to binary TCP stream.                   |
| **Connection State**           | **Stateless (mostly)**<br>Short polling creates a new connection per request. Long polling requires re-establishing connection after every message.                                                                                                                                                                                                                                                                                                                                                                                       | **Long-lived (Persistent)**<br>Maintains a single open connection for the duration of the stream.                                                                                                                                                          | **Stateful (Persistent)**<br>Both client and server must maintain connection state (open sockets).                            |
| **Data Format**                | **Flexible**<br>JSON, XML, Binary, etc.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | **Text Only**<br>UTF-8 text data only. Cannot handle binary natively.                                                                                                                                                                                      | **Text & Binary**<br>Supports both strings and binary data frames.                                                            |
| **Latency**                    | **High to Medium**<br>Short polling depends on interval. Long polling is better but requires a round-trip to re-connect after receiving data.                                                                                                                                                                                                                                                                                                                                                                                             | **Low**<br>Server pushes data instantly. No need for client to request updates.                                                                                                                                                                            | **Lowest**<br>No header overhead per message. Data frames are lightweight.                                                    |
| **Load Balancing (LB)**        | **Layer 7 (L7) Friendly**<br>Works easily with standard HTTP load balancers. Long polling may require basic sticky sessions.                                                                                                                                                                                                                                                                                                                                                                                                              | **Layer 7 (L7) Friendly**<br>Works with standard HTTP LBs, though some proxies may buffer responses and delay delivery.                                                                                                                                    | **Layer 4 (L4) Preferred**<br>Often requires L4 LBs to maintain the persistent TCP connection. L7 is possible but complex.    |
| **Firewall & Proxy Tolerance** | **High**<br>Looks like standard HTTP traffic. Works almost everywhere.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **Medium**<br>Some corporate firewalls/proxies drop connections that stay open too long without activity.                                                                                                                                                  | **Low/Medium**<br>Requires `Connection: Upgrade` support. Aggressive firewalls may block non-standard traffic.                |
| **Resource Overhead**          | **High**<br>Repeated HTTP headers sent with every request. Long polling consumes server threads while waiting.                                                                                                                                                                                                                                                                                                                                                                                                                            | **Medium**<br>Single connection handshake, but keeps an open socket.                                                                                                                                                                                       | **Low (Per Message)**<br>Initial handshake overhead, but subsequent messages have minimal framing overhead.                   |
| **Reconnection Logic**         | **Manual**<br>Client must handle interval logic and error retries.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | **Built-in**<br>`EventSource` API in browsers handles automatic reconnection and tracking last message ID.                                                                                                                                                 | **Manual**<br>Client logic must detect disconnects and initiate a new handshake.                                              |
| **Ideal Use Case**             | **Dashboards / Analytics**<br>Where real-time is not critical (e.g., CMS content updates, slow-moving metrics).                                                                                                                                                                                                                                                                                                                                                                                                                           | **News Feeds / Notifications**<br>Stock tickers, sports scores, social media feeds where client doesn't need to write back.                                                                                                                                | **Chat / Gaming / Collab**<br>Multiplayer games, chat apps, Google Docs, where speed and bidirectional interaction are vital. |

# load balancing
### client-side
- lets client choose which server to talk to (client sends request to service registry to get list of server and chooses one of them)
- use cases
	- small number of clients
	- server with slow updates (eg. DNS)
	- internal services
### dedicated LB (server-side)
- client -> LB -> servers (LB chooses which server will process request from client)
- load balancing algorightms
	- round-robin
	- random
	- least connections
	- least response time
	- IP hash

- network load balancer (transport layer TCP/UDP - L4)
	- make routing based on network information (ip address, port, ...) instead of request content
	- maintain persistent connection between server and client (all subsequent requests within TCP session will be processed by one server?)
	- ![[Pasted image 20250907161903.png | 700]]
	- where to use?
		- websockets (requires persistent TCP connection)
		- high performance application

- application load balancer (L7)
	- make routing based on request content -> more intelligent routing decisions
	- receive application-leve requesst (HTTP) and forward them to appropriate servers
	- are suitable for HTTP-based traffic
	- ![[Pasted image 20250907162653.png | 700]]
	- where to use?
		- all HTTP-based traffic (except websocket)

# regionalization, latency and data locality
### content delivery network (CDN)
- most common strategy to reduce latency
- cache data at edge server (edge location) to reduce network time

### regional partitioning

# handling failures and fault modes
### backoff
- instead of retrying immediately, wait a short amount of time before retrying
- [aws timeouts, retries and backoffs](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

### idempotency
- `f(f(f(...f(x)...))) = f(x)`
- setup idempotency key to API -> lock

### circuit breaker
- protect the system when network calls to dependencies fail repeatedly
- advantages
	- fail fast: reject requests to failing services, instead of waiting timeouts
	- reduce load: prevent overwhelming services
	- self-healing
	- system stability
- where to use
	- (external) third party services
	- database connections and queries
	- service-to-service in microservices
	- resource intensive operations
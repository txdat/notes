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
[systemdesign.one](https://systemdesign.one/url-shortening-system-design/)

- allows users to publish their comments on live video
- event-driven architecture can be used to build real-time data platform
- **read-heavy system** (clients view live comments)

# api design
- use pull-based model (client-initiated), and HTTP long pooling with server-sent events (SSE) (server streams events on same connection, with header `Accept: text/event-stream`)
- SSE works on traditional HTTP and supports chunking messages
- disadvantages of SSE
	- only support UTF-8 message transporting, no support for binary data
	- up to 6 concurrent connections (before http2)

# data storage
- relational DB is **suboptimal** solution for live comment service due to scalability limitations (internal data structures (delay) and complex operation to aggregation)
- nosql DB can be used for live comment data storage due to
	- use LSM storage for high performance for writes, but not optimized for reads
	- schemaless data models reduce overhead of joining tables
	- optimized for time-series data
- redis can be used to store live comments, with deduplication logic to prevent repeated live comments, and keep chronological ordering of live comments

# high-level design
### write globally - read locally
- reads come to servers on local DC, while writes come to servers on global DC
-> not use due to
	- significant bandwidth usage on data replication
	- not real-time due to asynchronous replication
	- poor latency

### write locally - read globally
- writes come to servers on local DC, while reads come to servers on global DC (pull-based model)
- timestamps can be used to check latest messages, and server in local DC will consolidate all published messages and return to client
- bandwidth usage is low because data isnt replicated globally, but latency is degraded because server will query data from all DCs
-> not use

- writes are broadcast/replicated to multiple DCs (push-based model) -> reduce usage of bandwidth and improve latency -> use this model

![[Pasted image 20250605215447.png | 500]]

### distribution of live comments
- receiver can periodically request (polling) server to check new messages -> unnecessary bandwidth (empty response), overload servers -> **push-based SSE** is optimal for real-time delivery of live comments

### pub/sub server
- publisher uses message bus to send messages to multiple consumers -> communicate instantly without having intervals for polling data
#### kafka
- as pub/sub server to decouple producers/consumers (separation of concerns)
- lower overheads, ordering guarantees, integrity guarantees and idempotency
- limitations
	- kafka consumers use pull-based model (consumer polls the broker to fetch messages from subscribed topics) -> degraded latency
	- limit scalability because consumer has to subscribe all topics, and consumes all messages
	- operational complexity is high

#### redis
- as pub/sub server to transmit messages between nodes
- replicates every message to all nodes (dont know about receivers) -> degraded performance
- TCP connections are maintained between producer-redis, and redis-consumer for delivering messages
- limitations
	- no guarantee at least one-time message delivery
	- reliability of message delivery depends on TCP connection?
	- lack of message persistence

#### redis streams
- used as append-only log to improve the responsiveness of system (similar to kafka)
- addresses above redis' limitations (data can be lost because it is periodically written to disk)
- redis sentinel/active-active leads to increased complexity of operations

# deep dive design
### gateway server
- actors in gateway server keep SSE connection to client, and handle how message is sent to clients
- actors **use in-memory subscription store** (redis) to broadcast message to child actors (connect to subscribed clients) when multiple clients subscribe different video on same gateway server
- ![[Pasted image 20250606105619.png | 600]]
### massive concurrent clients on multiple videos
- use dispatcher to broadcast message to partitioned gateway servers
- gateway servers (clients) only subscribe a subset of live videos -> dispatcher broadcasts **inefficiently** messages to all gateway servers
- dispatcher uses endpoint store to track which videos are requested by gateway servers for broadcasting
- ![[Pasted image 20250606110657.png | 600]]

### handle peak loads
- **stateless** dispatcher can be replicated for horizontal scaling -> move endpoint store to external store (out of )

### workflow
[[Excalidraw/live comment|live comment]]
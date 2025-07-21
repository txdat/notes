[systemdesign.one](https://systemdesign.one/gossip-protocol/)

# service management
### centralized
- service management (like Zookeeper) can be configured as service discovery to keep track of state of node -> strong consistency, but may be single point of failure
### peer-to-peer
- toward to high availability and eventually consistency
- gossip protocol is peer-to-peer state management

# message broadcast in distributed system
### point-to-point
- producers send message direclty to consumers
- retry and deduplication mechanisms are reliable, message will be lost if both producer and consumer fail at the same time
### eager realiable
- every node re-broadcasts messages to every other nodes -> improve fault tolerance
- limitations
	- cost of network transmission is more expensive (more usage)
	- increase cost of storage (every node has to store all messages)
### gossip protocol
- **core concept**: every node periodically sends out messages to a subset of other random nodes -> build global map with limited local interactions
- is robust, scalable and eventually consistent algorightm -> maintain node membership list, consensus, and fault detection
- messages can be retransmitted. FIFO, causality, total order broadcast can be implemented in gossip protocol
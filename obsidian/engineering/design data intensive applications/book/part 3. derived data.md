- system of records - source of truth
	- holds authoritative version of data, incomming data is written here first
- derived data
	- holds transformed/processed data from another systems
	- derived data is redundant - denormalized, but is essential for read queries (better performance)
	
- system types
	- services (online system)
		- primary measure: response time + availability
	- batch processing (offline system)
		- primary measure: throughput (number of jobs?)
	- stream processing (half online system)
		- operates on events shortly after they happen -> lower latency than batch processing system
# batch processing

### mapreduce
- mapper:
	- extract key/value tuples from each record, each record can handle independently
- reducer:
	- aggregate each key/value tuples from mapper into single value
- distributed mapreduce
	- ![[Pasted image 20250403135645.png | 600]]
- reducer-side joins and grouping
- map-side joins
	- need some assumptions about data

# stream processing
### transmitting event streams
- event: 
	- small, self-contained, immutable object containing the details of something
	- events are grouped into topic/stream
### message systems
- -> the producers send messages faster than the consumers can process them?
- -> if nodes crash/go offline, are any messages lost?

- direct messaging
	- use direct network communication between producers and consumers - brokerless messaging
- message brokers - message queue
	- can keep message permanently
	- can use unbounded message queue for slow consumers
	- multiple consumers
		- load balancing: assign one consumer for each message
		- fan-out: broadcase a message to all consumers, run independently
		- ![[Pasted image 20250405111232.png | 600]]
	- acknowledgements and redelivery
		- consumer must tell to message broker that message processing is success (ack), if not (failed response, timeout, ...) the message is sent to another consumer (redelivery)
		- message can be reordering (message is redelivered) when using load balancing
	- using logs (append-only sequence of records) for message storage
		- a producer sends a message by appending it to log, a consumer reads log sequentially
		- log-based approach supports fan-out messaging, multiple consumers can read independently (not delete message from queue)
	- change data capture (CDC)
		- observe all data changes written to DB, extract them to apply to derived data systems
		- database trigger can be used to implement CDC
### event sourcing
- store all changes as log of change events, built on immutable events that are written to an event log
- commands/events
	- command: user's request
	- event: command -> event (is fact, cannt be rejected by consumer)
- immutable events
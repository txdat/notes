[blog](https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html)

# CAP theorem
- consistency: linearizability - specific notion of consistency
- availability: every request received by non-failing node (able to handle it) must result in a non response
- (network) partition tolerance: message may be delay or dropped on asynchronous network
# linearizability - consistency
- informal definition: "if operation B start after operation A complete, it must see the system in the same state as it was on completion of operation A or newer state"
- if you want to provide linearizability (consistency), you have to make it appears as only one single copy of data (even though there are multiple copies of data in multiple places)
# availability
- having multiple copies of data (master-slave, master-master, quorum, ...), if data is writen to one of server, it also be writen to another servers -> there is connection between 2 servers for replication
# network partition
![[Pasted image 20240517150725.png | 600]]
	- one of two
		- continue writing to database -> fully available in both servers (any change in one server is not appeared in the other server) -> violate linearizability (consistency)
		- make sure to read/write to only one server (keep linearizability), other server refuses read/write to wait network partition is healed and database is synced again -> violate availability
# case study: zookeeper
- ZK uses consensus algorithm -> consistency over availability?
- client is connected to 1 server and reads data on this server (maybe not latest data?) -> not meet linearizability of CAP
- ZK requires majority quorum to reach consensus. if network is partitioned with 2 sides: majority nodes and minority nodes, nodes in minority nodes continue working without write operations -> not meet CAP availability
- is algorithm allow multi processes to reach to agreement on a value -> putting events in a particular order and ensuring consistency among the participants

# broadcast
- a communication abstraction in distributed system to disseminate information among a set of processes
- reliable broadcast guarantees that all correct processes receive the same message -> use fallback mechanism and failure detector
### atomic broadcast - total order multicast
- it guarantees both reliable delivery and total order of messages = same messages and same sequences of messages
- **atomicity**
	- either all non-failed processes deliver/agree on set of messages or none do
- **order**
	- all non-failed processes deliver messages in the same order
#### virtual synchrony
- it delivers totally ordered messages to dynamic group of peers -> processes can see identical messages (order) only as long as they belong to same group
- it distinguishes **message receipt** (when a group member receives the message) and **delivery** (which happens when all member receive the messages). If the message was sent in one view (group members change), it can be delivered only in the same way
- all messages are sent and delivered between the view changes.
### zookeeper atomic broadcast (ZAB)
- it has 2 roles leader (the temporary role to broadcast messages and establishes the order) and follower
- timeline is split into **epochs**. in each epoch, there is only one leader (using election)
- after a prospective leader is established, there are 3 phases
	- discovery
		- the leader proposes new epoch (greater than current epoch of any follower) -> no proposal of earlier epoch is accepted
		- in failure path, if the leader node crashes, node with highest/latest transaction id will be elected as the new leader
	- synchronization
		- the system recovers from previous leader's failure and brings lagging followers up to speed.
		- the leader proposes itself as the new leader and collects acknowledge from followers -> not accept follower's attempt to become new leader
	- broadcast
		- the leader receives client messages, establish their order and broadcast them to followers (waits for a quorum then commit)
	![[Pasted image 20260215142509.png | 700]]
- it ensures that followers accept proposals from the leader of established epoch and messages are totally ordered (leader doesn't attempt to send next message until the message is acknowledged)
- ZAB is efficient. the broadcast process requires 2 rounds of messages, and leader failure can be recovered from streaming missing messages from a single up-to-date process
# paxos
- it includes 3 roles, any participant can take any role
	- **proposers** receive values from clients, create proposals and collect votes from acceptors
	- **acceptors** accept/reject proposals
	- **learners** store outcomes of accepted proposals

### paxos algorithm
- it includes 2 phases
	- **prepare/promise**
		- prepare: proposer send proposal number N in `Prepare(N)` to quorum of acceptors
		- promise: 
			- if N is larger than any proposal number it has seen -> ignore all future proposals with number less than N
			- if acceptor has accepted any proposal before `Accept(m,v)`, it returns `Promise(m,v)` to proposer
	- **accept(propose)/accepted**
		- propose:
			- if proposer receives `Promise(m,v)` -> proposer adopts the value with highest proposal number (safety guarantee). The proposer **must abandon** its own value (effectively lost/discarded) and propose the value with highest proposal number 
			- if no values were returned, proposer selects its own value
			- proposer send `Accept(N,value)` to acceptors
			-> **once value reaches a quorum, every subsequent successful round of Paxos will choose this value.**
		- **accepted**
			- if acceptor receives `Accept(N,value)` and doesn't ignore proposal N (has seen larger value), it accepts proposal N and notifies learners (to store value)
![[Pasted image 20260215234227.png | 700]]

- failure cases
	- a value is accepted by minority -> it will be overwritten
	- a value is accepted by majority (quorum) -> it will be proposed again, and proposer is forced to complete it
	- a value is accepted by majority, but some of these acceptors in next quorum crash
		- with persistence, the system works perfectly
		- without persistence, the system violates consistency

### multi-paxos
- a distinguished proposer as leader to skip prepare/promise phase. Only new proposer has to perform this phase
- use **leases**: the leader periodically contacts to participants, and they must respond and allow the leader to continue operation (not accept proposals from other leaders in period of lease)
### fast paxos
- it reduces latency by allowing client sends its value to acceptors directly (reduce network hop - leader)
- it needs **fast quorum** (~75% of nodes) to handle collisions
### flexible paxos
- it needn't majority but prepare quorum and accept quorum must share at least one node

| **Feature**       | **Classic Paxos**                   | **Fast Paxos**                           | **Flexible Paxos**            |
| ----------------- | ----------------------------------- | ---------------------------------------- | ----------------------------- |
| **Primary Goal**  | Consistency                         | **Lower Latency**                        | **Grid Scalability**          |
| **Network Hops**  | 2 (Client-Leader-Nodes)             | **1** (Client-Nodes)                     | 2 (Standard)                  |
| **Quorum Size**   | Simple Majority ($\frac{N}{2} + 1$) | **Fast Quorum** ($\approx \frac{3N}{4}$) | **Custom** ($Q_p + Q_a > N$)  |
| **Best Use Case** | General purpose                     | Low-latency local networks               | Massively distributed systems |
# raft
- 3 roles
	- candidate: a temporary state. a participant must be a candidate before it becomes the leader by collection a majority of votes
	- leader: handles client requests and interacts with replicated state machine in period of time, called **term**
	- follower: persists log entries and responds to requests of leader/candidate (is acceptor/learner of paxos). every process begins as a follower

	=> candidate -> leader: voting
	=> follower -> candidate: election timeout (not receiving leader's heartbeats in a randomized period of time - randomized timeout). raft uses randomized timeout to prevent split votes (most/all of nodes become candidates)

- time is divided into terms (epochs). during it, leader is unique and stable

### raft algorithm
- 3 phases
	- leader election: a candidate collects a majority of votes to become new leader
	- periodic heartbeats: the leader periodically sends heartbeats to maintain its term
	- replication/broadcast
![[Pasted image 20260216002137.png | 700]]

- failure scenarios
	- split vote: no candidate collects a majority of votes

### byzantine consensus - practical byzantine fault tolerance (PBFT)
- for both safety and liveness, no more than (N-1)/3 replicas can be faulty
- PBFT uses **view** to distinguish cluster configurations (1 replica is primary and the rest are backups)
- 3 phases
	- pre-prepare: the primary sends prepare message (with view id, ...)
	- prepare: the backup accepts prepare message if its view matches view of the primary
	- commit: the primary broadcasts commit message and waits `2f+1` messages from participants
	![[Pasted image 20260216003547.png | 700]]

# paxos vs raft
- paxos: mathematical flexibility and decentralization
- raft: structural rigidity and predictable flow
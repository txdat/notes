# failure detection
### heartbeats and pings
### gossip
- collect and distribute states of neighboring processes
![[Pasted image 20260129120230.png | 700]]
# leader election
### bully algorithm
- use participants' rank to elect new leader (with highest rank)
- if nodes are splitted into 2 or many subsets -> split brain
- ![[Pasted image 20260129120536.png | 600]]
### next-in-line failover
- each elected leader provides list of failover nodes -> select highest rank node from provided list to elect as new leader
### candidate/ordinary
### invitation algorithm
### ring algorithm
- all nodes form a ring, the election message is forwarded across the ring
- the algorithm proceeds by fully traversing the ring -> select highest rank
- ![[Pasted image 20260129121151.png | 600]]
# replication and consistency
- fault tolerance: system can continue working correctly in the presence of failures of its components
### ordering
### consistency models
- strict consistency
	- complete replication transparency, any write by any process is instantly available for all subsequent reads by any process -> theoretical model, impossible to implement
- linearizability
	- the strongest single-object, single-operation consistency model.
	- write become available to all reads at some point in time, no client can observe state transitions, side effects of partial/incomplete operations
	- defines **total order of the events**. this order is consistent, every read of shared value return latest value
	- cost:
		- synchronization instructions are expensive, slow and involve cross-node CPU and cache validations -> avoid linearizability
- sequential consistency
	- allow ordering operations as if they were executed in some sequential order
	- operations can be ordered in different ways but all processes observe the operations in the same order
	- linearizability requires operations to be globally ordered (linearizability requires order of each process and global order to be consistent)
	- main difference between linearizability and sequential consistency = absence of globally enforced time bounds
		- linearizability requires when write operation W completes -> all readers should be able to see newest values
		- in sequential consistency, results can become visible after its completion
- causal consistency
	- all processes have to see causally related operations in the same order. concurrent writes without causal relationship can be observed in a different order by processes
		![[Pasted image 20260202142731.png | 600]] | ![[Pasted image 20260202142856.png | 600]] 
	- causally consistent system guarantees that the view of database is consistent with its own actions
	- causal consistency can be implemented using logical clocks and sending context metadata with every message
	- **VECTOR CLOCK**
		- causal order allows the system to reconstruct the sequence of events even if they are out of order
		- vector clock establishes a partial order between events, detects and resolves divergence event chains
		- vector clock allows replicas to serve state reads and accepts conflict writes -> create independent chains of events
			![[Pasted image 20260212143200.png | 700]]
- session models
	- how each client observes the state of the system while issuing reads and writes
	- read-own-writes consistency model is every write issued by client is visible to it
	- monotonic reads model is if `read(x)=V` then following `read(x)` reads return V or newer values
	- monotonic writes model is client session order is visible to other sessions (same order). if not, data loss occurs
	- writes-follow-reads (session causality) is writes are ordered after writes that are observed by previous reads. if `write(x,v2)` is after `read(x)=v1` then `write(x,v2)` is after `write(x,v1)`
- eventual consistency
	- under eventual consistency (no hard time bound), updates propagate asynchronously. if there is a conflict, values from diverged replicas are reconciled using a conflict resolution
- tunable consistency
	- is eventual consistency with tunable variables where R+W > N
		- N: number of nodes that store data
		- W: number of nodes that have to acknowledge its write is success
		- R: number of nodes that have to respond its read is success
	- **QUORUMS**
		- a consistency level that consists of `floor(N/2)+1` is called quorum - a majority of nodes
		- with at least 1 node in any majority, any quorum read will observe the recentest completed quorum write
- witness replicas
	- is replicas without data persistence
	- handle node failure and maintain availability
	- witness replicas serve as tie-breakers (equal counting) in voting (for consensus) to form a quorum -> help system decide if a write should happen
- strong eventual consistency / conflict-free replicated data types (CRDTs)
	- release some consistency requirements by allowing operations to preserve additional state that allows the diverged states to be reconciled

# anti-entropy (repair inconsistencies) and dissemination (spread new updates)
### read repair
- the coordinator node sends requests to replicas, and compares their responses. the coordinator node detects inconsistencies and sends updates back to replicas that missed updates
### hinted handoff
### merkle tree
- a mechanism finds and repairs data that is not actively queried, reduces cost of reconciliation
- is a tree of hashed representation of local data
![[Pasted image 20260212153937.png | 600]]
- finding consistencies between 2 replicas -> compare hashes from their markle trees
### gossip
- gossip protocols are probabilistic communication procedures to disseminate information from one process to the rest of cluster by cooperative propagation
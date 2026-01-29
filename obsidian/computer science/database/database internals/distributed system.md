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
- causal consistency
- session models
- eventual consistency
- tunable consistency
- witness replicas
- strong eventual consistency / CRDTs
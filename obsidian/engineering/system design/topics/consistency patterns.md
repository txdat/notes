[systemdesign.one](https://systemdesign.one/consistency-patterns/)

### strong consistency
- every read on any server must return latest data (by latest write) -> data is repliacated **synchronously** across multiple servers
- adventage
	- simplify application logic
	- increase data durability
	- guarantee consistent data view across system
- disadvantage
	- reduce availability of services (data syncing takes more resources)
	- reduce latency
![[Pasted image 20241215213748.png | 400]]

### eventual consistency
- when a write is executed on a server, the next read on another server may not return latest data (by latest write), but the system will eventually converage to same state -> data is replicated **asynchronously** across multiple servers
- advantage
	- high availablity
	- scalable
	- low latency
- disadvantage
	- weaker consistency model
	- potential data loss / conflict
![[Pasted image 20241215214104.png | 400]]
### weak consistency
### linearizability
- the data written to a server must be immediately visible to subsequent reads against other servers (a variant of strong consistency - atomic consistency)
- linearizability ~ strong consistency
### causal consistency
- ~ eventual consistency (strong > causal > eventual)
- 
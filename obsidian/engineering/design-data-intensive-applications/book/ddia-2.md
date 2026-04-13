# describing performance
- response time
- throughput
![[Pasted image 20260321120525.png | 600]]


### average, median, percentiles
![[Pasted image 20260321120728.png | 600]]

- use percentiles for response time (p 50, p 95, and p 99)
- high response percentiles (tail latencies) are important because they affect user experience

# replication
### problems with replication lag
- reading your own writes -> read from same replica that has written data
- monotonic reads -> read from same replica
- consistent prefix reads (causality)

### conflict writes (multi leader replication)
- last write wins (discarding concurrent writes)
- manual conflict resolution
	- DB stores all the concurrently written values for a given record
	- DB returns all values when you query it in the next time
- automatic conflict resolution
	- CRDT
		- conflict free = commutativity (`a+b=b+a`) + associativity (`(a+b)+c=a+(b+c)`) + idempotency (`a + a ... = a`)
		- CRDT is complex and overhead (stores metadata)
	- operational transformation (OT)
- problems
	- race condition on shared resource
	- data inconsistency
- solutions
	- database locking
	- zookeeper locking
	- redis locking
# redis locking - best effort basis lock
![[Pasted image 20250530103522.png | 700]]
- redis runs all commands in **single thread**, no risk of 2 commands run concurrently
- use `SETNX` to acquire lock (only set if not exist) and `DEL` to release lock. lock **MUST** include time-to-live
- the lock is approximate, and only be used for non-critical purposes [link](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- if client holding the lock stops working, and resumes after lock is released (due to time-to-live) -> system can end up with corrupted data
- use delaying restart of crashed nodes [link](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/#performance-crash-recovery-and-fsync) for at least the longest ttl of locks
- ![[Pasted image 20250530111213.png | 600]]

### redis lock with fencing token
- every write requires a fencing token (increasing number) when acquring lock (but require token service generates **strictly motonotically increasing tokens** -> zookeeper) -> write with old token is rejected
- ![[Pasted image 20250530111519.png | 600]]
# zookeeper/etcd - correctness lock
- keep data consistent across most of servers (through quorum)
- strong consistency but heavier computation compared to redis
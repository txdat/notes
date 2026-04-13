[systemdesign.one](https://systemdesign.one/real-time-presence-platform-system-design/)

- leverage heartbeat signal through server-send event (SSE) to check status of client
- heartbeat single is **connectionless** and **lightweight** for improving performance -> use UDP

# high-level design
### data storage
- store last active time of client
- distributed key-value storage supports high read/write operations (no SQL: ACID is overkill/noSQL: slower reads) -> use redis (with sets)
- redis can use [keyspace notification](https://redis.io/docs/latest/develop/use/keyspace-notifications/) (monitor redis changes in real time) to notify connected clients when presence status changes

### pub/sub server
- servers broadcast presence status to clients through pub/sub
- redis' message bus should be confirgured in ephemeral storage mode
- limitations
	- no guarantee at least one-time message delivery
	- degraded latency if consumers use pull-based model

# deep dive design

[[live presence]]
### when user is online
- subscribers establish SSE connection to real-time platform and subscribe to any change of connection status
- real-time platform sends heartbeat signal to presence service to detect status of client, presence service publishes event to notify when status changes

### when user goes offline
- web browser/app triggers unload event to change presence status when closing app -> delayed trigger can be configured to detect absence of heartbeat signal and queries whether DB record of user has expired

### handle jittery connections
- offline and timeout events can be treated as offline, longer time interval set for timeout to prevent fluctuations status -> handle jittery connection

### pub/sub flow
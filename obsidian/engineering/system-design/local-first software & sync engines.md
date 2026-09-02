# local-first application
- use local device as primary source of truth
- zero latency (no network round-trips)
- support offline mode and data ownership
# sync engines
- client and server act as leader in an asynchronous multi-leader replication
- client -> (push op) -> server
- client <- (broadcast op) <- server

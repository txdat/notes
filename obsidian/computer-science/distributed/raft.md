# Raft

# Leader Election
- randomized election timeout (150–300ms)
- RequestVote RPC
- vote counting with majority quorum
- term update on higher term

# Log Replication
- AppendEntries RPC
- nextIndex / matchIndex
- commit index advances on majority

# Leader Completeness Property

# Persistence
- currentTerm, votedFor, log entries

# Snapshots and Log Compaction

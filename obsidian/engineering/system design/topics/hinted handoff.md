[systemdesign.one](https://systemdesign.one/hinted-handoff/)

# requirements
- **high write** availability
- scalable
- eventually consistency


# hinted handoff
- distributed system pattern to perform repairs in the write path, post-failure data (as hints - metadata?) comes from backup node (coordinator) to target node when it is healthy again
- some DBMSs store hints for a certain time frames, and flush to disk-based storage, some DBMSs store in local directory
- hints can be rejected if target node remains unavailable, or gets decommissioned?

# sloppy quorum - hinted handoff
- traditional quorum is **not fault-toleration** when network partition happens or some nodes become unavailable (constraint of r/w nodes cannot be reached)
- sloppy quorum leverages hinted handoff (temporary backup nodes accept writes/hints) to reach quorum -> keep availability for writes
- drawback of sloppy quorum is clients may read stale data (delayed consistency - reads come before hints are delivered to designed nodes), DMBSs dont allow read directly from coordinators

![[Pasted image 20250525233435.png | 600]]
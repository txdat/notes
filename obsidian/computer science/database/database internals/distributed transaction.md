# atomic commitment
- it doesn't allow disagreement between participants -> a transaction will not commit if even one of participants votes against it
# 2-phase commit
- contains
	- a leader/coordinator that holds the state, collects votes
	- cohorts (other nodes) vote to accept/reject values that are proposed by the coordinator
- 2 phases
	- **prepare**: the coordinator sends propose message to all cohorts and collects/persists their votes
	- **commit/abort**
### cohort failures
- if one of cohorts is unavailable or fails during the propose phase, the coordinator will abort the transaction
### coordinator failures
- if one of cohorts doesn't receive a commit/abort command from the coordinator, it should find out which decision was made by the coordinator
- if the coordinator fails after phase 1 and before phase 2 (commit/abort), **the system will be uncertainty** -> blocking state
# 3-phase commit
- fix coordinator failures of 2PC
- 3 phases
	- prepare
	- **pre-commit**: safety buffer. the coordinator sends result to cohorts and prepare them to commit (cohorts send ACK to the coordinator)
	- commit/abort
- if ACK is not sent to the coordinator from any cohort in phase 1 and 2, transaction will be aborted

| failure point | Outcome |
| --- | --- |
| P1 | coordinator sends abort |
| P2 | coordinator sends abort |
| P3 | coordiantor ignores and finishes (transaction is committed) |
# distributed transaction models
### Calvin
### Spanner
### Percolator

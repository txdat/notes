# basic concepts and theorems

### partitioning
- split DB into multiple smaller datasets and store them in different nodes
- vertical splitting
	- multiple tables with fewer columns
- horizontal splitting (sharding)
	- stores a percentage of rows of initial tables -> potential for loss of transaction sematics
	- range partitioning
	- hash partitioning
	- consistent hashing
		- potential of non-uniform distribution of data (imbalance)

### replication
- increase availability by copying data to other nodes (data must be maintained and kept in sync)
- pessimistic replication
	- keep replicas identical to each other
- optimistic (lazy) replication - eventually consistency
	- allow replicas diverge, and converge again if they don't receive update for a period of time

#### (single) master-slave
- 1 node is master (writable) and other nodes are slave (readable)
![[Pasted image 20260711142406.png | 600]]

#### multi-master
- prefer high availability and performance to data consistency
- all nodes are writable/readable -> conflicts
	- expose conflict resolution to clients
	- last-write-wins (local clock?) -> unexpected behaviors
	- causality tracking algorithm

#### quorums
- quorum condition
	- Qr (quorum of read) + Qw (quorum of write) > N (number of nodes)
	- Qw > N/2
- why Qr > N/2 needn't?
	- Vr needn't be a majority but large enough to collide every possible write quorum

### CAP theorem
![[Pasted image 20260711151010.png | 600]]

#### PACELC theorem
- extend CAP
- in case of network partition (P), system has to choose between availability (A - AP) and consistency (C - CP), else (E) system has to choose between latency (L) and consistency (C)

### consistency / isolation

![[Pasted image 20260711161149.png | 600]]

#### consistency model
- linearizability = strong consistency
	- synchronous replication
	- operations appear to be instantaneous to external clients (subsequent reads will see the result of latest write) when thinking about a distributed system as a single node
	- writes take longer (propagate to other nodes)
	- is consistency C in CAP theorem (give up availability A in CAP)
- sequential consistency
	- no realtime guarantee
	- all operations must be seen in the same order (global order)
- causal consistency
	- only operations that are causally related need to be seen in the same order (not global order)
- eventual consistency = weak consistency
	- no guarantee for order of operations

#### isolation level
![[Pasted image 20260711215537.png | 600]]
- **anomalies**
	- dirty writes
		- a transaction overwrites a value that has previously been written by another transaction that is not committed -> violate integrity -> no rollback
	- dirty reads
		- a transaction reads a value that has been writen by another transaction that has not been committed
	- non-repeatable reads
		- a transaction reads a value twice with different values (acting on stale data)
	- phantom reads
		- a transaction does a predicate-based read (query) and another transaction updates matched items while the first transaction is running
	- lost updates
		- 2 transactions read the same value and try to update with different value
	- read skew
		- a transaction can only see partial result of another transaction
	- write skew
		- 2 transactions read the same data but modify disjoint set of data

- serializability
- repeatable read
- snapshot isolation
	- all reads made in a transaction will see a consistent snapshot of the database from the point it starts. it will commit successfully if no other transaction has updated the same data since that snapshot
- read committed
- read uncommitted

# distributed transactions

- performing some operations across multiple nodes in an atomic way
- 2 variants
	- same piece of data need to be updated in multiple replicas
	- different pieces of data residing in different nodes need to be updated atomically

### ACID of DB transaction
- Atomicity: a transaction composed of multiple operations is treated as a single unit (all or none) -> no partial failure
- Consistency: a transaction only transitions DB from 1 valid state to another valid state, maintaining DB invariants
- Isolation: if transactions happen at a time, there is no interference between them
- Durability: once transaction is committed, it will remain committed even in the case of failure

### isolation
- 2 mechanisms for concurrency control
	- pessimistic concurrency control: block a transaction if it is expected to cause violation, resume it when it is safe (reduce number of aborts/restarts of transactions)
	- optimistic concurrency control: delay the checking until the end of the transaction (a transaction is aborted if a commit violate any rule)

#### 2-phase locking (2PL)
- a pessimistic concurrency control using locks to prevent transactions from interfering
- 2 types of lock
	- write (exclusive) lock: acquired when a record is going to be written, block both read and write from another transaction
	- read (shared) lock: acquired when a record is read, blocks write from another transaction (multiple read locks can be acquired at the same time)
- 2 phases
	- expanding phase: acquire locks (without releasing)
	- shrinking phase: release locks (without acquring)

#### snapshot isolation via multiversion concurrency control (MVCC)
- an optimistic concurrency control that stores multiple versions of each record -> reads are never blocked by other transactions that are updating same data
- how it works?
	- DB keeps 2 timestamps of a transaction Tstart, Tend
	- DB reads version of record that has committed time <= Tstart, accepts write if latest version of record <= Tstart (no change)

### atomicity

#### 2-phase commit protocol (2PC)
![[Pasted image 20260712160808.png | 600]]
- 2 roles
	- coordinator
	- participants
- 2 phases
	- voting phase
		- coordinator sends the transaction to all participants. participants execute transaction and are supposed to commit, and send their votes to coordinator
	- commit phase
		- coordinator gathers all votes from participants. coordinator sends instruction to all participants to commit (all votes are yes)/abort (any vote is no) transaction
		- if a participant fails before receiving coordinator's instruction, it recovers and communicates with coordinator to find out result of pending transaction
- coordinator and all participants keep decision in write-ahead-log (WAL) to recover in case of failure
- coordinator is single point of failure, decrease the availability of system **significantly**

#### 3-phase commit protocol (3PC)
- split 1st phase of 2PC to 2 sub-phases to tackle failure of coordinator
- 3 phases
	- voting phase
	- pre-commit phase
		- if all votes are yes, coordinator sends PRE-COMMIT message to all participants and waits their ack messages
		- if coordinator fails before sending PRE-COMMIT message
			- all participants are in PREPARED -> new coordinator must issue ABORT
				- why new coordinator cannot send COMMIT even all participants are in PREPARED? -> new coordinator cannot distinguish original coordinator died before/after collecting all votes -> state-based decision, not vote-based
			- at least 1 participant is in PRE-COMMIT -> new coordinator must issue COMMIT
	- commit phase
- 3PC can resolve failure of coordinator but cannot resolve network partition. when network partition happens, participants try to unblock protocol, it can lead to split-brain situation (1 coordinator for each partition)
![[Pasted image 20260712163621.png | 600]]

#### quorum-based commit protocol (extended 3PC)
![[Pasted image 20260712172253.png | 600]]
- address 3PC weakness (requires synchronous network and all participant availability) by using quorum
	- Qp (quorum of prepare) + Qpc (quorum of pre-commit) > N
	- Qpc + Qc (quorum of commit) > N
- 3 sub-protocols
	- share a common state model and quorum intersection guarantees
	- commit protocol
		- similar to 3PC, wait target quorum in each phase
		- coordinator waits commit quorum of ACK because of recovery protocol requirement
			- for the recovery works correctly (participant queries a quorum of participants to determine transaction outcome), a quorum of participants must know the commit decision before coordinator considers transaction done
	- termination protocol
		- fires when a participant times out waiting for coordinator message
			- PREPARED
				- all PREPARED -> ABORT
				- any PRE-COMMITTED/COMMITTED -> COMMIT
			- PRE-COMMITTED
				- any COMMITTED -> COMMIT
				- all PRE-COMMITTED/PREPARED -> COMMIT
			- COMMITTED
	- merge/recovery protocol
		- failed participant P recovers
			- any COMMITTED -> COMMIT
			- any ABORTED -> ABORT
			- all PRE-COMMITED -> COMMIT (a full prepare quorum was reached and coordinator had decided to commit)
			- all PREPARED/INIT -> ABORT
   ```
NORMAL PATH: COMMIT PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

Coordinator        N1          N2          N3          N4          N5
    │               │           │           │           │           │
    │──── PREPARE ─────────────────────────────────────────────────>│
    │               │           │           │           │           │
    │<─── YES ──────│           │           │           │           │
    │<─── YES ──────────────────│           │           │           │
    │<─── YES ──────────────────────────────│           │           │
    │<─── YES ──────────────────────────────────────────│           │
    │                                                               │
    │   Qp=4 reached. Decide COMMIT.                                │
    │                                                               │
    │──── PRE-COMMIT ──────────────────────────────────────────────>│
    │               │           │           │           │           │
    │<─── ACK ──────│           │           │           │           │
    │<─── ACK ──────────────────│           │           │           │
    │<─── ACK ──────────────────────────────│           │           │
    │<─── ACK ──────────────────────────────────────────│           │
    │                                                               │
    │   Qpc=4 reached. Safe to commit.                              │
    │                                                               │
    │──── DO-COMMIT ───────────────────────────────────────────────>│
    │               │           │           │           │           │
    │<─── ACK ──────│           │           │           │           │
    │<─── ACK ──────────────────│           │           │           │
    │<─── ACK ──────────────────────────────│           │           │
    │<─── ACK ──────────────────────────────────────────│           │
    │                                                               │
    │   Qc=4 reached. Transaction DONE.                             │
    │                                                               │

Node states after commit protocol:
┌────┬────┬────┬────┬────┐
│ N1 │ N2 │ N3 │ N4 │ N5 │
│ CM │ CM │ CM │ CM │ PC │  CM=COMMITTED, PC=PRE-COMMITTED
└────┴────┴────┴────┴────┘
N5 missed DO-COMMIT (slow network). Coordinator re-drives or N5 self-recovers.


═══════════════════════════════════════════════════════════════════════════════
FAILURE PATH: TERMINATION PROTOCOL
(Coordinator crashes after Qpc reached, before sending DO-COMMIT)
═══════════════════════════════════════════════════════════════════════════════

Coordinator        N1          N2          N3          N4          N5
    │               │           │           │           │           │
    │──── PRE-COMMIT sent, Qpc=4 ACKed ────>│           │           │
    │                                                               │
    X  ← coordinator crashes here                                   │
                    │           │           │           │           │
                    │  timeout  │  timeout  │  timeout  │           │
                    │           │           │           │           │

All nodes: PRE-COMMITTED, waiting for DO-COMMIT. Timer expires.

─────────────────────────────────────────────────────────────────────────────
TERMINATION PROTOCOL FIRES
─────────────────────────────────────────────────────────────────────────────

                   N1 elected as new coordinator

New Coord(N1)      N1          N2          N3          N4          N5
    │               │           │           │           │           │
    │──── STATE? ──────────────────────────────────────────────────>│
    │               │           │           │           │           │
    │<─── PRE-COMMITTED ────────│           │           │           │
    │<─── PRE-COMMITTED ────────────────────│           │           │
    │<─── PRE-COMMITTED ────────────────────────────────│           │
    │                                                               │
    │  Quorum(4) all PRE-COMMITTED                                  │
    │  → PRE-COMMITTED proves commit decision was made              │
    │  → must COMMIT                                                │
    │                                                               │
    │──── DO-COMMIT ───────────────────────────────────────────────>│
    │               │           │           │           │           │
    │<─── ACK ──────────────────│           │           │           │
    │<─── ACK ──────────────────────────────│           │           │
    │<─── ACK ──────────────────────────────────────────│           │
    │<─── ACK ──────────────────────────────────────────────────────│
    │                                                               │
    │  Qc=4 reached. Transaction DONE.                              │

Node states after termination protocol:
┌────┬────┬────┬────┬────┐
│ N1 │ N2 │ N3 │ N4 │ N5 │
│ CM │ CM │ CM │ CM │ CM │
└────┴────┴────┴────┴────┘
Indistinguishable from commit protocol completing normally.


═══════════════════════════════════════════════════════════════════════════════
REJOIN PATH: RECOVERY PROTOCOL
(N3 was down during entire transaction, rejoins after termination completes)
═══════════════════════════════════════════════════════════════════════════════

                                       N3 recovers
                                       reads WAL → in-doubt transaction T
                                            │
                                            │──── STATE for T? ────> N1,N2,N4,N5
                                            │                              │
                                            │<─── COMMITTED ───────────────│ N1
                                            │<─── COMMITTED ───────────────│ N2
                                            │<─── COMMITTED ───────────────│ N4
                                            │<─── COMMITTED ───────────────│ N5
                                            │
                                            │  Quorum(4) all COMMITTED
                                            │  → write COMMITTED to WAL
                                            │  → release locks
                                            │  → done

Node states after recovery protocol:
┌────┬────┬────┬────┬────┐
│ N1 │ N2 │ N3 │ N4 │ N5 │
│ CM │ CM │ CM │ CM │ CM │
└────┴────┴────┴────┴────┘


═══════════════════════════════════════════════════════════════════════════════
RECOVERY: MIXED STATE CASE
(N3 recovers, finds peers in mixed PREPARED + PRE-COMMITTED state)
═══════════════════════════════════════════════════════════════════════════════

                                       N3 recovers, queries quorum
                                            │
                                            │──── STATE for T? ────> N1,N2,N4,N5
                                            │                              │
                                            │<─── PREPARED ────────────────│ N1
                                            │<─── PREPARED ────────────────│ N2
                                            │<─── PRE-COMMITTED ───────────│ N4
                                            │<─── PRE-COMMITTED ───────────│ N5
                                            │
                                            │  Mix seen. PRE-COMMITTED exists.
                                            │  → commit decision was made
                                            │  → N3 becomes new coordinator
                                            │  → drive remaining PREPARED nodes
                                            │    to PRE-COMMITTED first

New Coord(N3)                          N3        N1    N2    N4    N5
    │                                   │         │     │     │     │
    │──── PRE-COMMIT ───────────────────────────> │     │     │     │
    │                                             │     │     │     │
    │<─── ACK ─────────────────────────────────── │     │     │     │
    │<─── ACK ──────────────────────────────────────────│     │     │
    │                                                         │     │
    │  Qpc=4 reached (N1,N2,N4,N5)                            │     │
    │                                                         │     │
    │──── DO-COMMIT ───────────────────────────────────────────────>│
    │<─── ACK (all 4) ──────────────────────────────────────────────│
    │                                                               │
    │  Qc=4 reached. Transaction DONE.

Node states after recovery protocol:
┌────┬────┬────┬────┬────┐
│ N1 │ N2 │ N3 │ N4 │ N5 │
│ CM │ CM │ CM │ CM │ CM │
└────┴────┴────┴────┴────┘


═══════════════════════════════════════════════════════════════════════════════
HANDOFF MAP — HOW PROTOCOLS CHAIN
═══════════════════════════════════════════════════════════════════════════════

  COMMIT PROTOCOL
  ┌─────────────────────────────────────────────────────────────┐
  │  PREPARE → collect Qp → PRE-COMMIT → collect Qpc            │
  │  → DO-COMMIT → collect Qc → DONE                            │
  └──────────────────┬──────────────────┬───────────────────────┘
                     │ coordinator fails │ node fails
                     ▼                  ▼
  TERMINATION        │        RECOVERY PROTOCOL
  PROTOCOL           │        ┌──────────────────────────────────┐
  ┌──────────────────┴──┐     │  query quorum for state          │
  │  elect coordinator  │     │                                  │
  │  query peer states  │     │  COMMITTED    → apply commit     │
  │                     │     │  ABORTED      → apply abort      │
  │  COMMITTED  → COMMIT│     │  all PRE-CM   → drive termination│
  │  PRE-CM     → COMMIT│     │  all PREPARED → drive termination│
  │  PREPARED   → ABORT │     │  mixed        → drive termination│
  │                     │     └──────────────┬───────────────────┘
  │  drive to terminal  │                    │
  │  state via Qc ACKs  │                    │ if in-doubt
  └──────────┬──────────┘                    │
             │                               │
             └───────────────────────────────┘
             both produce terminal state (CM or AB)
             discoverable by future recovery quorum
             guaranteed by Qpc+Qc>N intersection


═══════════════════════════════════════════════════════════════════════════════
STATE DECISION MATRIX (used by both termination and recovery)
═══════════════════════════════════════════════════════════════════════════════

  Quorum response          Decision        Reason
  ──────────────────────── ─────────────── ───────────────────────────────────
  any COMMITTED            COMMIT          terminal state reached, match it
  any ABORTED              ABORT           terminal state reached, match it
  all PRE-COMMITTED        COMMIT          commit decision proven, drive it
  mix PREPARED+PRE-CM      COMMIT          PRE-CM proves decision, drive it
  all PREPARED             ABORT           no decision made, safe to abort
  all INIT                 ABORT           transaction never started

   ```
- failure scenarios
	- durability violation: commit quorum not reached
		```
N = 7, Qc = 4
coordinator sends DO_COMMIT to all 7, but receives 3 ACK before crash

termination protocol fires -> new elected coordinator queries states -> any COMMITTED, issue COMMIT
all COMMITTED nodes crash -> new elected coordinator sees only PRE-COMMIT
	- allow COMMIT from PRE-COMMIT quorum
	- abort -> 4 ABORTED, 3 COMMITTED (after recover) -> split brain
		```
		- additional mechanisms for durability
			- persistent WAL before ACK
			- consensus underneath (raft/paxos): spanner (2PC over paxos)
### long-lived transaction & saga
![[Pasted image 20260712174935.png | 600]]
- saga is sequence of local transactions (trigger next transaction by message/event) that can be interleaved with other sagas with atomic guarantee. each of transaction T in saga is associated with compensating transaction C for rollback
- 2 execution models
	- choreography
		- no central coordinator, services listen event and react
		```
OrderService          PaymentService        InventoryService
     │                       │                      │
  T1: create order           │                      │
     │──── OrderCreated ────>│                      │
     │                    T2: charge card           │
     │                       │──── PaymentDone ────>│
     │                       │                   T3: reserve stock
     │                       │                      │──── StockReserved
     │                       │                      │
     │                       │    <── StockFailed ──│  (failure)
     │                       │                      │
     │          <── PaymentFailed ──────────────────│
     │                    C2: refund card           │
  C1: cancel order           │                      │

		```
	- orchestration
		- central coordinator drives sequence of transactions
		```
Orchestrator      OrderService   PaymentService   InventoryService
     │                 │               │                 │
     │──── T1 ────────>│               │                 │
     │<─── success ────│               │                 │
     │──── T2 ─────────────────────────│                 │
     │<─── success ────────────────────│                 │
     │──── T3 ──────────────────────────────────────────>│
     │<─── FAIL ──────────────────────────────────────── │
     │                 │               │                 │
     │──── C2 ─────────────────────────│                 │  compensate
     │<─── ACK ────────────────────────│                 │
     │──── C1 ────────>│               │                 │  compensate
     │<─── ACK ────────│               │                 │
     │                 │               │                 │
   DONE (compensated)

		```

- drawbacks
	- no isolation guarantee between concurrent sagas
	- compenstating transactions are not true rollback
		- compensating transaction must be idempotent, commutative (concurrent compenstations shouldn't conflict), always possible (some operations cannot be compensated)

### when to use
- strong ACID across DB shars, same infra, short tx -> 2PC (with consensus underneath for HA)
- long-running business process across services -> saga
- non-blocking distributed commit -> 3PC/ quorum-based 3PC
# concensus

# time - order

# case studies and practice patterns
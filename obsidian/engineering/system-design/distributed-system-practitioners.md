# basic concepts and theorems

### partitioning
- split DB into multiple smaller datasets and store them in different nodes
- vertical splitting
	- multiple tables with fewer columns
- horizontal splitting (sharding)
	- stores a percentage of rows of initial tables -> potential for loss of transaction semantics
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
- eventual consistency (a weak consistency model, not a synonym for the whole category)
	- no guarantee for order of operations, only that replicas converge if updates stop

#### isolation level
![[Pasted image 20260711215537.png | 600]]
- **anomalies**
	- dirty writes
		- a transaction overwrites a value that has previously been written by another transaction that is not committed -> violate integrity -> no rollback
	- dirty reads
		- a transaction reads a value that has been written by another transaction that has not been committed
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
	- all reads made in a transaction will see a consistent snapshot of the database from the point it starts. it will commit successfully if no other transaction has updated the same data since that snapshot (first-committer-wins)
	- prevents dirty reads, non-repeatable reads, read skew and lost updates, but **NOT write skew** (the 2 transactions touch disjoint data, so there is no write-write conflict to detect)
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
	- shrinking phase: release locks (without acquiring)
- 2PL guarantees serializability. strict 2PL (hold all locks until commit/abort) additionally avoids cascading aborts

#### snapshot isolation via multiversion concurrency control (MVCC)
- MVCC itself is a *storage* technique (keep multiple versions of each record), not a concurrency-control discipline -> reads are never blocked by other transactions that are updating same data
	- it underpins optimistic schemes (snapshot isolation with first-committer-wins) and pessimistic ones alike (2PL for writers + MVCC snapshot readers, e.g. SQL Server RCSI)
- snapshot isolation on top of MVCC is optimistic: the write-conflict check is deferred to commit time
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
- 2PC is a **blocking** protocol: a participant that has voted yes is *in-doubt* and cannot unilaterally decide. it must hold its locks until the coordinator comes back -> other transactions touching the same data stall too

#### 3-phase commit protocol (3PC)
- split 1st phase of 2PC to 2 sub-phases to tackle failure of coordinator
- 3 phases
	- voting phase
	- pre-commit phase
		- if all votes are yes, coordinator sends PRE-COMMIT message to all participants and waits their ack messages
		- if coordinator fails before sending PRE-COMMIT message
			- all **reachable** participants are in PREPARED -> new coordinator must issue ABORT
				- why cannot send COMMIT even if every reachable participant is in PREPARED? -> an unreachable/crashed participant may have voted NO, in which case the original coordinator had already decided ABORT. no participant has pre-committed, so nobody can have committed -> ABORT is the only decision that is safe against an unseen NO voter
			- at least 1 participant is in PRE-COMMIT -> new coordinator must issue COMMIT
				- PRE-COMMIT can only have been sent after the original coordinator collected all YES votes -> its existence *proves* the decision was COMMIT -> state-based decision, not vote-based
	- commit phase
- 3PC can resolve failure of coordinator but cannot resolve network partition. when network partition happens, participants try to unblock protocol, it can lead to split-brain situation (1 coordinator for each partition)
![[Pasted image 20260712163621.png | 600]]

#### quorum-based commit protocol (extended 3PC)
![[Pasted image 20260712172253.png | 600]]
- address 3PC weakness (requires synchronous network and all participant availability) by using quorum
- **quorum conditions** (Skeen). the protocol is parameterized by a commit quorum Vc and an abort quorum Va:
	- `Vc + Va > N` -> **the load-bearing rule**. no set of nodes can gather a commit quorum while a disjoint set (e.g. on the other side of a partition) gathers an abort quorum -> the 2 decisions are mutually exclusive -> no split-brain
	- `Vc > N/2` is *not* required on its own; what is required is the intersection above (plus Va >= 1, Vc >= 1)
	- the prepare/pre-commit/commit rounds each wait for their target quorum before advancing
- 3 sub-protocols
	- share a common state model and quorum intersection guarantees
	- commit protocol
		- similar to 3PC, wait target quorum in each phase
		- coordinator waits commit quorum of ACK because of recovery protocol requirement
			- for the recovery works correctly (participant queries a quorum of participants to determine transaction outcome), a quorum of participants must know the commit decision before coordinator considers transaction done
	- termination protocol
		- fires when a participant times out waiting for coordinator message. it elects a new coordinator, which queries peer states and **must reach a quorum of responses** — if it cannot, it stays blocked (this is the price of safety under partition)
			- any COMMITTED -> COMMIT (terminal state already reached)
			- any ABORTED -> ABORT (terminal state already reached)
			- any PRE-COMMITTED (rest PREPARED) -> drive the PREPARED nodes to PRE-COMMIT, then COMMIT once Vc is reached
			- all PREPARED, and an abort quorum Va is reachable -> ABORT
			- all INIT -> ABORT
	- merge/recovery protocol
		- failed participant P recovers, finds an in-doubt transaction in its WAL, and queries a quorum of peers. same decision table as termination
			- any COMMITTED -> COMMIT
			- any ABORTED -> ABORT
			- all PRE-COMMITTED -> COMMIT (a full prepare quorum was reached and coordinator had decided to commit)
			- all PREPARED/INIT -> ABORT
		- a node that cannot reach a quorum stays in-doubt and keeps its locks — it may **not** decide unilaterally

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
                                           (needs an abort quorum Va)
  all INIT                 ABORT           transaction never started

  SAFETY: "all PRE-COMMITTED -> COMMIT" and "all PREPARED -> ABORT" can never
  both fire, because Vc + Va > N forces the 2 quorums to intersect, and the
  node in the intersection cannot report both states.

```

- why "all PRE-COMMITTED -> COMMIT" is mandatory, not an optimization

```
N = 7, Vc = 4
coordinator sends DO_COMMIT to all 7, gets 3 ACK, then crashes

termination fires -> new coordinator sees a COMMITTED node -> issues COMMIT
now all COMMITTED nodes crash -> a later coordinator sees only PRE-COMMITTED

	- with the rule:    PRE-COMMITTED quorum -> COMMIT
	                    -> agrees with the 3 crashed nodes when they recover
	- without the rule: ABORT -> 4 ABORTED, 3 COMMITTED after recovery -> split brain

=> PRE-COMMITTED must be treated as proof that COMMIT was decided, even though
   no node ever observed the commit quorum Vc complete
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
	- compensating transactions are not true rollback (the intermediate state was already visible to everyone)
		- compensating transaction must be idempotent, commutative (concurrent compensations shouldn't conflict), always possible (some operations cannot be compensated — an email already sent, a physical shipment)

### when to use
- strong ACID across DB shards, same infra, short tx -> 2PC (with consensus underneath for HA)
- long-running business process across services -> saga
- non-blocking distributed commit -> 3PC/ quorum-based 3PC
# consensus
- all N nodes in distributed system agree on a single value v, satisfy these properties
	- termination: every non-faulty node must eventually decide
	- agreement: final decision of every non-faulty node must be identical
	- validity: the value v must be proposed by one of the nodes

- **FLP impossibility** it is IMPOSSIBLE for a deterministic consensus algorithm to guarantee all three simultaneously in an asynchronous system, **even if only a single node may crash** (the impossibility is about *termination*: a slow node and a dead node are indistinguishable without timing assumptions)
	- practical algorithms escape it by giving up determinism (randomization) or pure asynchrony (timeouts / partial synchrony — what raft and paxos do). they keep safety always and get liveness only when the network behaves

### paxos algorithm
![[Pasted image 20260714165235.png | 600]]
- system will come to an agreement, tolerating the failure of any number of nodes if more than half the nodes are working properly at any time
- 3 roles
	- proposers
		- propose values to the acceptors and persuade them to accept them
	- acceptors
		- receive proposals and reply their decisions
	- learners
		- keep outcomes of consensus, potentially act on them
- algorithm
```
Phase 1a:  proposer picks n > any n it has used before
           sends prepare(n) to majority

Phase 1b:  acceptor receives prepare(n)
           if n > highest_promised:
               highest_promised = n
               reply promise(n, accepted_ballot, accepted_value)
           else:
               reject/ignore

Phase 2a:  proposer receives promise from majority
           if any promise has accepted_value != null:
               V = accepted_value from promise with highest accepted_ballot
           else:
               V = proposer's own value
           send accept(n, V) to majority (can be same or different majority)

Phase 2b:  acceptor receives accept(n, V)
           if n >= highest_promised:
               accepted_ballot = n
               accepted_value = V
               reply accepted(n, V)
           else:
               reject/ignore

Phase 3:   learner sees accepted(n, V) from majority → value V is chosen
```
### raft
- establishes the concept of a replicated state machine and the associated replicated log of commands with multiple consecutive rounds of consensus
- 3 states
	![[Pasted image 20260714224737.png | 400]]
	- leader
		- receives proposals and replicates them to following nodes to reach consensus
		- send heartbeats to other nodes to maintain its leadership
		- fallbacks to follower if another node gains leadership
	- follower
	- candidate
		- is middle state (follower -> leader) in leader election after original leader crashes
- use temporal terms to prevent 2 leaders operating concurrently. in each term, a candidate becomes the leader (receives votes from majority of nodes)
- an entry is committed if leader receives `append` responses from majority of nodes **AND the entry belongs to the leader's current term**
	- a leader may **NOT** commit an entry from a *previous* term just because it is now replicated on a majority (raft paper, figure 8: such an entry can still be overwritten by a future leader). those entries are committed *indirectly*, once an entry from the current term commits on top of them — the log matching property then makes all preceding entries committed too
	- in practice a new leader appends a no-op entry in its own term to flush this out
- raft guarantees
	- committed entries are durable and are executed eventually by all available state machines
	- no 2 committed entries have same index
	- if an entry is committed, all preceding entries are committed
- temporary divergence
	- any elected leader has all committed entries up to term it becomes leader -> help followers converge (leader **ONLY** appends entries to its log, while followers can update them)
	- followers must vote to candidate having more up-to-date log

# time - order
- no global clock to order events happening on different nodes of distributed system

### total/partial ordering
- total ordering is a binary relation that can be used to compare any 2 elements -> only 1 order for all elements
- partial ordering is a binary relation that can be used to compare only some of elements

### causality
- causal consistency model ensures that events that are causally related are observed in a single order

### lamport clock
- each node maintains a logical clock (numeric counter)

```
- increase C_i (C_i+1) before executing an event
- a node receives message with C_msg, C_i = max(C_i, C_msg), increase C_i by 1 and delivers message
```

- satisfies the **clock condition** (`Ei -> Ej  =>  C_Ei < C_Ej`) but NOT the **strong clock condition** (the converse fails): `C_Ei < C_Ej` tells you nothing, Ei and Ej may be concurrent -> cannot be used to infer causality

#### why merge THEN increment? (and why vector clock doesn't care)
- on receive, lamport is **forced** into `C_i = max(C_i, C_msg) + 1`. the `+1` MUST come last

```
receiver is behind: C_i = 2, message arrives with C_msg = 9

merge-then-increment:  max(2, 9) + 1 = 10        OK, 10 > 9
increment-then-merge:  max(2 + 1, 9) = 9         BROKEN, receive == send
```

- the receive event would carry the same timestamp as the send event that caused it -> 2 causally ordered events with equal timestamps -> clock condition (which demands **strict** `<`) is violated
- root cause: lamport collapses the whole vector into a single number, so that one number must do both jobs — absorb the sender's knowledge (max) AND strictly advance past it (+1). only max-then-increment does both

- **vector clock has no such constraint**: increment and merge touch disjoint slots, so they commute and either order gives the same vector
	- node i only ever increments its OWN slot `C_i[i]`
	- the merge can never change slot i: `C_j[i]` is j's belief about i's counter, and j only ever learned it FROM i (directly or transitively) -> `C_j[i] <= C_i[i]` always -> `max(C_i[i], C_j[i]) = C_i[i]`, a no-op
	- deeper reason: the merge alone already makes the receiver `>=` the sender in EVERY slot, so the `+1` on its own slot is what makes it strictly greater. no single scalar has to carry both duties

### vector clock
- vector of N counters (N is number of nodes), clock of i-th node is `[C_i1, C_i2, ..., C_iN]`

```
- increase C_ii (C_ii+1) before sending message
- when i-th node receives message from j-th node, increase C_ii by 1, for each k in 1..N, C_ik=max(C_ik,C_jk) and delivers message
```

- merge and increment **commute** here (see above) -> the order in the rule above is arbitrary, unlike lamport
- satisfies strong clock condition. `C_Ei < C_Ej  <=>  Ei -> Ej` (causal relationship). incomparable vectors = concurrent events
![[Pasted image 20260715010651.png | 600]]

### version vector
- every data item is tagged with a version vector in DB -> can be updated in multiple parts concurrently -> reconcile in conflict resolution
- for a data item x, `V[x]` is a vector with one slot per node: `V[x] = [v1, v2, ..., vN]`

```
- all slots init to 0
- if i-th node updates x, it increases its OWN slot: V[x][i] += 1
- if i-th and j-th nodes sync x, both take the element-wise max over ALL slots:
      for each k in 1..N: V[x][k] = max(Vi[x][k], Vj[x][k])
```

- compare 2 version vectors of x: one dominates (>= in every slot) -> it is newer, discard the other. neither dominates -> concurrent updates -> **conflict**, hand to the resolver (siblings in dynamo/riak, LWW, app-level merge)
- vector clock tracks *events per node*, version vector tracks *updates per replica of one data item* — same math, different subject

#### version vector vs MVCC — NOT the same thing
- both keep multiple "versions", but they solve different problems and are **not** used together in the usual case

| | MVCC | version vector |
|---|---|---|
| problem | isolation between concurrent **transactions** on one logical DB | conflict detection between concurrent **writes on different replicas** |
| ordering | a **total** order: monotonic txid / commit timestamp from a single authority | a **partial** order: concurrency is a first-class, detectable outcome |
| on 2 conflicting writes | one must abort (or block) — never a conflict left for the app | keep both as siblings, resolve later |
| where | postgres (xmin/xmax), mysql innodb, oracle | dynamo, riak, voldemort, cassandra-style multi-master |

- MVCC does not need a version vector because it has a **single point of truth for time** (the transaction id counter / commit timestamp), so every version is comparable -> a scalar suffices. version vectors exist precisely because leaderless/multi-master replication has **no such authority**
- distributed MVCC systems still use scalars, just better ones: spanner = TrueTime commit timestamps, cockroachdb/yugabyte = hybrid logical clocks (HLC = physical time + lamport counter). they buy back a total order rather than tracking causality per item
- so: **MVCC -> scalar versions, single writer/authority. version vector -> causal versions, many writers**

# case studies and practice patterns
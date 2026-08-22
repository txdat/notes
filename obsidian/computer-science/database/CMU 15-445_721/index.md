# hash tables

# indexes & filters

- a subset of table's attributes that is organized/sorted for efficient access to location of tuples

### index

- b-tree
  - is a self-balancing tree that keeps data sorted, complexity is O(log(n))
  - is m-way search tree (m is fanout)
    	![[Pasted image 20260728221425.png | 400]]

### filter

- bloom filter
  - is a probabilistic filter using bitmap. it can return false positve results, but no false negative
- skip list
- trie
- inverted index

### index concurrency control

### lock/latch

- lock: high level, logical primitive, protects the contents of DB
- latch: low level, primitive for DB internal data structure
  - read latch: a worker can acquire the latch in read mode, even if another thread has already acquired
  - write latch: only 1 worker is allowed to access the item. a worker holds a write latch prevents other workers acquire a read latch

### latch implementation

- use atomic instructions (CPU)
- Test-and-Set spin latch (TAS)
- Blocking OS mutex (OS built-in mutex)
- Reader-Writer latches
  - a latch can be held in either read or write mode -> manage read/write queues

### hash table latching

### b-tree latching

- prevent
  - threads trying to modify the contents of a node at the same time
  - 1 thread traversing the tree while another thread splits/merges nodes
- latch crabbing protocol

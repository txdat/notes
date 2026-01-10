- balanced search tree with high fanout (improve locality of neighboring keys) and low height (reduce number of seeks during traversal)
- keys in b-tree node are stored in order

# structure
- page header
- magic number
- sibling links (neighbors)
![[Pasted image 20260101172120.png | 600]]
- rightmost pointer (k keys -> k+1 children)
- overflow pages
	- b-tree node keeps a specific number of items -> variable-size node = multiple linked pages (overflow pages)
	- ![[Pasted image 20260101172554.png | 300]]

# b-tree variants
### copy on write
- use copy-on-write instead of latching for data integrity
- ![[Pasted image 20260105164019.png | 600]]
- advantages
	- readers require no synchronization, writer doesn't block readers (writen pages are immutable -> no latching)
- disadvantages
	- requires more storage and processing time, but b-tree is shallow -> it is acceptable
### lazy b-tree
- lightweight, concurrency, update-friendly in-memory structures to buffer updates, and propagate later
- reduce random IO by batching updates
#### WiredTiger/MongoDB
- buffering updates to individual nodes
- materialize node in memory while it is paged until it is flushed
- update buffers are accessed during reads (merged with original data on disk)
- page updates and structural modifications run on background -> reads/writes needn't wait
#### lazy-adaptive tree
- buffering updates to subtree, and propagate changes to lower levels (to leaf nodes) when buffer becomes full
### FD-tree
- minimize random writes by converting them to sequential merges
#### fractional cascading
- to locate item in multiple sorted arrays. complexity is O(k+logn) instead of O(klogn) (use binary search on each array)
### BW-tree
- batch updates to nods by append-only storage, use in-memory data structure that allow installing pointers between nodes -> make tree latch-free
- high concurrency, no cache validation
### cache-oblivious b-tree
### introduction
- database systems are splitted into:
	- 3 major categories
		- online transaction processing (OLTP): amount of transactions, but they are predefined and short-lived
		- online analytical processing (OLAP): complex aggregations, handling complex, long-runnning ad-hoc queries
		- hybrid: mixed of OLTP and OLAP
	- where to store data
		- in-memory (with backup + log (snapshot) for restoring)
		- hard disk
	- data layouts
		- row
			- store data on records (rows) ~ tabular representation
		- column
			- partition data vertically instead of storing in a row (values from 1 column are stored together)
- buffering, immutability, and ordering
	- buffering
		- group amount of data in memory before put it into disk
	- mutability/immutability
		- mutability: read/write data on the same location of file
		- immutability: appled-only (written data cannot be modified)
	- ordering
		- data is stored in the key order of pages on disk
### b-tree
[b-tree](https://www.scaler.in/b-tree/)
- balanced tree height is log2N (N is number of nodes in tree) and height difference between 2 subtrees (from root) must be less than or equal 1
- optimal balanced tree for on-disk structures (external search)
	- high fanout (number of childrens) -> improve locality of neightboring keys
	- low height -> number of seeks during traversal
- b-tree contains multiple nodes, each node holds up to N keys and N+1 pointers to its child nodes. b-tree is page organization technique (fixed size page organization)
- b-tree is characterized by **fan-out** : number of keys that are stored in each node. higher fan-out amortize the cost to balance tree and reduce number of seeks by storing keys and pointers in single or consecutive blocks
![[Pasted image 20250101204213.png | 600]]

![[Pasted image 20250101204321.png | 600]]

#### properties of b-tree (fan-out is m)
- all leaves of b-tree are same level (depth)
- all keys in each node are sorted ascending (for binary search)
- a non-leaf node has at least m/2-1 keys and m/2 child nodes

#### b-tree lookup algorithm
- complexity: = number of block transfers + number of comparisons
	- M is total number of items (leafs), K is number of keys in node (fan-out)
		-> number of block transfers = logK(M), number of comparisons = log(M)
#### node splits
- locate target node and append key/value to it
- if node doesnt have enough room -> split in two (overflow)
- splits: allocation new node, move half the elements from current node to new node, and add first key (if target node is leaf, or move key if target node is non-leaf) and pointer to parent node (and continue process if parent node's room is not enough)
![[Pasted image 20250101213125.png | 600]]

![[Pasted image 20250101213149.png | 600]]
#### node merges
- locate target node and delete it key and value
- if node doesnt have enough keys and pointers (underflow) -> merge two nodes into 1
![[Pasted image 20250101213803.png | 600]]

![[Pasted image 20250101213824.png | 600]]
### file formats
- B-tree is page management mechanism
- slotted pages
![[Pasted image 20250114092537.png | 600]]
![[Pasted image 20250114092604.png | 600]] delete cell2 data


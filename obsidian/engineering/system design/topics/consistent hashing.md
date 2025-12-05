[[consitent hashing.excalidraw]]

[highscalability blog](https://highscalability.com/consistent-hashing-algorithm/)
[systemdesign.one blog](https://systemdesign.one/consistent-hashing-explained/)

- to distribute requests/data across servers for horizontal scaling
- rehashing problem?
	- happen when adding new servers or remove existing servers if still using current hash function
- consistent hashing is **when hash table is resized, only k/n keys need to be remapped on average, when k is number of keys, and n is number of slots**

# basic approach
- map servers and keys (requests) to the ring by using uniform distribution hash function, same hash function for both servers and requests (impossible to keep same size partitions of ring due to adding/removing servers)
- popular hashing function is MD5
- to find server for each key, go clockwise and until first server is found
- add virtual nodes for each server (a server can serve for multiple partitions of ring)
- when add/remove a server, a fraction of data need to be redistributed (move anticlockwise from removed server to first running server)

# dynamic hashing for partitioning
![[Pasted image 20250525162325.png | 600]]
# static hash partitioning
![[Pasted image 20240823153631.png | 600]]
![[Pasted image 20240823153645.png | 600]]
- using hash function with fixed number of nodes (N) to locate index, collision may occur when multiple nodes have same position
- not horizontally scalable, add/remove nodes need rehashing cached data -> massive data movement between nodes

# consistent hashing
- consistent hashing distributes hashing positions on virtual hash ring (finite fixed circular space) -> reduce re-hashing
- use same uniform and independent hashing function for both nodes and data
- the first node with greater position than key's position (follow clockwise direction) stores data of key
![[Pasted image 20240823154656.png | 600]]
### delete an existing node
![[Pasted image 20240823154803.png | 600]]
### add a new node
![[Pasted image 20240823154815.png | 600]]


- consistent hashing aid cloud computing by minimizing the movement of data when number of nodes changes due to scaling
- nodes mayn't be uniform distributed -> virtual nodes -> improve load balancing and prevent hotspots (receive too much requests). the nodes with higher capacity will have more positions (or virtual nodes) on hash ring

# optimization
- multi-probe
	- linear space complexity for storing node's position on hash ring -> no virtual node, a node is assigned only one position on hash ring
	- use **multiple hashing functions** at the same time to find nearest node for each request -> slower lookup
	- ![[Pasted image 20250525171913.png | 600]]
- bounded loads
	- set upper limit on load received by node -> average load of whole hash ring -> node is not overloaded (hotspots)
	- list of fallback nodes are similar for same request's hash -> request is redistributed among the available nodes instead of only fallback node
	- ![[Pasted image 20250525172147.png | 600]]

# implementation
- use self-balancing binary search tree (BST), each node on BST is a node on hash ring

- insert data object (key)
	- ![[Pasted image 20250525172647.png | 600]]

- add new node
	- ![[Pasted image 20250525172713.png | 600]]

- remove node
	- ![[Pasted image 20250525172853.png | 600]]

- complexity of consistent hashing
	- add/remove a node: O(k/n + logn) - O(k/n) for redistribution of keys
	- add/remove a key: O(logn) - BST traversal
	
# modulo hashing
- hash id to number, and apply modulo operation to find target server `server_id = hash(id) % number_of_servers`
- disadvantages
	- when number of servers changes, data need being redistributed -> massive data movement

# consistent hashing
- arrange both of data and servers on fixed-size hash ring
![[Pasted image 20251007014013.png | 600]]
- adding new server: some data need being redistributed (instead of whole data)
![[Pasted image 20251007014146.png | 600]]
- removing server
![[Pasted image 20251007014238.png | 600]]


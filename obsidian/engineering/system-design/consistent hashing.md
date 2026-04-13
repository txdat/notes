[[consistent hashing.excalidraw]]

[highscalability blog](https://highscalability.com/consistent-hashing-algorithm/)
[systemdesign.one blog](https://systemdesign.one/consistent-hashing-explained/)

- to distribute requests/data across servers for horizontal scaling
- rehashing problem?
	- happens when adding new servers or removing existing servers if still using current hash function
- consistent hashing is a technique where only k/n keys need to be remapped on average when a hash table is resized, where k is the number of keys and n is the number of slots

# basic approach
- map servers and keys (requests) to the ring by using a uniform distribution hash function—the same hash function for both servers and requests (impossible to keep same size partitions of ring due to adding/removing servers)
- A popular hashing function is MD5
- to find the server for each key, go clockwise until the first server is found
- add virtual nodes for each server (a server can serve multiple partitions of the ring)
- when adding/removing a server, a fraction of the data needs to be redistributed (move counter-clockwise from the removed server to the first running server)

# dynamic hashing for partitioning
![[Pasted image 20250525162325.png | 600]]
# static hash partitioning
![[Pasted image 20240823153631.png | 600]]
![[Pasted image 20240823153645.png | 600]]
- using a hash function with a fixed number of nodes (N) to locate the index, collisions may occur when multiple nodes have the same position
- not horizontally scalable; adding/removing nodes needs rehashing of cached data -> massive data movement between nodes

# consistent hashing
- consistent hashing distributes hashing positions on a virtual hash ring (finite fixed circular space) -> reduce re-hashing
- use the same uniform and independent hashing function for both nodes and data
- the first node with a greater position than the key's position (following the clockwise direction) stores the key's data
![[Pasted image 20240823154656.png | 600]]
### delete an existing node
![[Pasted image 20240823154803.png | 600]]
### add a new node
![[Pasted image 20240823154815.png | 600]]


- consistent hashing aids cloud computing by minimizing the movement of data when the number of nodes changes due to scaling
- nodes may not be uniformly distributed -> virtual nodes -> improve load balancing and prevent hotspots (receive too many requests). The nodes with higher capacity will have more positions (or virtual nodes) on the hash ring

# optimization
- multi-probe
	- Linear space complexity for storing a node's position on the hash ring -> no virtual node, a node is assigned only one position on hash ring
	- use **multiple hashing functions** at the same time to find nearest node for each request -> slower lookup
	- ![[Pasted image 20250525171913.png | 600]]
- bounded loads
	- set an upper limit on the load received by a node -> average load of whole hash ring -> node is not overloaded (hotspots)
	- the list of fallback nodes is similar for same request's hash -> request is redistributed among the available nodes instead of only fallback node
	- ![[Pasted image 20250525172147.png | 600]]

# implementation
- Use a self-balancing binary search tree (BST), each node on BST is a node on hash ring

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
	- when the number of servers changes, the data needs to be redistributed -> massive data movement

# consistent hashing
- arrange both the data and the servers on a fixed-size hash ring
![[Pasted image 20251007014013.png | 600]]
- adding a new server: some data needs to be redistributed (instead of whole data)
![[Pasted image 20251007014146.png | 600]]
- removing server
![[Pasted image 20251007014238.png | 600]]


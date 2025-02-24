[[consitent hashing.excalidraw]]
[blog](https://highscalability.com/consistent-hashing-algorithm/)
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

# static hash partitioning
![[Pasted image 20240823153631.png | 600]]
![[Pasted image 20240823153645.png | 600]]
- static hash partitioning is not horizontally scalable -> break existing mappings between keys (requests) and servers
- consistent hashing distributes hashing positions on virtual hash ring (finite fixed circular space) -> reduce re-hashing
![[Pasted image 20240823154656.png | 600]]
### delete an existing node
![[Pasted image 20240823154803.png | 600]]
### add a new node
![[Pasted image 20240823154815.png | 600]]
# optimization
- multi-probe
	- linear space complexity for storing node's position on hash ring
	- use multiple hashing functions to find nearest node for each request
- bounded loads
	- average load of whole hash ring -> node is not overloaded
	- list of fallback nodes are similar for same request's hash -> request is distributed among the available nodes instead of only fallback node
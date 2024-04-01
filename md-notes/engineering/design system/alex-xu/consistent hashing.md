- to distribute requests/data across servers for horizontal scaling
- rehashing problem?
	- happen when adding new servers or remove existing servers if still using current hash function
- consistent hashing is **when hash table is resized, only k/n keys need to be remapped on average, when k is number of keys, and n is number of slots**
[[consitent hashing.excalidraw]]

# basic approach
- map servers and keys (requests) to the ring by using uniform distribution hash function (impossible to keep same size partitions of ring due to adding/removing servers)
- to find server for each key, go clockwise and until first server is found
- add virtual nodes for each server (a server can serve for multiple partitions of ring)
- when add/remove a server, a fraction of data need to be redistributed (move anticlockwise from removed server to first running server)
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

# usage of consistent hashing
- CDN
- Cassandra DB
- Amazon Dynamo DB
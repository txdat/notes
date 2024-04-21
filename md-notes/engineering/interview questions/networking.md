1. how does TCP create, handle and close connection?
	- TCP opens a connection to determine when server is available, and the way to server before transfering data
	- use 3-step handshake
		- client send SYN (synchronization) with random sequence number A
		- server send SYN-ACK (acknowledgment) with random sequence number B and ACK number is A+1
		- client send ACK with ACK number is B+1
	- half-duplex and full-duplex connection
		- half-duplex supports either sending or receiving at a time
		- full-duplex supports both sending and receiving simultaneous -> need 3-step handshake for full-duplex connection
	- TCP close connection by sending FIN-ACK packages in 4-step
		- peer A sends FIN package to peer B
		- peer B sends ACK package to peer A
		- peer B sends FIN package to peer A (can be merged with above step)
		- peer A sends ACK package to peer B, then connection is closed
2. TCP vs UDP?
	- TCP supports resend loss packets, while UDP doesn't -> TCP is used in case packet lossing is not acceptable, UDP can be used in real-time voice/call/video streaming
3. HTTP?
	- is application protocol (on L7 layer), uses TCP protocol
	- is stateless connection because each request is executed independently -> high scalability
	- HTTPS = HTTP + TLS for data encryption
4. Socket?
	- is an endpoint for sending/receiving data between processes and machines
5. DNS?
	- convert a hostname to ip address (given to each device on internet)
	- get from: browser's cache -> OS' cach -> DNS resolver (sends request to domain name server)
	- DNS uses UDP protocol (fast, request's data is small)
6. Connection pool?
	- group of database connections, can be reused for new connections (opening/closing a new connection is costly)
	- cons:
		- manage pool's configuration: pool's size and max connections
		- resource allocation: inefficient use -> resource contention
7. TCP proxy/ reversed proxy?
	- proxy server acts as an intermediary between clients and servers. proxy hides clients on internet (server only knows requests come from proxy, not clients), and reversed proxy hides servers (client only knows response come from reversed proxy, not servers)
8. REST vs RPC vs GraphQL?
9. Event-driven architecture (EDA) vs request/response (RR)?

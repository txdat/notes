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
- client can be either mobile applications or web applications
- chat service must support:
	- receive messages from other clients
	- find the target recipients and relay message to them
	- if a recipient is not online, hold message on server until he/she is online
# network protocols
- client (sender) -> chat service
	- client opens a http connection to chat service with keep-alive header to send message, and inform chat service to send to the receiver
	- keep-alive connection allows maintain connection, reduce http handshakes
- chat service -> client (recipient)
	- not able to send message from server to client using http connection
	- server initiated connection:
		- pooling
			- client periodically asks the server for new messages available
			- depend on frequency, pooling could be costly (consume more server's resources to answer 'no')
		- long pooling
			- client holds connection until there are new messages or reach to timeout
			- client sends new messages to server by new connection after receiving messages
			- cons:
				- sender and receiver may not connect to same server (http requests are stateless, the server that receives messages may not hold connection)
				- a server has no good way to tell that client is disconnected
				- make periodic connections after timeout
		- web socket -> most common solution to send asynchronous updates from server to client
			- initiated by client, bi-direction and persistent connection
			- works even if firewall is in place, because it uses port 80 and 443 like http/https connection
			- use for both sending/receiving on both server and client
# service
[[chat service]]
- stateless services
	- traditional public-facing request/response services (behind a load balancer for routing request) for login, signup, ...
- stateful service - chat service
	- maintain a persistent network connection to server -> reason for why chat service is stateful
	- a client normally does not switch to another server as long as server is still available (session affinity in load balancing)
- third-party integration - notification service
	- inform users when new messages have arrived, even if the app is not running
- service discovery: select best chat server for client based on geographical location, server capacity, ... -> zookeeper
- online presence service:
	- manage online status and communicate with client through web socket
	- use heart-beat system (client send event to server every X seconds)

# storage - database
- relational database: for generic data like user profile, settings, user friends list, ...
- no-relational database: for chat history
	- amount of data is very? large
	- only recent data is accessed frequently, but service must support old chat history by search
	-> key-value storage?
		- easy horizontal scaling
		- low-latency to access data
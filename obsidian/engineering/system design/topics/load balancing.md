# algorithms
### round-robin
- LB keeps a list of servers, and sends requests in sequential order
### least response time
- LB monitors the response time of servers, send requests to server with fastest response time
- if 2 servers have same response time, LB sends requests to server with fewer connections
### weighted round-robin
- LB assigns weight to each server, and sends requests to server with higher weight (higher capacity) (round-robin extension)
### adaptive
- LB keeps track of server's metrics (like CPU, memory, etc...), and sends requests to server with lower load -> better fault tolerance, but it's complex
### least connections
- LB keeps track of servers with their connections, and send requests to server with fewer connections
### ip hash
- LB uses hash function to convert user's ip address to a number and sends requests to matched server -> sticky sessions from same user
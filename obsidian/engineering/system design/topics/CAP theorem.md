[swsmile](https://swsmile.info/post/distributed-system-cap-theorem/)

- Consistency: all nodes see same data at the same time
- Availability: all reads/writes always succeed
- P: network partition toleration: the system continues to work despite that some parts of system are unavailable, or data is lost during network transmission -> must be met in distributed system (cannot avoid)
-> distributed system can only meet at most 2 of 3 at same time

# CAP tradeoffs
- CA without P (network partition): not realistic in distributed system
- CP without Availibity = high consistency
	- clients **MUST** wait data among nodes be consistent before accessing them
	- eg: distributed relational DBMS
- AP without Consistency = high availability
	- clients need to be able to get data immediately, data may be stale
	- eg: CDN, S3
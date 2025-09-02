- guide for interviewing: https://interviewing.io/guides/system-design-interview

- 45 FAANG/MAANG problems: https://airtable.com/appk6OJVwxXta1vu4/shrC6BrspHhXTIJ7D/tbl8JOeXpb5Yv509v

# overall structure
![[Pasted image 20250902153508.png | 600]]

### types of SD
- low-level design (OOP) -> real use cases
- infrastructure design -> infrastructure use cases
	- rate limiter, message broker, key-value storage, ...
- product design
	- use correct class structure (following SOLID design) for particular use cases
	- [grokking low-level design](https://drive.google.com/file/d/1qt-8a51ftE-w_9y5oi7GNFZ2ZqvLmpmq/view)

### 1. delivery framework (how to make a workable system - interview progress) => for 40m - 1h
-> structure thoughts and focus on most important aspects

![[Pasted image 20250902153435.png | 800]]

1. requirements (~ 5m)
	1. functional requirements = business requirements
		- are **core functions** of the system -> the first things to discuss with the interviewer
		- questions
			- users/clients should be able to ...?
			- does the system need to do ...?
			- what would happen if ...?
	2. non-functional requirements = system requirements (system qualities)
		- questions
			- the system should be ...?
			- the system should be able to ...?
		- top requirements
			- CAP theorem = consistency or availability when network partition occurs (always happens in distributed system)
			- environment constraints = server or edge devices, network, ...
			- scalability = how to solve bursty traffic / significant increase
			- latency
			- durability = tolerate some data loss (social network) or not (banking system)
			- security
			- fault tolerance = redundancy, failover, recovery mechanisms
2. core entities (~ 5m)
	- are data entities/schemas
	- **don't entire data models at this point** -> quickly iterate and add to it later
3. API / system interfaces (~ 1m)
	- REST (default) => not choose another type unless there are specific requirements
	- RPC for service-to-service
	- socket
	- graphQL
4. data flow (~ 5m)
	- is data processing (optional)
5. high-level design = white board design (~ 5-10m)
	- represents system components (eg. load balancer, servers, databases, caches, ...) and demonstrates how they interact
	- **don't overthink** -> make it simple and focus on functional requirements
	- be explicit about how data flows and changes in the system
	- ![[Pasted image 20250902155636.png | 700]]
6. low-level design (deep dive) (~ 10-20m)
	- think about non-functional requirements -> improve existing system to solve each of interviewer's requiments
### 2. core concepts
- [x] CAP theorem [[engineering/interview/system design/core concepts/cap theorem|cap theorem]] -> choose between consistency (C) or availability (A) when partition (P) happens
- [ ] networking essentials
- [x] API design [[api design]] -> choose REST as default
- [ ] locking
- [ ] DB indexing
- [ ] consistent hashing
- [ ] scaling
- [ ] security
- [ ] monitoring
### 3. key technologies
- [ ] API gateway
- [ ] Redis
- [ ] PostgreSQL
- [ ] MongoDB
- [ ] ElasticSearch
- [ ] LSM/Cassandra
- [ ] Kafka/Zookeeper
- [ ] Spark/Flink
### 4. patterns
- [ ] real-time updates
- [ ] dealing with contention
- [ ] multi-step processes
- [ ] scaling reads
- [ ] scaling writes
- [ ] blob storage
- [ ] long-running task

### 5. common problems

### infrastructure designs
- [ ] distributed cache
- [ ] distributed queue
- [ ] distributed lock
- [ ] api rate limiter
### product designs
- [ ] distributed metrics/logs, aggregation and monitoring service
- [ ] notification service
- [ ] ticket booking system
- [ ] distributed counter (eg. count facebook likes, ...)
- [ ] top-k elements (eg. shared articles, video ranking, ...)
- [ ] cloud storage (eg. dropbox, google drive, ...)
- [ ] payment system (eg. credit card, ...)
- [ ] on-call escalation system
- [ ] live comments on facebook, youtube, ...
- [ ] url shortening
- [ ] live feed on social network
- [ ] ride sharing (eg. uber, lift, ...)
- [ ] live streaming
- [ ] recommendation system (eg. spotify, ...)
- [ ] web crawler
- [ ] chat application
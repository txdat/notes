# service
- data gathering service
	- gathers user input queries and aggregates (counting) them in real time
- query service
	- given a search query or prefix, return top-k most frequently search terms
# trie data structure
- a crucial component to avoid fetching top-k from database
- properties
	- tree-like data structure
	- each node represents a string or a prefix string (root represents empty string)
- steps:
	- find node based on query
	- get all valid childrens (under found node), sort them and get top-k
- optimization:
	- limit length of query
	- cache top search queries at each node -> requires lots of space to store top queries at each node (trade off between space and response time)
# data gathering service
- when user types a query, updating data in real-time is not practically:
	- too many requests per day -> updating trie on every query will slow down system
	- top suggestions may not change much -> unnecessary to update trie frequently (if there isn't real-time requirement)
-> data used to build trie comes from analytics and logging services
- use cache to store trie snapshot
- can update trie daily/weekly/.. (recommended) or update trie's nodes (and their ancestors) directly (slow)
# query service
- api server gets trie data from cache and construct autocomplete suggestion. if data isnt in cache, replenish data (from trie db) back to the cache
- optimization:
	- browser caching (in client)
	- data sampling in data logging
# storage scaling
- apply data sharding based on queries. a not good sharding can cause data imbalance problem
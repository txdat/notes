- given a long url, create a shortened url (as short as possible) and redirect to original url: `https://abc.xyz/...` -> `https://tinyUrl.com/{hashValue}`
	- 2 endpoints
		- `[POST] /shorten` -> shorten url
		- `[GET] /shortUrl` -> redirect shortened url to original url (status code 301)
			- code 301 (permanent redirect): browser sends subsequent requests to original url servers directly instead of shortenUrl service
			- code 302 (temporary redirect): browser keep sending subsequent requests to shortenUrl service first and redirect to original url servers
- store in DB: {unique id, shortened url (hashed from unique id), original url}
# solution
### hash & collision
- use well-known hash functions like CRC32, MD5, SHA-1, ... and get X first characters
- collision can be solved by append predefined string to original url and re-hash -> use bloom filter to improve performance when searching in DB
- pros:
	- fixed shortened url length
	- needn't unique id generator
	- cannot find next available shortened url
- cons:
	- have to solve collision
### base62
- convert number to base-62 representation
- pros:
	- collision is impossible (because id is unique)
- cons:
	- length of shortened url is not fixed (increasing)
	- depends on unique id generator
	- can guest next available shortened url
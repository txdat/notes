[hellointerview](https://www.hellointerview.com/learn/system-design/core-concepts/api-design)

# REST/GraphQL/RPC
1. REST (representation state transfer)
	- uses standard HTTP methods to manipulate resources => default choice for most web apps
2. GraphQL
	- uses single endpoint and allows clients query exactly data what they want by SQL => flexible data fetching, avoid over/under fetching
3. RPC (remote procedure call)
	- use serialization + HTTP2 + well defined schemas => microservices, internal APIs, streaming, or high performance connection

# authentication (verify identity) & authorization (verify permissions)
1. JWT

# rate limiting & throttling => 429 error: too many requests

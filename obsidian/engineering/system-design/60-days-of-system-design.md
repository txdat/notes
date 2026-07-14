# decoupling mobile from backend services
- [x] add an API gateway
	- 1 domain/auth flow/error contract
- [ ] build a BFF (backend for frontend)
	- BFF solves data shape per client type
- [ ] put a load balancer in front of all services
	- a LB distributes traffic across identical instances of services (support service splitting), not support 1 auth flow/rate limiting
- [ ] switch to GraphQL
	- GraphQL solves schema unification, not transport coupling
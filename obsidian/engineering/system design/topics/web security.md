- authentication >>> authorization
# cookie
- in client site
- store user's info: name, address, ...
# session-based authentication
- in server site
- disadvantages
	- increase storage quickly
	- difficult in horizontal scaling
![[Pasted image 20240724234547.png | 800]];
# oauth/jwt
![[Pasted image 20240724234836.png | 800]]
- jwt contains 3 parts (splitted by '.')
	- header: token's info (like encryption algorithm, ...)
	- payload: client-defined info (eg. username, role, ...)
	- signature: (base64 header + base64 payload) & secret key `HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret_key)`
- jwt is stateless (access/refresh? tokens are stored in client)
- signing key by symetric signing method
- token expiration
	- refresh token
		- **RT is stateful (stored in DB in dedicated RT table) , AT is stateless**
		- expiration days/weeks
		- only sent to server when access token is expired -> avoid log in again
		- created with access token simultaneously
		- refresh token is stored in DB (not access token). if access token is expired, client send refresh token to renew access token. server checks refresh token from DB, if RT is existing in DB, server deletes it and creates both RT/AT (RT keeps expiration date) -> server creates new RT/AT pair to avoid (Refresh) Token Theft
		- if RT is expired -> logout
		- if user wants to logout -> server delete RT in DB
	- (short-lived) access token
		- expiration ~15 mins
		- reduce authentication time (not query DB)
		- revoke access token?
	- why not increase AT lifetime to match RT (replace RT)?
		- AT (from JWT) is stateless and self-contained, so server cannot check that AT is revoked or not
	- what happens when user clicks log-out button?
		- client sends RT to server to delete RT without returning new AT
		- user can use AT for a short time (~15m)

# comparison

|**Feature**|**Session-Based Authentication (SB)**|**OAuth with JWT Access Tokens (AT)**|
|---|---|---|
|**Authentication Type**|**Stateful** (Server maintains the "state" of the session)|**Stateless** (Session state is in the token itself)|
|**The Credential**|Session ID (a meaningless random string) in a cookie.|Access Token (AT) which is typically a self-contained **JWT**.|
|**Validation Flow**|For **every request**, the server must **look up the Session ID in the Session Store/DB** to find the user's data.|For **every request**, the server verifies the JWT's **cryptographic signature** using a secret key. **No DB lookup is required** for the AT.|
|**Scalability**|Poor: Requires a central, shared, and highly available session store (DB/Redis) that every server must hit, creating a bottleneck.|Excellent: API servers are independent (stateless). They can validate tokens on their own, making it easy to scale horizontally.|
|**Revocation**|**Instant**: Deleting the session ID from the DB immediately invalidates it.|Delayed: Must wait for the short-lived AT to expire. Revocation is handled by the **Refresh Token (RT)**.|
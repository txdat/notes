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
# jwt
![[Pasted image 20240724234836.png | 800]]
- jwt contains 3 parts (splitted by '.')
	- header: token's info (like encryption algorithm, ...)
	- payload: client-defined info (eg. username, role, ...)
	- signature: (base64 header + base64 payload) & secret key `HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret_key)`
- jwt is stateless (access/refresh? tokens are stored in client)
- signing key by symetric signing method
- token expiration
	- refresh token
		- expiration days/weeks
		- only sent to server when access token is expired
		- created with access token simultaneously
		- refresh token is stored in DB (not access token). if access token is expired, client send refresh token to renew access token. server checks refresh token from DB, if RT is existing in DB, server deletes it and creates both RT/AT (RT keeps expiration date)
		- if RT is expired -> logout
		- if user wants to logout -> server delete RT in DB
	- (short-lived) access token
		- expiration ~15 mins
		- reduce authentication time (not query DB)
		- revoke access token?
			- 
# oauth
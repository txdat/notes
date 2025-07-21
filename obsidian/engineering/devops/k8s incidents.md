# cpu throttling cascade
- is cascading failure pattern, where CPU throttling leads to performance degradation, triggers more scaling, and make problem worse
- k8s uses **cgroups** to enforce CPU limit, when a container exceeds CPU limit (too restrictive):
	- kernel throttles, reduces CPU allocation (only degrades performance) -> container becomes slower
- issues
	- more pods, more cpu contention on nodes
	- each pod gets throttled, system becomes slower despite having mode pods, and more loads on shared resources (like DB, cache, ...)
	- 

# hpa thrashing
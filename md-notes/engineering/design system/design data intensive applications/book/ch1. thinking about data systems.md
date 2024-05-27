# reliability
- system continues working correctly even when things go wrong (having faults) -> fault-tolerant/resilient system (fault is one component of system deviating from its spec, failure is when system whole stop providing services)
- prefer tolerating faults over preventing faults, but some cases preventing is better (hacker attacking cannot be undone)
### hardware faults
- random and independent from each other -> weak correlations
- add redundancy to the individual hardware components -> reduce failure rate of system, sufficient for most applications
### software errors
- harder to anticipate, they are correlated across nodes -> cause many system faults
- solution?
	- process isolation
	- service monitoring
human errors (configuration errors)
# scalability
- is term use to describe a system's ability to cope with increased load -> "what are our options/add computing resources to cope with the growth?"
# maintainability

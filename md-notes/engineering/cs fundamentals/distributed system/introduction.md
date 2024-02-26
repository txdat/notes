# distributed system
### distributed system is ...
- a collection of computing elements (behave independently)
	- no global clock for independent nodes -> synchronization and coordination in distributed system
	- distributed system is organized as an overlay network (built on top of another network, without any effect to it)
- appear as a single coherence system -> distribution transparency
- distributed systems usually have a middleware layer (placed on top of computers' OS) -> hide differences in hardware and operating systems from applications
### design goals
- support resources sharing
- make distribution transparent -> hide its processes and resources are physically distributed across multiple computers
	- types of transparency:
		- access: hide differences in data presentation and how it can be accessed
		- location: hide where data is physically located in system
		- relocation/migration: hide how data is being moved in system
		- replication: hide the fact that several copies of a resource exist -> all replications have same name
		- concurrency: hide that other users are using the same resource
		- failure: hide the failure of any piece of system
	-> trade-off between high degree of transparency and performance of system
- openness: its components are easily used by, or integrated into other systems
	- two or more implementations of systems or components (from different manufaturers) can co-exist and work together
	- components from system A can work on system B (having same interfaces)
- scalable (for system)
	- size: add more users and resources without any noticeable loss of performance
	- geographical: users and resources may lie far apart, but the communication delays are hardly noticed
	- administrative: for more organizations
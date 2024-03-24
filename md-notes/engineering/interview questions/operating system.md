1. process vs thread?
- process:
	- is program execution
	- memory is isolated between processes (must be modified by 1 process at specific time)
	- processes can communicate with others by socket
	- multi-process is more than 1 process running simultaneously on computer
	- child process:
		- created by 1 process
		- inherit most of properties from its parent, create new properties like id, lock, ...
- thread:
	- segment of a process. a process can have one or more threads (with 1 main thread)
	- threads in same process can access same memory allocation
	- cpu costs less resources to switch between threads than processes - needn't to change memory space
	- multi-thread is more than 1 thread running simultaneously by 1 process
	- thread pool:
		- manage concurrent execution
2. concurrency vs parallelism vs multi-threading?
- [concurrency-parallelism](https://jenkov.com/tutorials/java-concurrency/concurrency-vs-parallelism.html)
- concurrency
	- make progress on more than 1 task at the same time. if computer has 1 cpu, cpu switches between the different tasks during execution
- parallel execution
	- cpus (more than 1 cpu) make progress on more than 1 task simultaneously. parallel execution != parallelism
- parallel concurrent execution
	- make progress tasks on cpus simultaneously (parallel), multi tasks on each cpu (concurrency)
- parallelism
	- application splits its tasks into smaller subtasks, which can be processed parallel at the same time -> != parallel (concurrent) execution
	- have more than 1 thread and each thread must run on seperate cpus
	-> concurrency refers to how a single cpu make progress multiple tasks seemingly at the same time
	-> parallelism refers to how an application can be processed parallel by spliting a task into smaller subtasks
3. race condition?
	- multi-threading issue
	- data race
		- more than 1 thread/process that access to shared memory/resources
		- at least 1 thread/process that changes shared resources' values
	-> use 'mutual exclusion' to guarantee that only 1 thread/process modifies shared memory/resource at any time
	- race condition:
		- not control order and number of executions of threads/processes
4. locking mechanism?
	- 
5. virtual memory & paging?
6. 
[nodejs event loop](https://www.builder.io/blog/visual-guide-to-nodejs-event-loop)
			
- javascript: synchronous - blocking - single thread
- libuv library helps handle asynchronous operations
- nodejs fakes multithreading by multitasking, not speads tasks across threads/processes but time
- synchronous callbacks (call stack) > asynchronous callbacks (microtask queue) > `setTimeout` (pushed into task queue)
- reactor pattern
![[Pasted image 20240912002217.png | 700]]
- event loop 
![[Pasted image 20240912221635.png | 800]]
- libuv library uses native OS/ its thread pool to process asynchronous operations (keep main thread non blocking), then put callbacks to event queue
- call stack must be empty before tasks in event queue are processed (loaded into call stack)
- order of tasks in event queue (includes 6 queues)
	- microtask (nextTick, promise)
	- timer queue (setTimeout, setInterval)
	- microtask
	- I/O queue (fs/http/...)
	- microtask
	- check queue (setImmediate)
	- microtask
	- close queue (close event)
	- microtask

[effective promise](https://www.builder.io/blog/promises)
- use `Promise.all`
	- add `.catch()` to promises
	```javascript
	const [user, product] = await Promise.all([
		fetchUser().catch(onReject), // ⬅️
		fetchProduct().catch(onReject) // ⬅️
	]);
```
- use `Promise.allSettled`
	- returns `{status, value, reason}`, status is `fulfilled/rejected`
# V8
- source code -> Ignition bytecode -> Sparkplug (machine code) -> Maglev/TurboFan (deoptimize to Sparkplug/Ignition if assumption fails) -> optimized code
- optimize base on assumption of **static object shape**
	- internal object layout - maps
		```javascript
// Run with: node --allow-natives-syntax hidden-classes-demo.js
const obj1 = {};
const obj2 = {};
console.log(%HaveSameMap(obj1, obj2)); // true

obj1.x = 1;
console.log(%HaveSameMap(obj1, obj2)); // false

obj2.x = 5;
console.log(%HaveSameMap(obj1, obj2)); // true
		```
	- transition trees
		![[Pasted image 20260615152905.png | 600]]

# Event loop
- JS stack -> process.nextTick -> V8 microtasks -> libuv callbacks
### libuv
- use epoll (linux), kqueue (mac), iocp (windows)
- all the core event loop mechanics belong to libuv
- manage global pool of background threads (4/1024 threads)

### event loop phases
```
 ┌─────────────────────────────────┐
 │           timers                │  setTimeout / setInterval
 │  (post-poll in Node 20+)        │  min-heap; delay = minimum threshold
 ├─────────────────────────────────┤
 │       pending callbacks         │  I/O errors deferred from prior iteration
 ├─────────────────────────────────┤
 │        idle / prepare           │  libuv internal bookkeeping only
 ├─────────────────────────────────┤
 │            poll                 ┤  I/O events; epoll/kqueue/IOCP
 │       (heavy hitter)            │  blocks at OS level (not a JS busy-loop)
 │                                 │  if setImmediate pending → skip to check
 ├─────────────────────────────────┤
 │            check                │  setImmediate callbacks
 ├─────────────────────────────────┤
 │       close callbacks           │  socket.destroy() "close" events
 └────────────┬────────────────────┘
              │ any referenced handles/timers left?
              │  yes → next iteration
              │  no  → process exits
```

```javascript
console.log("1. Start");
Promise.resolve().then(() => console.log("4. Promise"));
process.nextTick(() => console.log("3. nextTick"));
fs.readFile(__filename, (error) => {
  console.log("5. I/O Callback");
  setTimeout(() => console.log("9. Timeout from I/O"), 0);
  setImmediate(() => console.log("8. Immediate from I/O"));
  process.nextTick(() => console.log("6. nextTick from I/O"));
  Promise.resolve().then(() => console.log("7. Promise from I/O"));
});
console.log("2. End");


"1. Start"
Synchronous, main call stack
"2. End"
Synchronous, main call stack — fs.readFile is async, doesn't block
"3. nextTick"
Stack cleared → drain nextTick queue first
"4. Promise"
nextTick queue empty → drain V8 microtask queue
"5. I/O Callback"
libuv poll phase fires the fs.readFile completion callback
"6. nextTick from I/O"
I/O callback returns → immediately drain new nextTick entries
"7. Promise from I/O"
nextTick empty → drain V8 microtasks queued inside I/O callback
"8. Immediate from I/O"
Loop advances to check phase — setImmediate fires
"9. Timeout from I/O"
Check phase done → timer phase — zero-delay timer fires last
```

|                              | Runs in...                           | Relative order (from I/O callback)                      |
| ---------------------------- | ------------------------------------ | ------------------------------------------------------- |
| `process.nextTick()`         | Current iteration, before next phase | 1st — drains immediately after current callback returns |
| `queueMicrotask()` / Promise | Current iteration, after nextTick    | 2nd                                                     |
| `setImmediate()`             | Next check phase                     | 3rd                                                     |
| `setTimeout(..., 0)`         | Next timers phase                    | 4th                                                     |

# Buffer

# Stream

# Async pattern
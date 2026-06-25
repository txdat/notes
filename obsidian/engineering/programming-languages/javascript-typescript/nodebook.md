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
Two-layer architecture: **libuv** (native engine — I/O, timers, thread pool) + **Node scheduling rules** (microtask queues). V8 only handles JS execution and GC.

### Components
- **V8**: call stack, heap, GC — no I/O or timers
- **libuv**: epoll (linux) / kqueue (mac) / IOCP (windows); worker thread pool default 4 threads (`UV_THREADPOOL_SIZE`); serves `fs`, `crypto.pbkdf2`, `dns.lookup`, zlib
- **C++ bindings**: bridge between V8 and libuv

Blocking the event loop = any long-running synchronous work on the call stack; no queued callback can interrupt it.

### Event loop phases
```
 ┌─────────────────────────────────┐
 │           timers                │  setTimeout / setInterval
 │                                 │  delay = minimum threshold, not guarantee
 ├─────────────────────────────────┤
 │       pending callbacks         │  I/O errors deferred from prior iteration
 ├─────────────────────────────────┤
 │        idle / prepare           │  libuv internal bookkeeping only
 ├─────────────────────────────────┤
 │            poll                 │  I/O events; epoll/kqueue/IOCP
 │                                 │  calculates wait time from pending timers
 │                                 │  if setImmediate pending → skip to check
 ├─────────────────────────────────┤
 │            check                │  setImmediate callbacks
 ├─────────────────────────────────┤
 │       close callbacks           │  socket.destroy() "close" events
 └────────────┬────────────────────┘
              │ any referenced handles/timers left?
              │  yes → next iteration   no → process exits
```

After **every** callback returns → drain nextTick queue → drain V8 microtask queue → advance to next phase.

### Microtask priority queues
| Queue         | API                                                              | Priority | Notes                               |
| ------------- | ---------------------------------------------------------------- | -------- | ----------------------------------- |
| next tick     | `process.nextTick()`                                             | 1st      | "Legacy"; recursive use starves I/O |
| V8 microtasks | Promise `.then/catch/finally`, `queueMicrotask()`, `async/await` | 2nd      |                                     |
```javascript
  [callback returns]
    1. drain ALL nextTick  (including new ones added during drain)
    2. drain ALL microtasks (including new ones added during drain)
    3. move on

  A concrete proof:

  Promise.resolve().then(() => {
    console.log("microtask 1");
    process.nextTick(() => console.log("nextTick (nested inside microtask)"));
    Promise.resolve().then(() => console.log("microtask 2 (nested)"));
  });

  process.nextTick(() => {
    console.log("nextTick 1");
    process.nextTick(() => console.log("nextTick 2 (nested)"));
  });

  // Output:
  // nextTick 1
  // nextTick 2 (nested)     ← nested nextTick still runs before any microtask
  // microtask 1
  // nextTick (nested inside microtask)  ← nextTick added during microtask drain...
  // microtask 2 (nested)    ← ...runs before the next microtask
```


**Execution order by context**:
- CJS top-level: stack → nextTick → microtasks → event-loop phases
- Phase callback: callback → nextTick → microtasks → next phase
- ESM top-level: module evaluation *is* a microtask — promises can run before `process.nextTick()`

```javascript
console.log("1. Start");
Promise.resolve().then(() => console.log("4. Promise"));
process.nextTick(() => console.log("3. nextTick"));
fs.readFile(__filename, (err) => {
  console.log("5. I/O Callback");
  setTimeout(() => console.log("9. Timeout from I/O"), 0);
  setImmediate(() => console.log("8. Immediate from I/O"));
  process.nextTick(() => console.log("6. nextTick from I/O"));
  Promise.resolve().then(() => console.log("7. Promise from I/O"));
});
console.log("2. End");

// 1. Start          — sync
// 2. End            — sync
// 3. nextTick       — stack cleared → drain nextTick
// 4. Promise        — drain V8 microtasks
// 5. I/O Callback   — poll phase
// 6. nextTick from I/O  — I/O returns → drain nextTick
// 7. Promise from I/O   — drain microtasks
// 8. Immediate from I/O — check phase
// 9. Timeout from I/O   — timers phase (next iteration)
```

### `setTimeout` vs `setImmediate`
- **From main script**: unpredictable — timer threshold may or may not have passed
- **From inside I/O callback**: `setImmediate` always first — poll phase finishes, check phase is next; timer phase comes after

### What blocks the event loop
- `fs.readFileSync()` and other sync APIs
- `JSON.parse()` on large payloads
- Regex with catastrophic backtracking
- Heavy CPU loops without yielding

Worker pool (libuv threads) is shared — a slow `fs` op competes with `crypto.pbkdf2`; default 4 threads is a common bottleneck under concurrency.

### CPU-bound solutions
| Approach | Mechanism | Use case |
|---|---|---|
| `setImmediate()` chunking | yields between batches, same thread | improve responsiveness without true parallelism |
| `worker_threads` | own V8 isolate + event loop per worker | true parallelism; data cloned or transferred |
| `cluster` | multiple Node processes sharing ports | horizontal scale across CPU cores |

### Monitoring event loop lag
```javascript
// basic
let last = Date.now();
setInterval(() => {
  const lag = Date.now() - last - 1000;
  if (lag > 50) console.warn(`EL lag: ${lag}ms`);
  last = Date.now();
}, 1000);

// production
const { monitorEventLoopDelay } = require("node:perf_hooks");
const h = monitorEventLoopDelay({ resolution: 10 });
h.enable();
// h.mean, h.percentile(99), etc.
```

V8 GC stop-the-world pauses are indistinguishable from blocking code and contribute to tail latency spikes under memory pressure.

# Buffer

# Stream

# Async pattern
### error-first callback
### try/catch
- try/catch only protects the stack that is running right now
```javascript
try {
  fs.readFile("/nonexistent", "utf8", (err, data) => {
    console.log(data.trim()); // -> error
  });
} catch (err) {}
```

### promise
- a promise starts as pending, goes fulfilled/rejected (irreversible); tracked via internal `[[PromiseState]]` / `[[PromiseResult]]`
- executor runs **synchronously**; `.then/.catch/.finally` handlers always deferred to microtask queue
- **resolution vs settlement**: resolving with another promise makes the outer promise *follow* that promise's state (not wrap it); thenables go through `PromiseResolveThenableJob` — one extra microtask turn vs a plain value
- **chaining**: each `.then()` returns a **new** promise; handler return value determines next settlement
	- normal return → fulfills next
	- thrown error → rejects next
	- returned promise → next follows that promise
- **error propagation**: rejection travels down the chain until a handler catches it; fulfillment-only handler is skipped; `.catch()` returning a value recovers the chain
- unhandled rejection: Node v24 default `--unhandled-rejections=throw` (treats as uncaught exception); `unhandledRejection` / `rejectionHandled` process events track lifecycle
- `util.promisify()` wraps error-first callbacks; multi-value functions need `util.promisify.custom`; `util.callbackify()` reverses direction
- **starvation**: unbounded microtask recursion starves I/O — use `setImmediate()` between large independent batches
- memory: every `.then()` allocates a promise; handler closures can retain large buffers — profile heap under concurrency

**Combinators** — operate on already-started promises; they don't cancel, retry, or limit concurrency:

| Combinator | Fulfills when | Rejects when | Use case |
|---|---|---|---|
| `Promise.all(arr)` | **all** fulfill | first rejection | need every result; one fail = all fail |
| `Promise.allSettled(arr)` | **all settle** (never rejects) | — | batch ops; collect all outcomes |
| `Promise.race(arr)` | first to settle | first to settle | timeout racing; losers keep running |
| `Promise.any(arr)` | first fulfillment | **all** reject → `AggregateError` | redundant mirrors / fallbacks |

```javascript
// all — ordered results regardless of completion sequence
const [user, posts] = await Promise.all([fetchUser(id), fetchPosts(id)]);

// allSettled — inspect each outcome
const results = await Promise.allSettled([...]);
for (const r of results) {
  if (r.status === "fulfilled") use(r.value);
  else logError(r.reason);
}

// race — timeout pattern (does NOT cancel the loser)
const res = await Promise.race([fetch(url), timeout(5000)]);

// any — first CDN to respond wins
const data = await Promise.any([fetch(cdn1), fetch(cdn2), fetch(cdn3)]);
```

**Concurrency limiting**:
```javascript
async function pMap(items, fn, concurrency) {
  const results = new Array(items.length);
  let nextIndex = 0;
  async function worker() {
    while (nextIndex < items.length) {
      const i = nextIndex++;
      results[i] = await fn(items[i], i);
    }
  }
  await Promise.all(Array.from({ length: Math.min(concurrency, items.length) }, worker));
  return results;
}
```

**Retry with exponential backoff**:
```javascript
async function retry(fn, { maxRetries = 3, baseMs = 1000, shouldRetry = () => true } = {}) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try { return await fn(); }
    catch (err) {
      if (attempt === maxRetries || !shouldRetry(err)) throw err;
      const delay = baseMs * 2 ** attempt * (0.5 + Math.random() * 0.5);
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
// wrap functions, not promises: retry(() => fetch(url))
// only retry transient: 429, 503, timeouts — not 4xx auth/input errors
```

**Timeout with AbortSignal**:
```javascript
async function fetchWithTimeout(url, ms, options = {}) {
  const signal = options.signal
    ? AbortSignal.any([options.signal, AbortSignal.timeout(ms)])
    : AbortSignal.timeout(ms);
  return fetch(url, { ...options, signal });
}
```

### async/await
- syntactic sugar over promise chains; each `await` ≈ a `.then()` continuation
- code **before** the first `await` runs synchronously on the caller's stack
- at an `await`: V8 saves locals + bytecode position to heap (`JSAsyncFunctionObject`), enqueues a `PromiseReactionJob`, returns control; resumes when awaited promise settles
- the **outer promise** (returned to caller) is the single caller-facing result across all suspension points

**Execution ordering** (same rules as microtasks):
```
// CJS: nextTick drains before V8 microtasks
// ESM: top-level runs inside microtask drain — order may differ
```

**`return` vs `return await` in try/catch**:
```javascript
// BAD — rejection escapes try/catch because fn() returns before promise settles
async function bad() {
  try { return fn(); } catch(e) { ... }
}
// GOOD — keeps execution inside try/catch until settled
async function good() {
  try { return await fn(); } catch(e) { ... }
}
```

**Anti-patterns**:
```javascript
// floating promise — rejection is lost
async function bad() { doAsync(); }

// forEach ignores returned promises — loop ends before work completes
urls.forEach(async url => { await fetch(url); });

// accidental serialization — sequential awaits for independent work
for (const u of users) { await sendEmail(u); } // slow!
// fix: await Promise.all(users.map(u => sendEmail(u)))
```

**Memory**: suspended functions retain all in-scope locals — null out large buffers before long waits:
```javascript
async function handle(req) {
  let body = await readBody(req);
  const parsed = parse(body);
  body = null; // release before next await
  return db.save(parsed);
}
```

**Bounded concurrency for large batches**:
```javascript
for (let i = 0; i < items.length; i += 100) {
  await Promise.all(items.slice(i, i + 100).map(transform));
}
```

### event emitter
- **synchronous** listener registry — `emit()` runs listeners on the **current call stack** in registration order; slow listeners block everything that follows
- internal `_events` uses a null-prototype object (no inherited-property collisions); single listener stored as function, multiple as array

**Registration**:
- `on()` / `addListener()` — append to end
- `prependListener()` — insert at front
- `once()` — auto-removes after first fire (but persists if event never fires)
- `off()` / `removeAllListeners()` — explicit cleanup; required for listeners on long-lived objects to avoid leaks

**Special `"error"` event**: if emitted with no listener → throws and crashes process; always attach an `"error"` listener to sockets, streams, servers

**Max-listener warning** (default 10/event): signals repeated `on()` without cleanup, typically from per-request patterns on long-lived emitters

**Modern integration**:
```javascript
import { once, on } from "node:events";

// one-shot — returns a promise
const [data] = await once(ee, "data");

// async iteration — buffers events, consumer-paced
for await (const [msg] of on(ee, "message")) {
  console.log(msg);
}
// both support AbortSignal for timeout/cancellation
```

**When to use each pattern**:

| Pattern | Use case |
|---|---|
| Callback | single result, legacy API |
| Promise / async-await | single async result |
| `events.once()` | wait for one event as a promise |
| EventEmitter `.on()` | repeated push-based notifications |
| Async iterator / `events.on()` | consumer-paced stream of events |

### async iterators
- protocol: object exposes `[Symbol.asyncIterator]()` returning `{ next() → Promise<{value, done}> }`
- `for await...of`: calls `next()`, awaits, loops until `done: true`; on break/throw calls iterator's `return()` for cleanup (closes file handles, destroys streams)
- **inherently sequential** — 100 items × 500 ms = 50 s minimum

**Async generators** (`async function*`):
```javascript
async function* fetchPages(url) {
  for (let page = 1; ; page++) {
    const data = await fetch(`${url}?page=${page}`).then(r => r.json());
    if (!data.items.length) return;
    yield data.items; // pauses until consumer calls next()
  }
}
// await = wait for external I/O; yield = wait for consumer
```

**Readable streams** implement `Symbol.asyncIterator`; `for await...of` naturally respects backpressure — next chunk requested only after current one is processed. Early exit calls `destroy()` by default; use `readable.iterator({ destroyOnReturn: false })` to preserve the stream.

**`events.on()` adapter**: buffers emitted events in an (effectively unbounded) queue for async consumption — beware memory growth if emitter outpaces consumer:
```javascript
for await (const [msg] of on(ee, "message", { signal })) { ... }
// use streams or custom queues with limits for high-throughput sources
```

**Pipeline with backpressure**:
```javascript
async function* map(source, fn) { for await (const x of source) yield fn(x); }
async function* filter(source, pred) { for await (const x of source) if (pred(x)) yield x; }
for await (const item of filter(map(source, transform), predicate)) { ... }
```

**Adding concurrency** inside `for await`:
```javascript
const batch = [];
for await (const item of source) {
  batch.push(process(item));
  if (batch.length >= BATCH_SIZE) { await Promise.all(batch); batch.length = 0; }
}
await Promise.all(batch);
```
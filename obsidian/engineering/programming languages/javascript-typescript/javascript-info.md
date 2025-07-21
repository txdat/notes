# objects
- is keyed collections of various data (not primitive - single value)
- object references and copying
	- store and copied by reference (not like primitive data types)
	- a variable is assigned to object stores reference (address in memory) instead of object itself
	- const object's attributes can be modified
```javascript
const a = {name: 'Peter'};
const b = a; // copy a's properties by references

const c = {};
for (const [k, v] in Object.entries(a)) c[k] = v; // clone, it's copy references if any attribute of a is object -> deep clone
```
- garbage collection
	- counted by incomming references make an object is reachable
- `this` keyword
	- is not bounded -> can be used in any function, even if it's not class' function
	- `this` is evaluated during runtime, depends on the context
	- arrow functions don't have `this`, it takes from outer context
- classes
	- can return from constructor, and methods can be defined in constructor
```javascript
function User(name) {
	// this = {};
	this.name = name;
	this.isAdmin = false;
	// return this;
};

const user = new User('Dat'); // create new object
```

- optional chaining '?'
	- for non existing properties, support shorten chaining
```javascript
const user = null;
console.log(user?.name); // undefined
console.log(user?.sayHi?.()); // undefined, calling method `sayHi`
console.log(user?.['age']); // undefined
```

- symbol
	- primitive types for object's property keys
	- create hidden properties -> no other parts of code can access and overwrite
	- symbols are skipped in for loop
```javascript
const user = {
	name: 'John',
};

const id = Symbol('id');
user[id] = 1; // not accessed accidently

const user2 = {
	[id]: 1, // not 'id': 1
};
```

- bracket `[]` as key of object
```javascript
const k = 'hello';
const map = {
	[k]: 'world',
};

console.log(map['hello']); // "world!"
```
# prototypes, inheritance
- prototypal inheritance
- update/delete operations work with the object directly (not its prototypes)
- `this` is not affected by prototypes at all
- for loop iterates over inherited properties
- `F.prototype` is used to create `[[prototype]]` for new object by calling `new F()`
- `Obj.__proto__` is out-of-date, use `Object.getPrototypeOf(obj)` and `Object.setPrototypeOf(obj, proto)` to get/set `[[prototype]]` of `obj`
- built-in prototypes
```javascript
String.prototype.repeat = function(n) {
	return new Array(n).fill(this).join('');
};
console.log("BOOM".repeat(3)); // BOOMBOOMBOOM
```
# classes
# promise, async/await
### callback
- function passed as an argument into other function, and invoked inside outer function
### promise
- a proxy for a value not necessarily known when the promise is created [doc](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), link producing code and consuming code together
- `resolve(value)` and `reject(error)` are callback functions that are provided by JS itself for `new Promise` calling
	- `state=pending` initially, change to `fulfilled` when `resolve` is called and `rejected` when `reject` is called
	- `result=undefined` initially, change to `value` and `error`
- consuming functions can be registered through `.then` and `.catch`
```javascript
promise.then(
	function (result) {},
	function (error) {} // equal to promise.catch(function (error) {});
);
```
- use `finally` to clean up promise
	- without any argument (don't know the state of promise after executing)
	- pass through result/error to next handlers
	- shouldn't return anything
```javascript
promise.finally(() => { console.log('hello, world!'); }).then(...);
```
- handler can return a new promise
- promise chaining
```javascript
promise.then(...).then(...).then(...); // chaining - handlers process sequentially

// handlers process independently
promise.then(...);
promise.then(...);
```
### async/await
- special syntax to work with promises
- `async function()` returns a promise, wraps non-promises in it
- `await promise` makes JS wait until that promise settles and returns its result (suspends the function execution to wait and resume)

# generators, advanced iterations
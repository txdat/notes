# intent
- ensure only 1 instance of class is created with global point to access

# use cases
- logger
- configuration
- accessing resources in shared mode

# implementation
```typescript
class Singleton {
	private static instance = new Singleton();
	
	private constructor() {}
	
	static getInstance(): Singleton { return this.instance; }
	
	doSomething() {
		// do something here
	}
}
```
#todo thread-safe implementation in typescript
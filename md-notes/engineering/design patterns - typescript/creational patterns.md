# singleton
- [guru](https://refactoring.guru/design-patterns/singleton)
- ensure a class has only one instance with global access point to it -> control access on some shared resources, and protect it from being overwritten by other code
- requires special treatment in multithreading environment (won't create a singleton object in several times) = thread-safe singleton -> use lock mechanism
- can use *Enum Singleton* (thread-safe in java, typescript, ...)
- ![[Pasted image 20250428103504.png | 500]]
```typescript
class Singleton {
	private instance: Singleton;

	// cannot access from public
	private constructor() {
	}

	public static getInstance() : Singleton {
		if (!Singleton.instance) {
			Singleton.instance = new Singleton();
		}
		return Singleton.instance;
	}

	...
}

// THREAD-SAFE

// instance is created at class loading time (use static field)
class EagerSingleton {
	private static readonly instance: Singleton = new Singleton();

	private constructor() {
	}

	public static getInstance() : Singleton {
		return Singleton.instance;
	}
}


```
# factory method (virtual constructor)
- provide an interface for creating objects in a superclass, but allow subclasses to alter type of object -> object type is determined at runtime/some specific conditions
- single responsibility (creation/business logic)
![[Pasted image 20250428114521.png | 700]]
```typescript

abstract class Logger { // Product (abstract class or interface)
    abstract log(message: string) : void;
}

class ConsoleLogger extends Logger { // Concrete product
    log(message: string) : void {
        console.log(`[console] ${message}`);
    }
}

class FileLogger extends Logger { // Concrete product
    log(message: string) : void {
        console.log(`[file] ${message}`);
    }
}

abstract class LoggerFactory { // Creator (includes factory method), (abstract class or interface)
    protected abstract createLogger(): Logger

    log(message: string) : void {
        this.createLogger().log(message);
    }
}

class ConsoleLoggerFactory extends LoggerFactory { // Concrete creator
    createLogger(): Logger {
        return new ConsoleLogger();
    }
}

class FileLoggerFactory extends LoggerFactory { // Concrete creator
    createLogger(): Logger {
        return new FileLogger();
    }
}

const consoleLogger = new ConsoleLoggerFactory();
consoleLogger.log('hello, world!');

const fileLogger = new FileLoggerFactory();
fileLogger.log('xin chào, Việt Nam');

```
# abstract factory
# builder
# prototype
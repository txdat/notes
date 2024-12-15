[link](https://joyofcode.xyz/typescript-fundamentals)
- typescript is static type-checker at compile time
- TS is superset of JS and compiles to JS
- add `// @ts-check` at the top of JS file for type checking
- primitive types >< primitive wrapper objects
- typescript types
	- any (avoid using)
		- represent all possible values -> no type checking
	- unknown (avoid using)
		- type-safe version of `any`
		- cannot access object's properties unless type narrowing first and then type assertion
		```typescript
		const response = apiResponse as {data: []}; // narrowing
		console.log(response.data);
```
	- void
		- absence of having any type
		- only `undefined` to be assignable to type `void`
		- use for returned value of function isn't going to be used
	- never
		- represent values that never occur (no reachable endpoint) -> cant have a value
		```typescript
		function infiniteLoop(): never {
			while (true) {...}
		}
```
- function overloading
	- same name with different implementations
	- TS supports overload signatures
	```typescript
	function logPokemon(name: string, hp: number) : void; // sig1
	function logPokemon(pokemon: Pokemon) : void; // sig2

	function logPokemon(arg1: unknown, arg2?: unknown) : void {
		// sig1
		if (typeof arg1 === 'string' && typeof arg2 === 'number') {
			console.log(`${arg1} has ${arg2} hp.`);
			return;
		}

		// sig2
		if (typeof arg1 === 'Pokemon') {
			const { name, hp } = arg1 as Pokemon; // narrowing
			console.log(`${name} has ${hp} hp.`);
			return;
		}
	};
```
- type alias
```typescript
type Pokemon = {name: string, hp: number}; // 'Pokemon' as alias for object

const pokemons: Pokemon[] = [];

// for function
type LogPokemon = (name: string, hp: number) => void;

const log1: LogPokemon = (name) => { console.log(name); };

// can extend an alias by using intersection
type ElectricPokemon = Pokemon & {pokemonType: 'electric'}; // fixed pokemonType to 'electric' -> change to string?
```
- interface
	- name an object type
	```typescript
	interface Pokemon {
		id?: string,
		name: string,
		pokemonType: string,
		ability: string,

		attack(): void; // method
	};

	// extend interface
	interface ElectricPokemon extends Pokemon {
		pokemonType: 'electric'
	};
```
- union types
```typescript
function hello(name: string[] | string) { // accept both string[] and string
	console.log(`hello ${name}`);
};
```
- enum
	- a set of named constants (not exists in JS)
	```typescript
	// js
	const direction = {
		UP: 'UP',
		DOWN: 'DOWN',
		LEFT: 'LEFT',
		RIGHT: 'RIGHT',
	};
	// ts
	enum Direction {
		UP = 'UP',
		DOWN = 'DOWN',
		LEFT = 'LEFT',
		RIGHT = 'RIGHT',
	};
```
- class
	- support 4 access modifiers
		- public: default
		- protected: can be accessed from subclasses
		- private: only be accessed from current class (not subclasses)
		- readonly: only be assigned in constructor, but can be read from outside of class
	- difference between class and interface in TS
		- purpose
			- class: create object with properties and methods (blueprint of object)
			- interface: define struct of object (how object works)
		- implementation
			- class: contains both properties and methods
			- interface: contains neither properties nor methods, only describe structure
		- inheritance
			- class: support inhertance from other class (only 1)
			- interface: only extend without any implementation, can be extended from multiple interfaces
		- usage
			- class: for creating object with data and behavior
			- interface: want to define structure of object
```typescript
class Pokemon {
    readonly name: string
    private hp: number
    public status: string

    constructor(name: string, hp?: number, status?: string) {
        this.name = name;
        this.hp = hp || 100;
        this.status = status || 'alive';
    }

    hello(): void {
        console.log(`${this.name} has ${this.hp} hp`);
    }
};

interface DogAbilities {
    bark(name: string): void;
};

class ElectricPokemon extends Pokemon implements DogAbilities {
    ability?: string

    constructor(name: string, hp?: number, status?: string, ability?: string) {
        super(name, hp, status);
        this.ability = ability;
    }

    hello(): void {
        super.hello();
        console.log(this.ability ? `i will use ${this.ability}` : `i don't have any shit`);
    }

    bark(name: string): void {
        console.log(`hello ${name} dog`);
    }
};

const pokemon = new ElectricPokemon('hehe', undefined, undefined, 'yaya');
pokemon.hello();
pokemon.bark('hihi');
```
- decorator
	- high-order function, takes function as argument -> metaprogramming #TODO
```typescript
```
- generic
	- variables for types -> create reusable of code for variety of types instead of one
	- function generic
		```typescript
		function map<Input,Output> (arr: Input[], callback: (arr: Input) => Output) {
		    return arr.map(callback);
		}
		
		const names = ['hehe', 'hihi', 'haha'];
		const callback = (name: string) => name.toUpperCase();

		console.log(map(names, callback));
```
	- interface generic
	```typescript
	interface Dictionary<Type> {
	    [key: string]: Type,
	};
	
	interface Pokemon {
	    id: number,
	    name: string,
	};
	
	const dict: Dictionary<Pokemon> = {
	    '1': { id: 1, name: 'haha' },
	    '2': { id: 2, name: 'hehe' },
	};
	
	console.log(dict);
```
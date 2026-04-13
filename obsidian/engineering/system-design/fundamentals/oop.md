1. OOP and its 4 principles?
	- is object-oriented programming -> focus on objects and builds things upon them
	- 4 principles
		- encapsulation
			- wraps things into a unity, wraps methods and fields into a class, classes into a package
		- abstraction
			- only care about public fields, attributes, methods, and needn't care about its private stuff and how they are implemented
		- inheritance
			- allow a class to inherit the properties and characteristics from other classes
		- polymorphism
			- uses same types and functions, but their actions depend on its entity (eg. like circle, rectangle, ...)
2. access modifiers?
	- private: can be accessed by things in same class (object?)
	- default: can be accessed in the same package
	- protected: can be accessed in the same package + outside things that have inheritance relationship
	- public: can be accessed by everything
3. interface and abstract class?
	- the difference is the relationship between it and the classes that extend or implement it
	- class A extends abstract class B -> A is B
	- class A implements interface C -> A has C's characteristics
4. SOLID
	- Single responsibility principle
		- a class should be focused on a single functionality -> easier testing, lower coupling
	- Open/closed principle
		- software entities should be open for extension, but closed for modification -> reduce risk of introducing bugs into existing code
	- Liskov substitution principle
		- objects of a super class should be replaceable with objects of its subclass -> ensure that inheritance hierarchies are logically sound
	- Interface segregation principle
		- no client should be forced to depend on methods that it doesn't use -> prevent polluting classes with unused methods
	- Dependency inversion principle
		- depends upon abstractions, not concretions -> make system pluggable
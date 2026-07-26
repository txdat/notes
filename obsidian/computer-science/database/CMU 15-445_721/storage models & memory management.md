# storage

- DBMS always target maximizing sequential access (on non-volatile memory)
- design goal of DBMS is managing DB that exceeds the amount of memory available
- not use `mmap` in DBMS due to correctness/performance
### pages
- fixed-size block of data (1-16KB)
- page layout
	- slotted pages: maps slots to offsets
		![[Pasted image 20260727003530.png | 200]]

# memory
- move data back and forth between disk and memory with Buffer Pool Manager
### buffer pool
- is in-memory cache (write-back) of pages
- is array of fixed-size frames
- page directory maps page IDs to page locations in DB files. all changes must be recorded on disk
- page table maps page IDs to a copy of pages in buffer pool frames

### locks/latches
- lock is a higher-level, logical primitive that protects **the contents of a DB** from other transactions
- latch is a low-level protection primitive that DBMS uses for **critical sections in internal data structures**

### buffer replacement policies
- LRU
- CLOCK
	- similar to LRU without a separate timestamp per page (use reference bit - 1 is page is accessed)
	- LRU/CLOCK are susceptible to sequential flooding
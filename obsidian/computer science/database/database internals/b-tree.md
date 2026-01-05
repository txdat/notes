- balanced search tree with high fanout (improve locality of neighboring keys) and low height (reduce number of seeks during traversal)
- keys in b-tree node are stored in order

# structure
- page header
- magic number
- sibling links (neighbors)
![[Pasted image 20260101172120.png | 600]]
- rightmost pointer (k keys -> k+1 children)
- overflow pages
	- b-tree node keeps a specific number of items -> variable-size node = multiple linked pages (overflow pages)
	- ![[Pasted image 20260101172554.png | 300]]
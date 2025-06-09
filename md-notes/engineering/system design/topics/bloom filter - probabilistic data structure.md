[systemdesign.one](https://systemdesign.one/bloom-filters-explained/)

- space-efficient probabilistic data structure to check membership, return "true" if item is member of set, may be **false positive**

[[bloom filter]]

### minimize false positive of bloom filter (when checking item is in set or not)
- formula to calculate false positive $$p \approx (1-e^{-kn/m})^k$$, with n is number of inserted items, k is number of hash functions, and m is size of bits array
- to minimize p
	- increase m (reduce probability of hash collision)
	- increase number of hash functions, or use higher quality hash functions
- trade-off
	- memory/false positive rate: increase m (more memory usage)
	- performance/accuracy: increase k, more hash functions require more time
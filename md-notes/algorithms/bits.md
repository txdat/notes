1. [xor tricks](https://florian.github.io//xor-trick/)
2. [number of excellent pairs](https://leetcode.com/problems/number-of-excellent-pairs/description/)
- call `N(a)` is number of set bits of `a`, so `N(a or b) = N(a) + N(b) - N(a and b)` 
3. [apply operations on array to maximize sum of squares](https://leetcode.com/problems/apply-operations-on-array-to-maximize-sum-of-squares/description/)
```cpp
using ll = long long;

constexpr int MOD = 1e9 + 7;

// for any a, b, c = a|b, d = a&b, number of bits unchanged

class Solution {
public:
    int maxSum(vector<int>& nums, int k) {
        int cnt[32] = {0};
        for (int &d : nums) {
            bitset<32> b(d);
            for (int i = 0; i < 32; i++) cnt[i] += b[i];
        }
        ll ans = 0;
        while (k--) {
            ll d = 0;
            for (int i = 0; i < 32; i++) {
                if (cnt[i]) {
                    d |= 1ll<<i;
                    cnt[i]--;
                }
            }
            ans += d * d;
            ans %= MOD;
        }
        return ans;
    }
};
```
4. [bitwise AND of numbers range](https://leetcode.com/problems/bitwise-and-of-numbers-range/description/)
```cpp
// bitwise and of range is common prefix of their bits
class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        int i = 0;
        while (left < right) {
            left >>= 1;
            right >>= 1;
            i++;
        }
        return right << i;
    }
};
```
- [minimum array end](https://leetcode.com/problems/minimum-array-end/description/)
```cpp
using ll = long long;

class Solution {
public:
//	long long minEnd(int n, int x) { // O(n)
//        ll ans = x;
//        while (--n) {
//            ans = (ans+1)|x;
//        }
//        return ans;
//	}


	// we can ignore x's set bits -> fill remaining bits with set bits of n-1
    long long minEnd(int n, int x) {
        n--; // 1st element is x
        ll ans = x;
        for (ll i = 1; n > 0; i <<= 1) {
            if ((i&x) == 0) {
                // fill to i-th bit
                if (n&1) ans |= i;
                n >>= 1;
            }
        }
        return ans;
    }
};
```
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
- [find the maximum sum of node values](https://leetcode.com/problems/find-the-maximum-sum-of-node-values/)
```cpp
using ll = long long;

class Solution {
public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
        ll ans = 0;
        int m = INT_MAX, c = 0; // min diff and number of changable nodes
        // needn't care about edges
        for (int &d : nums) {
            int t = d^k;
            ans += max(t,d);
            m = min(m, abs(t-d));
            if (t>d) c++;
        }
        return ans - (c&1)*m;
    }
};
```
- [single number ii](https://leetcode.com/problems/single-number-ii/description/)
```cpp
class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int c[32] = {0};
        for (int &d : nums) {
            if (d == INT_MIN) {
                for (int i = 0; i < 32; i++) c[i]++;
                continue;
            }
            if (d < 0) {
                d = -d;
                c[31]++;
            }
            int i = 0;
            while (d) {
                c[i++] += d&1;
                d >>= 1;
            }
        }
        int s = 0;
        for (int i = 0; i < 32; i++) s += c[i]%=3;
        if (s == 32) return INT_MIN;
        int ans = 0;
        for (int i = 30; i >= 0; i--) {
            ans <<= 1;
            ans += c[i];
        }
        return c[31] ? -ans : ans;
    }
};
```
- [single number iii](https://leetcode.com/problems/single-number-iii/description/)
```cpp
class Solution {
public:
    vector<int> singleNumber(vector<int>& nums) {
        long x = 0;
        for (int &d : nums) x ^= d;
        // x ^= x&(x-1);
        x = 1<<__builtin_ctzl(x); // select one of bits
        int a = 0, b = 0;
        for (int &d : nums) {
            if (x&d) {
                a ^= d;
            } else {
                b ^= d;
            }
        }
        return {a,b};
    }
};
```
- [find xor-beauty of array](https://leetcode.com/problems/find-xor-beauty-of-array/description/)
	- [explaination](https://leetcode.com/problems/find-xor-beauty-of-array/solutions/3015014/why-just-xor-of-all-numbers-works/)
```cpp
class Solution {
public:
    int xorBeauty(vector<int>& nums) {
        int ans = 0;
        for (int &d : nums) ans ^= d;
        return ans;
    }
};
```
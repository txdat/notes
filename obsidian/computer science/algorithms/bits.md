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
- [patching array](https://leetcode.com/problems/patching-array/)
```cpp
using ll = long long;

class Solution {
public:
    int minPatches(vector<int>& nums, int n) {
        int ans = 0;
        ll m = 1; // can cover [1,m)
        for (int &d : nums) {
            if (d > n || m > n) break;
            while (m < d) {
                ans++; // patch m (2^x) to array
                m <<= 1ll;
            }
            m += d;
        }
        while (m <= n) {
            ans++;
            m <<= 1ll;
        }
        return ans;
    }
};
```
- [minimum number of K consecutive bit flips](https://leetcode.com/problems/minimum-number-of-k-consecutive-bit-flips/description/)
```cpp
class Solution {
public:
    int minKBitFlips(vector<int>& nums, int k) {
        int n = nums.size();
        vector<int> q;
        int ans = 0, f = 0, j = 0;
        for (int i = 0; i <= n-k; i++) {
            if (j < q.size() && q[j] == i) {
                f--;
                j++;
            }
            if (f&1) nums[i] ^= 1;
            if (nums[i]) continue;
            ans++;
            f++;
            q.push_back(i+k);
        }
        for (int i = n-k+1; i < n; i++) {
            if (j < q.size() && q[j] == i) {
                f--;
                j++;
            }
            if (f&1) nums[i] ^= 1;
            if (nums[i] == 0) return -1;
        }
        return ans;
    }
};
```
- [flip columns for maximum number of equal rows](https://leetcode.com/problems/flip-columns-for-maximum-number-of-equal-rows/description/)
```cpp
// key: flip some columns equals to XOR all row values with same number K -> X = X^K^K = K or 1^K -> K = X or 1^X
class Solution {
public:
    int maxEqualRowsAfterFlips(vector<vector<int>>& matrix) {
        unordered_map<string,int> m;
        unordered_map<string,string> rev;
        for (auto &r : matrix) {
            string s = "", t = "";
            for (int &d : r) {
                s.push_back('0'+d);
                t.push_back('0'+(1-d));
            }
            m[s]++;
            rev[s] = t;
        }
        int ans = 0;
        for (auto &[s, c] : m) {
            auto &t = rev[s];
            ans = max(ans, c + (m.find(t) == m.end() ? 0 : m[t]));
        }
        return ans;
    }
};
```
- [maximum product of 2 integers without common bits](https://leetcode.com/problems/maximum-product-of-two-integers-with-no-common-bits/description/)
	- idea: `dp[i]` is maximum value of nums such that `d&i=d` (i is superset of d)
```cpp
using ll = long long;

class Solution {
public:
    long long maxProduct(vector<int>& nums) {
        int m = *max_element(nums.begin(),nums.end());
        int mb = 31 - __builtin_clz(m), max_mask = (1<<(mb+1))-1;
        vector<int> dp(max_mask+1,0);
        for (int &d : nums) dp[d] = d;
        for (int b = 0; b <= mb; b++) {
            int t = 1<<b;
            for (int mask = 0; mask < max_mask; mask++) {
                if (mask&t) {
                    dp[mask] = max(dp[mask], dp[mask^t]);
                }
            }
        }
        ll ans = 0;
        for (int &d : nums) {
            ans = max(ans, ll(d)*dp[max_mask^d]);
        }
        return ans;
    }
};
```
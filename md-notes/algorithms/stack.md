1. monotonic stack
- [sum of subarrays' minimum](https://leetcode.com/problems/sum-of-subarray-minimums/description)
```cpp
using ll = long long;
constexpr int MOD = 1e9 + 7;

class Solution {
public:
    int sumSubarrayMins(vector<int>& arr) {
        int n = arr.size();
        ll ans = 0;
        stack<int> q; // increasing monotonic stack
        for (int i = 0; i < n; i++) {
            while (!q.empty() && arr[q.top()] >= arr[i]) {
                int j = q.top(); q.pop();
                // arr[j] is minimum of any subarray in [q.top()...i)
                ans += ll(arr[j]) * (i - j) * (j - (q.empty() ? -1 : q.top()));
            }
            q.push(i);
        }
        while (!q.empty()) {
            int j = q.top(); q.pop();
            // arr[j] is minimum of any subarray in [q.top()...n)
            ans += ll(arr[j]) * (n - j) * (j - (q.empty() ? -1 : q.top()));
        }
        return ans % MOD;
    }
};
```
- [count submatrices with all ones](https://leetcode.com/problems/count-submatrices-with-all-ones)
```cpp
// solve 1
class Solution {
public:
    int numSubmat(vector<vector<int>>& mat) {
        int m = mat.size(), n = mat[0].size();
        int ans = 0;
        bool r[150];
        for (int i1 = 0; i1 < m; i1++) {
            memset(r, true, sizeof(r));
            for (int i2 = i1; i2 < m; i2++) {
                for (int j = 0; j < n; j++) r[j] &= mat[i2][j];
                int l = 0;
                // count number of subarrays with all ones in 1d array
                for (int j = 0; j < n; j++) {
                    l = r[j] ? l + 1 : 0;
                    ans += l;
                }
            }
        }
        return ans;
    }
};
```
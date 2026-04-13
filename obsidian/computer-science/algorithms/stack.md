1. monotonic stack
**find maximum element -> decreasing monotonic stack. find minimum element -> increasing monotonic stack**
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
- [longest valid parentheses](https://leetcode.com/problems/longest-valid-parentheses/)
```cpp
class Solution {
public:
    int longestValidParentheses(string s) {
        int n = s.length();
        int ans = 0;
        // from left to right
        for (int i = 0, j = -1, c = 0; i < n; i++) {
            c += s[i] == '(' ? 1 : -1;
            if (c < 0) {
                c = 0;
                j = i;
            } else if (c == 0 && i-j > ans) {
                ans = i-j;
            }
        }
        // from right to left
        for (int i = n-1, j = n, c = 0; i >= 0; i--) {
            c += s[i] == ')' ? 1 : -1;
            if (c < 0) {
                c = 0;
                j = i;
            } else if (c == 0 && j-i > ans) {
                ans = j-i;
            }
        }
        return ans;
    }
};
```
- [largest rectangle in histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)
```cpp
// using strictly increasing monotonic stack
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        int ans = 0;
        stack<int> q;
        for (int i = 0; i < n; i++) {
            while (!q.empty() && heights[q.top()] >= heights[i]) {
                int j = q.top(); q.pop();
                ans = max(ans, heights[j]*(i - (q.empty() ? -1 : q.top()) - 1)); // heights[j] is minimum height in [heights[q.top()+1]...heights[i-1]]
            }
            q.push(i);
        }
        while (!q.empty()) {
            int j = q.top(); q.pop();
            ans = max(ans, heights[j]*(n - (q.empty() ? -1 : q.top()) - 1)); // heights[j] is minimum height in [heights[q.top()+1]...heights[n-1]]
        }
        return ans;
    }
};
```
- [find number of subarrays where boundary elements are maximum](https://leetcode.com/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/)
```cpp
using ll = long long;

class Solution {
public:
    long long numberOfSubarrays(vector<int>& nums) {
        int n = nums.size();
        unordered_map<int,vector<int>> m;
        for (int i = 0; i < n; i++) {
            m[nums[i]].push_back(i);
        }
        ll ans = 0;
        stack<int> q;
        for (int i = 0; i < n; i++) {
            while (!q.empty() && nums[q.top()] <= nums[i]) {
                int j = q.top(); q.pop();
                int l = q.empty() ? 0 : q.top() + 1; // nums[j] is maximum element in range [l,i)
                auto &r = m[nums[j]];
                // find all indices between [l,i)
                auto il = lower_bound(r.begin(),r.end(),l), ir = lower_bound(r.begin(),r.end(),i);
                ans += ir - il;
            }
            q.push(i);
        }
        while (!q.empty()) {
            int j = q.top(); q.pop();
            int l = q.empty() ? 0 : q.top() + 1; // nums[j] is maximum element in range [l,n)
            auto &r = m[nums[j]];
            // find all indices between [l,i)
            auto il = lower_bound(r.begin(),r.end(),l);
            ans += r.end() - il;
        }
        return ans;
    }
};
```
- [using a robot to print the lexicographically smallest string](https://leetcode.com/problems/using-a-robot-to-print-the-lexicographically-smallest-string)
```cpp
class Solution {
public:
    string robotWithString(string s) {
      int n = s.length();
      vector<int> q(n); // q[i] is greater or equal than i such that s[q[i]] <= s[i]
      q[n-1] = n-1;
      for (int i = n-2; i >= 0; i--) q[i] = s[i] <= s[q[i+1]] ? i : q[i+1];

      string ans, t;
      for (int i = 0; i < n; i = q[i]+1) {
        int j = q[i]+1;
        t += s.substr(i, j-i); // copy s[i..q[i]]
        if (j < n) {
          char c = s[q[j]];
          while (!t.empty() && t.back() <= c) { // pop t if top/back of t is smaller or equal to next smaller c (s[q[i]+1])
            ans.push_back(t.back());
            t.pop_back();
          }
        }
      }
      while (!t.empty()) {
        ans.push_back(t.back());
        t.pop_back();
      }
      return ans;
    }
};
```
1. [minimum moves to pick k ones](https://leetcode.com/problems/minimum-moves-to-pick-k-ones/description/)
```cpp
using ll = long long;
constexpr int MOD = 1e9+7;

class Solution {
public:
    int sumOfPower(vector<int>& nums, int k) {
        int n = nums.size();
        vector<vector<int>> dp(n+1,vector<int>(k+1,0));
        dp[0][0] = 1; // dp[i][j]: number of subsequences length i, and sum equals to j -> bottom-up solution
        for (int &d : nums) {
            for (int v = k; v >= d; v--) {
                for (int i = n; i > 0; i--) {
                    dp[i][v] += dp[i-1][v-d]; // select d when length is i
                    dp[i][v] %= MOD;
                }
            }
        }
        ll ans = 0, pow = 1;
        for (int i = n; i > 0; i--) {
	        // when picking i elements, number of subsequences containing i elements (select from m=n-i left elements) is (mC0+mC1+...+mCm) = (1+1)^m = 3^m
            ans += pow*dp[i][k];
            ans %= MOD;
            pow *= 2;
            pow %= MOD;
        }
        return ans;
    }
};
```
2. [number of subsequences that satisfy the given sum condition](https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/description/)
```cpp
using ll = long long;
constexpr int MOD = 1e9+7;

class Solution {
public:
    int numSubseq(vector<int>& nums, int target) {
        sort(nums.begin(), nums.end());
        int n = nums.size();

        vector<int> p(n+1); // p[i]=2^i
        p[0] = 1;
        for (int i = 1; i <= n; i++) p[i] = (p[i-1]*2)%MOD;

        int target2 = target/2;
        ll ans = nums[0] <= target2; // length-1 subsequence
        for (int i = 1; i < n; i++) {
            ans += nums[i] <= target2; // length-1 subsequence
            int j = upper_bound(nums.begin(),nums.begin()+i,target-nums[i]) - nums.begin() - 1; // min element in [0..j], j<i -> subsequences are chosen from nums[j..i]
            if (j < 0) continue;
            ans += p[i] - p[i-j-1] + MOD; // sum of 2^(i-j-1)+...+2^(i-1), 2^(i-j-1) is number of subsequences are chosen from nums[j..i] with fixed j and i
            // 2^(i-j-1) + ... + 2^(i-1) = A
            // 2^(i-j) + ... + 2^i = 2A
            // -> A = 2^i - 2^(i-j-1)
            ans %= MOD;
        }
        return ans;
    }
};
```
3. [maximum number of points with cost](https://leetcode.com/problems/maximum-number-of-points-with-cost/)
```cpp
using ll = long long;

class Solution {
public:
    long long maxPoints(vector<vector<int>>& points) {
        int m = points.size(), n = points[0].size();
        vector<vector<ll>> dp(2,vector<ll>(n,0));
        vector<int> fw(n), bw(n); // forward/backward index
        fw[0] = 0;
        bw[n-1] = n-1;
        for (int j = 0; j < n; j++) dp[0][j] = points[0][j];
        for (int i = 1; i < m; i++) {
            int i0 = i%2, i1 = 1 - i0;
            for (int j = 1; j < n; j++) {
                fw[j] = dp[i1][j] >= dp[i1][fw[j-1]] - abs(j-fw[j-1]) ? j : fw[j-1];
            }
            for (int j = n-2; j >= 0; j--) {
                bw[j] = dp[i1][j] >= dp[i1][bw[j+1]] - abs(j-bw[j+1]) ? j : bw[j+1];
            }
            for (int j = 0; j < n; j++) {
                dp[i0][j] = max(dp[i1][bw[j]] - abs(j-bw[j]), dp[i1][fw[j]] - abs(j-fw[j])) + points[i][j];
            }
        }
        return *max_element(dp[1-m%2].begin(),dp[1-m%2].end());
    }
};
```
- [length of the longest subsequence that sums to target](https://leetcode.com/problems/length-of-the-longest-subsequence-that-sums-to-target/)
```cpp
class Solution {
public:
    int lengthOfLongestSubsequence(vector<int>& nums, int target) {
        vector<int> dp(target+1,-1e9);
        dp[0] = 0;
        for (int &d : nums) {
            for (int i = target; i >= d; i--) dp[i] = max(dp[i], dp[i-d]+1);
        }
        return max(-1, dp[target]);
    }
};
```
- length of the shortest subsequence that sums to target
```cpp
class Solution {
public:
	vector<int> backtrack(vector<int> &trace, int target) {
		vector<int> ans;
		while (target) {
			ans.push_back(target-trace[target]);
			target = trace[target];
		}
		return ans;
	}

	vector<int> shortestSubsequence(vector<int> &nums, int target) {
		sort(nums.begin(),nums.end(),greater<int>());
		vector<int> ans;
		vector<int> dp(target+1,1e9), trace(target+1);
		dp[0] = 0;
		for (int &d : nums) {
			for (int i = target; i >= d; i--) {
				if (dp[i-d] != 1e9 && dp[i-d]+1<dp[i]) {
					dp[i] = dp[i-d]+1;
					trace[i] = i-d;
					if (i == target) ans = backtrack(trace,target); // backtracking after forloop can cause wrong results
				}
			}
		}
		if (dp[target] == 1e9) return {};
		return ans;
	}
};

// failed with simple test case
// int totalAmount = 12345;
// vector<pii> denominationList{
// {1, 100},   {5, 100},    {10, 100},   {50, 100},   {100, 1},
// {500, 100}, {1000, 100}, {2000, 100}, {5000, 100}, {10000, 100}};
```
- [maximum total reward using operations i](https://leetcode.com/problems/maximum-total-reward-using-operations-i/)
```cpp
int dp[2001][4002];

class Solution {
public:
	// pick/notpick solution (slow but not TLE)
    int solve(vector<int> &values, int i = 0, int m = 0) {
        if (i == values.size()) return 0;
        if (dp[i][m] != -1) return dp[i][m];
        int ans = solve(values, i+1, m);
        if (values[i] > m) ans = max(ans, solve(values, i+1, m+values[i]) + values[i]);
        return dp[i][m] = ans;
    }

    int maxTotalReward(vector<int>& values) {
        memset(dp, -1, sizeof(dp));
        sort(values.begin(),values.end());
        // remove duplicated values
        int n = 1; // new size of values
		for (int i = 1; i < values.size(); i++) if (values[i] != values[i-1]) swap(values[i], values[n++]);
		values.resize(n);
        return solve(values);
    }

	int maxTotalRewardBetter(vector<int>& values) {
        sort(values.begin(),values.end());
        // remove duplicated values
        int n = 1; // new size of values
		for (int i = 1; i < values.size(); i++) if (values[i] != values[i-1]) swap(values[i], values[n++]);
		values.resize(n);

		int dp[4002] = {0}; // dp[v] is max total reward taken from values[i..] after receiving v reward
		int m = values[n-1]*2;
		for (int i = n-1; i >= 0; i--) {
			for (int v = 0; v < m; v++) {
				if (v < values[i]) dp[v] = max(dp[v], values[i] + dp[v+values[i]]);
			}
		}
		return dp[0];
	}
};
```
- [maximum total reward using operations ii](https://leetcode.com/problems/maximum-total-reward-using-operations-ii/description/)
```cpp

```
- [shortest distance after road addition queries i](https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/description/)
```cpp
class Solution {
public:
    vector<int> shortestDistanceAfterQueries(int n, vector<vector<int>>& queries) {
        vector<int> dist(n); // dist[i] is distance from 0 to i
        iota(dist.rbegin(),dist.rend(),0);
        vector<int> ans;
        vector<vector<int>> next(n,vector<int>());
        for (auto &q : queries) {
            next[q[0]].push_back(q[1]);
            // dist from q[1] to n-1 is unchanged, all dist from [0..q[0]] to q[1] are changed because there is dist from i to i+1
            for (int i = q[0]; i >= 0; i--) {
                dist[i] = min(dist[i], dist[i+1]+1);
                for (int &j : next[i]) dist[i] = min(dist[i], dist[j]+1);
            }
            ans.push_back(dist[0]);
        }
        return ans;
    }
};
```
- [maximum number of points with cost](https://leetcode.com/problems/maximum-number-of-points-with-cost/)
```cpp
using ll = long long;

class Solution {
public:
    long long maxPoints(vector<vector<int>>& points) {
        int m = points.size(), n = points[0].size();
        vector<vector<ll>> dp(2, vector<ll>(n)); // dp[i][j] is maximum points after taking points[i][j]
        vector<int> fw(n), bw(n); // fw[j] (forward: left-to-right), bw[j] (backward: right-to-left) is best column index of previous row that maximize dp[i][j]
        for (int j = 0; j < n; j++) dp[0][j] = points[0][j];
        for (int i = 1; i < m; i++) {
            int i0 = i&1, i1 = 1-i0;
            fw[0] = 0;
            for (int j = 1; j < n; j++) {
                fw[j] = dp[i1][j] >= dp[i1][fw[j-1]] - abs(j-fw[j-1]) ? j : fw[j-1];
            }
            bw[n-1] = n-1;
            for (int j = n-2; j >= 0; j--) {
                bw[j] = dp[i1][j] >= dp[i1][bw[j+1]] - abs(j-bw[j+1]) ? j : bw[j+1];
            }
            for (int j = 0; j < n; j++) {
                dp[i0][j] = max(dp[i1][fw[j]] - abs(j-fw[j]), dp[i1][bw[j]] - abs(j-bw[j])) + points[i][j];
            }
        }
        m = 1 - (m&1); // index of row m-1
        return *max_element(dp[m].begin(),dp[m].end());
    }
};
```
- [strange printer](https://leetcode.com/problems/strange-printer/)
```cpp
class Solution {
public:
    // minimum steps to make s[i..j]
    int solve(string &s, vector<vector<int>> &dp, int i, int j) {
        if (i > j) return 0;
        if (dp[i][j] != -1) return dp[i][j];
        if (s[i] == s[j]) return dp[i][j] = solve(s, dp, i, j-1); // make s[i..j] = a..a, and update s[i..j)
        int ans = solve(s, dp, i, j-1) + 1; // update s[i..j) and insert s[j]
        for (int k = i+1; k < j; k++) {
            if (s[k] == s[j]) {
                // solve(s, dp, i, k-1): solve s[i..k)
                // solve(s, dp, k, j-1): make s[k..j] = 'a..a', and update s[k..j)
                ans = min(ans, solve(s, dp, i, k-1) + solve(s, dp, k, j-1));
            }
        }
        return dp[i][j] = ans;
    }

    int strangePrinter(string s) {
        // remove duplicate consecutive characters
        int n = 0;
        for (char &c : s) if (c != s[n]) s[++n] = c;
        s.resize(++n);

        vector<vector<int>> dp(n,vector<int>(n,-1));
        for (int i = 0; i < n; i++) dp[i][i] = 1;
        return solve(s, dp, 0, n-1);
    }
};
```
- [length of longest increasing subsequence](https://leetcode.com/problems/longest-increasing-subsequence)
```cpp
// O(n)
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();
        vector<int> q{nums[0]};
        for (int i = 1; i < n; i++) {
            int j = lower_bound(q.begin(), q.end(), nums[i]) - q.begin();
            if (j < q.size()) {
                q[j] = nums[i];
            } else {
                q.push_back(nums[i]);
            }
        }
        return q.size();
    }
};
// O(n^2)
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();
        vector<int> dp(n, 1);
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[i] > nums[j]) dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        return *max_element(dp.begin(), dp.end());
    }
};
```
- [length of the longest increasing path](https://leetcode.com/problems/length-of-the-longest-increasing-path/description/)
```cpp
class Solution {
public:
    int lis1(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        vector<int> q{nums[0]};
        int j = 0;
        for (int i = 1; i < n; i++) {
            j = lower_bound(q.begin(), q.end(), nums[i]) - q.begin();
            if (j < q.size()) {
                q[j] = nums[i];
            } else {
                q.push_back(nums[i]);
            }
        }
        return j; // keep the last element
    }
    
    int lis2(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        vector<int> q{nums[0]};
        for (int i = 1; i < n; i++) {
            int j = lower_bound(q.begin(), q.end(), nums[i]) - q.begin();
            if (j < q.size()) {
                if (j > 0) q[j] = nums[i]; // keep the first element
            } else {
                q.push_back(nums[i]);
            }
        }
        return q.size();
    }
    
    int maxPathLength(vector<vector<int>>& a, int k) {
        int n = a.size();
        int x0 = a[k][0], y0 = a[k][1];
        sort(a.begin(),a.end(),[](vector<int> &x, vector<int> &y) { return x[0] == y[0] ? x[1] > y[1] : x[0] < y[0]; }); // to avoid selecting 2 points with same x
        int l = lower_bound(a.begin(),a.end(),x0,[](const vector<int> &ai, int v) { return ai[0] < v; }) - a.begin();
        int r = upper_bound(a.begin(),a.end(),x0,[](int v, const vector<int> &ai) { return v < ai[0]; }) - a.begin();
        vector<int> q1;
        for (int i = 0; i < l; i++) q1.push_back(a[i][1]);
        q1.push_back(y0);
        vector<int> q2{y0};
        for (int i = r; i < n; i++) q2.push_back(a[i][1]);
        return lis1(q1)+lis2(q2);
    }
};
```
- [find the longest substring containing vowels in even counts](https://leetcode.com/problems/find-the-longest-substring-containing-vowels-in-even-counts)
```cpp
class Solution {
public:
    int get_idx(char c) {
      switch (c) {
        case 'a':
          return 0;
        case 'e':
          return 1;
        case 'i':
          return 2;
        case 'o':
          return 3;
        case 'u':
          return 4;
        default:
          return -1;
      }
    }

    int findTheLongestSubstring(string s) {
      int n = s.length();
      int q[32]; // 2^5 states
      memset(q, -1, sizeof(q));
	      q[0] = 0; // zero for all vowels
      int ans = 0;
      int m = 0;
      for (int i = 0; i < n; i++) {
        int t = get_idx(s[i]);
        if (t != -1) m ^= 1<<t;
        if (q[m] == -1) q[m] = i+1;
        ans = max(ans, i-q[m]+1);
      }
      return ans;
    }
};
```
- [painting the grid with three different colors](https://leetcode.com/problems/painting-a-grid-with-three-different-colors)
```cpp
using ll = long long;
constexpr int mod = 1e9+7;

class Solution {
public:
    int dp[1001][1024] = {};

    // curr is state of current column j (from row 0 to row i-1), if i = 0, curr = 0
    // prev is state of entire previous column j-1
    int colorTheGrid(int m, int n, int i = 0, int j = 0, int curr = 0, int prev = 0) {
      if (i == m) return colorTheGrid(m, n, 0, j+1, 0, curr); // move to next column, curr becomes prev
      if (j == n) return 1;
      if (i == 0 && dp[j][prev]) return dp[j][prev]; // check for first row only
      // get color of left and up cells
      int left = (prev>>(i*2))&3, up = i == 0 ? 0 : (curr>>((i-1)*2))&3;
      ll ans = 0;
      for (int k = 1; k <= 3; k++) {
        if (k == left || k == up) continue;
        int mask = k<<(i*2);
        curr ^= mask; // set color of current cell
        ans += colorTheGrid(m, n, i+1, j, curr, prev);
        curr ^= mask;
      }
      if (i == 0) return dp[j][prev] = ans%mod;
      return ans%mod;
    }
};
```
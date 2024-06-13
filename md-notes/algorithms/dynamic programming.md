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
		vector<int> ans;
		vector<int> dp(target+1,1e9), trace(target+1,0);
		dp[0] = 0;
		for (int &d : nums) {
			for (int i = target; i >= d; i--) {
				if (dp[i-d]+1<dp[i]) {
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
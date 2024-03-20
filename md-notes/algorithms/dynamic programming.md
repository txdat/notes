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
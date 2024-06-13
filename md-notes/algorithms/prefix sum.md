- [special array ii](https://leetcode.com/problems/special-array-ii/)
```cpp
class Solution {
public:
    vector<bool> isArraySpecial(vector<int>& nums, vector<vector<int>>& queries) {
        int n = nums.size();
        vector<int> a{0};
        nums[0] &= 1;
        for (int i = 1; i < n; i++) {
            nums[i] &= 1;
            a.push_back(a.back()+(nums[i-1] == nums[i]));
        }

        vector<bool> ans;
        for (auto &q : queries) {
            ans.push_back(a[q[0]] == a[q[1]]); // if between q[0] and q[1], there is a adjecent elements with same parity, prefix sum will change
        }
        return ans;
    }
};
```
- [make sum divisible by p](https://leetcode.com/problems/make-sum-divisible-by-p/description/)
```cpp
using ll = long long;

class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        int n = nums.size();
        int r = accumulate(nums.begin(),nums.end(),0ll)%p;
        if (r == 0) return 0;

        unordered_map<int,int> m;
        m[0] = -1;
        int ans = n;
        for (int i = 0, s = 0; i < n; i++) {
            s += nums[i];
            s %= p;
            int t = s - r;
            if (t < 0) t += p;
            if (m.find(t) != m.end()) ans = min(ans, i-m[t]);
            m[s] = i;
        }
        return ans == n ? -1 : ans;
    }
};
```
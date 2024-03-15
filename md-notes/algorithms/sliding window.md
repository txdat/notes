1. [binary subarrays with sum](https://leetcode.com/problems/binary-subarrays-with-sum/)
```cpp
class Solution {
public:
    int at_most(vector<int> &nums, int goal) {
        int n = nums.size();
        int ans = 0;
        for (int i = 0, j = 0, s = 0; i < n; i++) {
            s += nums[i];
            while (s > goal) s -= nums[j++];
            ans += i-j+1;
        }
        return ans;
    }

    int numSubarraysWithSum(vector<int>& nums, int goal) {
        return at_most(nums,goal) - (goal ? at_most(nums,goal-1) : 0);
    }
};
```
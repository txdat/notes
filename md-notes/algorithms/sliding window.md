1. [binary subarrays with sum](https://leetcode.com/problems/binary-subarrays-with-sum/)
```cpp
class Solution {
public:
    int count(vector<int> &nums, int goal) {
        int n = nums.size();
        int ans = 0;
        for (int i = 0, j = 0, s = 0; j < n; j++) {
            s += nums[j];
            while (s > goal) {
                s -= nums[i++];
            }
            ans += j-i+1;
        }
        return ans;
    }

    int numSubarraysWithSum(vector<int>& nums, int goal) {
        return count(nums,goal) - (goal ? count(nums,goal-1) : 0);
    }
};```
2. [subarrays with k different integers](https://leetcode.com/problems/subarrays-with-k-different-integers/description/)
```cpp
// using 2 hashmaps to store counts and last index
class Solution1 {
public:
    int subarraysWithKDistinct(vector<int>& nums, int k) {
        int cnt[20001] = {0}, last[20001];
        int n = nums.size();
        int ans = 0;
        for (int i = 0, j = 0, c = 0; j < n; j++) {
            last[nums[j]] = j;
            if (cnt[nums[j]]++ == 0) c++;
            while (c > k) {
                if (--cnt[nums[i]] == 0) c--;
                i++;
            }
            if (c == k) {
                int l = j;
                for (int t = i; t <= j; t++) l = min(l,last[nums[t]]);
                ans += l-i+1;
            }
        }

        return ans;
    }
};

// count at-most
class Solution {
public:
    int cnt[20001];

    // count number of subarrays with number of distinct integers less than or equal k
    int count(vector<int> &nums, int k) {
        memset(cnt,0,sizeof(cnt));
        int n = nums.size();
        int ans = 0;
        for (int i = 0, j = 0, c = 0; j < n; j++) {
            if (cnt[nums[j]]++ == 0) c++;
            while (c > k) {
                if (--cnt[nums[i]] == 0) c--;
                i++;
            }
            ans += j-i+1;
        }
        return ans;
    }

    int subarraysWithKDistinct(vector<int>& nums, int k) {
        return count(nums,k) - (k ? count(nums,k-1) : 0);
    }
};
```
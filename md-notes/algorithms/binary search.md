1. [earliest second to mark indices i](https://leetcode.com/problems/earliest-second-to-mark-indices-i/description/)
```cpp
class Solution {
public:
    bool check(vector<int> &nums, vector<int> &changeIndices, int t) {
        int n = nums.size();
        vector<int> last(n,-1);
        for (int i = 0; i <= t; i++) last[changeIndices[i]] = i;
        for (int i = 0; i < n; i++) if (last[i] == -1) return false; // contain non-markable indices

        for (int i = 0, c = 0; i <= t; i++) {
            if (last[changeIndices[i]] == i) { // if current index i is last index to mark nums[i]
                c -= nums[changeIndices[i]];
                if (c < 0) return false;
            } else {
                c++;
            }
        }
        return true;
    }

    int earliestSecondToMarkIndices(vector<int>& nums, vector<int>& changeIndices) {
        for (int &i : changeIndices) i--;
        int n = changeIndices.size(), l = 0, r = n, m;
        while (l < r) {
            m = (l+r) >> 1;
            if (check(nums, changeIndices, m)) {
                r = m;
            } else {
                l = m+1;
            }
        }
        return l == n ? -1 : l+1;
    }
};
```
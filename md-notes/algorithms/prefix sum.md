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
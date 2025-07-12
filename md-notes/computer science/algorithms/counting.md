- [maximum frequency after subarray operation](https://leetcode.com/problems/maximum-frequency-after-subarray-operation/description/)
```cpp
# kadane algo
class Solution {
public:
    int maxFrequency(vector<int>& nums, int k) {
        int s = 0;
        for (int m = 1; m <= 50; m++) {
            if (m == k) continue;
            int t = 0; // t is cost to change m to k (number of m in subarray)
            for (int &d : nums) {
                t += d == m ? 1 : d == k ? -1 : 0;
                t = max(t, 0); // if t < 0, there are more k in subarray than others, ignore subarray
                s = max(s, t);
            }
        }
        s += count(nums.begin(), nums.end(), k);
        return s;
    }
};
```
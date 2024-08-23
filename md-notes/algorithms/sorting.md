1. [find the number of ways to place people ii](https://leetcode.com/problems/find-the-number-of-ways-to-place-people-ii/description/)
```cpp
class Solution {
public:
    int numberOfPairs(vector<vector<int>>& points) {
        int n = points.size();
        sort(points.begin(), points.end(), [](vector<int> &p1, vector<int> &p2) {
            return p1[0] == p2[0] ? p1[1] > p2[1] : p1[0] < p2[0]; // x inc, y dec
        });
        int ans = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1, y = INT_MIN; j < n; j++) {
                if (points[j][1] <= points[i][1] && y < points[j][1]) {
                    ans++;
                    y = points[j][1];
                }
            }
        }
        return ans;
    }
};
```
- [maximum gap - O(n)](https://leetcode.com/problems/maximum-gap/description/)
```cpp
// bucket sort?
class Solution {
public:
    void _sort(vector<int> &nums, int l, int r, int i) {
        if (l >= r || i < 0) return;
        int m = 1<<i, t = l;
        for (int j = l; j <= r; j++) if ((nums[j]&m) == 0) swap(nums[j],nums[t++]);
        _sort(nums, l, t-1, --i);
        _sort(nums, t, r, i);
    }

    int maximumGap(vector<int>& nums) {
        int mx = *max_element(nums.begin(),nums.end());
        _sort(nums, 0, nums.size()-1, 31-__builtin_clz(mx));
        int ans = 0;
        for (int i = 1; i < nums.size(); i++) ans = max(ans, nums[i]-nums[i-1]);
        return ans;
    }
};
```
- [sort an array - radix sort](https://leetcode.com/problems/sort-an-array/description/)
```cpp
class Solution {
public:
    void sort01(vector<int> &a, int l, int r, int m) {
        if (l >= r || m == 0) return;
        int j = r;
        for (int i = l; i <= j;) {
            if (a[i]&m) {
                swap(a[i],a[j--]);
            } else {
                i++;
            }
        }
        m>>=1;
        sort01(a,l,j,m);
        sort01(a,j+1,r,m);
    }

    vector<int> sortArray(vector<int>& nums) {
        int t = 5*10e4;
        for (int &d : nums) d += t;
        sort01(nums,0,nums.size()-1,1<<30);
        for (int &d : nums) d -= t;
        return nums;
    }
};
```

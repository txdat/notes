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
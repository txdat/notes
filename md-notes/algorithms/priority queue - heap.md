- [maximum subsequence score](https://leetcode.com/problems/maximum-subsequence-score/description/)
```cpp
using ll = long long;

class Solution {
public:
    long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
        int n = nums1.size();
        vector<int> idx(n);
        iota(idx.begin(), idx.end(), 0);
        sort(idx.begin(), idx.end(), [&](int i, int j) { return nums2[i] < nums2[j]; });

        priority_queue<int,vector<int>,greater<int>> q;
        ll s = 0;
        for (int i = n-1; i > n-k; i--) {
            int d = nums1[idx[i]];
            s += d;
            q.push(d);
        }
        ll ans = 0;
        for (int i = n-k; i >= 0; i--) {
            int d = nums1[idx[i]];
            s += d;
            q.push(d);
            ans = max(ans, s*nums2[idx[i]]);
            s -= q.top();
            q.pop();
        }
        return ans;
    }
};
```
- [minimum cost to hire k workers](https://leetcode.com/problems/minimum-cost-to-hire-k-workers/description/)
```cpp
class Solution {
public:
    double mincostToHireWorkers(vector<int>& quality, vector<int>& wage, int k) {
        int n = quality.size();
        vector<double> w;
        for (int i = 0; i < n; i++) w.push_back(double(wage[i])/quality[i]); // compare worker's efficiency
        vector<int> idx(n);
        iota(idx.begin(),idx.end(),0);
        sort(idx.begin(),idx.end(),[&](int i, int j) { return w[i] < w[j]; }); // increasing efficiency

        double ans = INT_MAX;
        int total = 0;
        priority_queue<int> q;
        for (int i = 0; i < k-1; i++) {
            int qi = quality[idx[i]];
            total += qi;
            q.push(qi);
        }
        for (int i = k-1; i < n; i++) {
            int qi = quality[idx[i]];
            total += qi;
            q.push(qi);
            ans = min(ans, w[idx[i]]*total);
            total -= q.top();
            q.pop();
        }
        return ans;
    }
};
```
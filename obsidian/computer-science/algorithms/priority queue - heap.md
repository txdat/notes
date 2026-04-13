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
- get k-th element
	- minimum -> max-heap priority queue
	- maximum -> min-heap priority queue
- [find x-sum of all k-long subarrays ii](https://leetcode.com/problems/find-x-sum-of-all-k-long-subarrays-ii)
```cpp
using ll = long long;
using pii = pair<int,int>;

class Solution {
public:
    void add(unordered_map<int,int> &m, set<pii,greater<pii>> &top, set<pii,greater<pii>> &rest, ll &s, int x, int d) {
        auto &c = m[d];
        pii p = {c,d};
        if (top.find(p) != top.end()) {
            top.erase(p);
            s -= 1ll*c*d;
        } else {
            rest.erase(p);
        }
        
		// add new pair to top to move smallest of top to rest if necessary
        top.insert({++c,d});
        s += 1ll*c*d;
        if (top.size() > x) {
            auto it = prev(top.end());
            s -= 1ll*it->first*it->second;
            rest.insert(*it);
            top.erase(it);
        }
    }

    void sub(unordered_map<int,int> &m, set<pii,greater<pii>> &top, set<pii,greater<pii>> &rest, ll &s, int x, int d) {
        auto &c = m[d];
        pii p = {c,d};
        if (top.find(p) != top.end()) {
            top.erase(p);
            s -= 1ll*c*d;
        } else {
            rest.erase(p);
        }

        if (--c == 0) {
            m.erase(d);
        } else {
	        // add new pair to rest to move largest of rest to top if necessary
            rest.insert({c,d});
        }

        if (top.size() < x && !rest.empty()) {
            auto it = rest.begin();
            top.insert(*it);
            s += 1ll*it->first*it->second;
            rest.erase(it);
        }
    }

    vector<long long> findXSum(vector<int>& nums, int k, int x) {
        int n = nums.size();
        unordered_map<int,int> m;
        set<pii,greater<pii>> top, rest; // maintain 2 set(heap) [...top, ...rest] of sliding window
        ll s = 0;

        for (int i = 0; i < k; i++) add(m, top, rest, s, x, nums[i]);

        vector<ll> ans{s};
        for (int i = k; i < n; i++) {
            sub(m, top, rest, s, x, nums[i-k]);
            add(m, top, rest, s, x, nums[i]);
            ans.push_back(s);
        }
        return ans;
    }
};
```
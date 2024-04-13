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
- [kth smallest amount with single denomination combination](https://leetcode.com/problems/kth-smallest-amount-with-single-denomination-combination/description/)
```cpp
using ll = long long;

class Solution {
public:
	// count nubmer of denimiations less than or equal to m
    ll count(vector<vector<pair<ll,int>>> &q, ll m) {
        ll ans = 0;
        ll s = 1;
        for (int i = 1; i < q.size(); i++) {
            for (auto [d, _] : q[i]) {
                ans += s*m/d;
            }
            s *= -1;
        }
        return ans;
    }
    
    long long findKthSmallest(vector<int>& coins, int k) {
        int n = coins.size();
        vector<vector<pair<ll,int>>> q;
        q.push_back(vector<pair<ll,int>>{{1,0}});
        unordered_set<int> t; // store state of combinations - bitmask
        for (int l = 1; l <= n; l++) {
            auto &r = q.back();
            vector<pair<ll,int>> v;
            for (auto [d,m] : r) {
                for (int i = 0; i < n; i++) {
                    int mi = m|(1<<i); // new state
                    if (t.find(mi) != t.end()) continue;
                    t.insert(mi);
                    ll di = d*coins[i]/gcd(d,coins[i]); // find lowest common multiplier - lcm
                    v.push_back({di,mi});
                }
            }
            q.push_back(v);
        }
        
        ll l = 0, r = 1e15, m;
        while (l < r) {
            m = l+(r-l)/2;
            ll c = count(q, m);
            if (c >= k) {
                r = m;
            } else {
                l = m+1;
            }
        }
        return r;
    }
};
```
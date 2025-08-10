- [block placement queries](https://leetcode.com/problems/block-placement-queries/description/)
```cpp

```
- [peeks in array](https://leetcode.com/problems/peaks-in-array/)
```cpp
class Solution {
public:
    void build_st(vector<int> &st, vector<int> &arr, int l, int r, int i = 1) {
        if (l == r) {
            st[i] = arr[l];
            return;
        }
        int m = (l+r)>>1, j = i<<1;
        build_st(st,arr,l,m,j);
        build_st(st,arr,m+1,r,j+1);
        st[i] = st[j] + st[j+1];
    }
    
    void update_st(vector<int> &st, int l, int r, int k, int v, int i = 1) {
        if (k < l || k > r) return;
        if (l == r) {
            st[i] = v;
            return;
        }
        int m = (l+r)>>1, j = i<<1;
        update_st(st,l,m,k,v,j);
        update_st(st,m+1,r,k,v,j+1);
        st[i] = st[j]+st[j+1];
    }
    
    // query [u,v] of nums
    int get_val(vector<int> &st, int l, int r, int u, int v, int i = 1) {
        if (v < l || u > r) return 0;
        if (u <= l && r <= v) return st[i];
        int m = (l+r)>>1, j = i<<1;
        return get_val(st,l,m,u,v,j)+get_val(st,m+1,r,u,v,j+1);
    }
    
    vector<int> countOfPeaks(vector<int>& nums, vector<vector<int>>& queries) {
        int n = nums.size();
        vector<int> arr(n,0);
        for (int i = 1; i < n-1; i++) if (nums[i] > nums[i-1] && nums[i] > nums[i+1]) arr[i] = 1;
    
        vector<int> st(4*n);
        build_st(st, arr, 0, n-1);
        
        vector<int> ans;
        for (auto &q : queries) {
            if (q[0] == 1) {
                ans.push_back(get_val(st, 0, n-1, q[1]+1, q[2]-1));
            } else {
                nums[q[1]] = q[2];
                for (int t : {-1, 0, 1}) {
                    int i = q[1] + t;
                    if (i > 0 && i < n-1) {
                        int v = nums[i] > nums[i-1] && nums[i] > nums[i+1];
                        if (arr[i] != v) {
	                        update_st(st, 0, n-1, i, v);
	                        arr[i] = v;
	                    }
                    }
                }
            }
        }
        return ans;
    }
};
```
- [fruits into baskets iii](https://leetcode.com/problems/fruits-into-baskets-iii/description/)
```cpp
// use segment tree ST to track largest basket in range [l,r], but too slow
class Solution {
public:
    int build_st(vector<int> &st, vector<int> &baskets, int l, int r, int i = 1) {
        if (l == r) {
            return st[i] = baskets[l];
        }
        int m = (l+r)>>1, ii = i<<1;
        return st[i] = max(build_st(st, baskets, l, m, ii), build_st(st, baskets, m+1, r, ii+1));
    }

    int update_st(vector<int> &st, int l, int r, int k, int v, int i = 1) {
        if (k < l || k > r) return st[i];
        if (l == r) return st[i] = v;
        int m = (l+r)>>1, ii = i<<1;
        return st[i] = max(update_st(st, l, m, k, v, ii), update_st(st, m+1, r, k, v, ii+1));
    }

    int query(vector<int> &st, int l, int r, int u, int v, int i = 1) {
        if (v < l || u > r) return 0;
        if (u <= l && r <= v) return st[i];
        int m = (l+r)>>1, ii = i<<1;
        return max(query(st, l, m, u, v, ii), query(st, m+1, r, u, v, ii+1));
    }

    int numOfUnplacedFruits(vector<int>& fruits, vector<int>& baskets) {
        int n = fruits.size();
        vector<int> st(4*n);
        build_st(st, baskets, 0, n-1);
        int ans = 0;
        for (int &d : fruits) {
            int l = 0, r = n, m;
            while (l < r) {
                m = (l+r)>>1;
                int v = query(st, 0, n-1, 0, m);
                if (v >= d) {
                    r = m;
                } else {
                    l = m+1;
                }
            }
            if (l < n) {
                update_st(st, 0, n-1, l, 0);
            } else {
                ans++;
            }
        }
        return ans;
    }
};
```
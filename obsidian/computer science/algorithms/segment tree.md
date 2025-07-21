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
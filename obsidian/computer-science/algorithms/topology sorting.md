- [build a matrix with conditions](https://leetcode.com/problems/build-a-matrix-with-conditions)
```cpp
class Solution {
public:
    bool dfs(vector<vector<int>> &g, vector<int> &q, int i, int d = 0) {
        if (q[i] == -2) return false; // graph has a cycle
        if (d <= q[i]) return true;
        q[i] = -2;
        d++;
        for (int &j : g[i]) if (!dfs(g, q, j, d)) return false;
        q[i] = --d;
        return true;
    }

    vector<int> topo_sort(int k, vector<vector<int>> &conds) {
        vector<vector<int>> g(k+1,vector<int>());
        for (auto &p : conds) g[p[1]].push_back(p[0]);
        vector<int> q(k+1,-1);
        for (int i = 1; i <= k; i++) {
            if (q[i] != -1) continue;
            if (!dfs(g, q, i)) return {};
        }
        // keep only one number in each row/col
        vector<int> idx(k+1);
        iota(idx.begin(),idx.end(),0);
        sort(idx.begin(),idx.end(),[&](int i, int j) { return q[i] < q[j]; });
        for (int i = 1; i <= k; i++) q[idx[i]] = k-i; // change direction
        return q;
    }

    vector<vector<int>> buildMatrix(int k, vector<vector<int>>& rowConditions, vector<vector<int>>& colConditions) {
        auto row = topo_sort(k, rowConditions);
        if (row.empty()) return {};
        auto col = topo_sort(k, colConditions);
        if (col.empty()) return {};
        vector<vector<int>> ans(k,vector<int>(k,0));
        for (int i = 1; i <= k; i++) ans[row[i]][col[i]] = i;
        return ans;
    }
};
```
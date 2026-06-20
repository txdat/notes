- [balance a binary search tree](https://leetcode.com/problems/balance-a-binary-search-tree/)
```cpp

```
- [number of good leaf node pairs](https://leetcode.com/problems/number-of-good-leaf-nodes-pairs/)
```cpp

```
- [find duplicate subtrees](https://leetcode.com/problems/find-duplicate-subtrees/)
```cpp
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    string dfs(TreeNode *root, unordered_map<string,pair<int,TreeNode*>> &q) {
        if (!root) return "";
        string t = dfs(root->left, q) + "$" + dfs(root->right, q) + "$" + to_string(root->val);
        if (q.find(t) == q.end()) {
            q[t] = {1, root};
        } else {
            q[t].first++; 
        }
        return t;
    }

    vector<TreeNode*> findDuplicateSubtrees(TreeNode* root) {
        unordered_map<string,pair<int,TreeNode*>> q;
        dfs(root, q);
        vector<TreeNode*> ans;
        for (auto &[_, p] : q) {
            if (p.first > 1) ans.push_back(p.second);
        }
        return ans;
    }
};
```
- [delete duplicate folders in system (duplicate subtrees)](https://leetcode.com/problems/delete-duplicate-folders-in-system)
```cpp
```
- [number of ways to assign edge weights ii](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-ii/) - LCA + binary lifting
```cpp
using ll = long long;
constexpr int MOD=1e9+7;

class Solution {
public:
    void bfs(vector<vector<int>> &g, vector<int> &depth, vector<vector<int>> &up) {
        queue<int> q;
        int n = g.size();
        vector<bool> visited(n,false);

        visited[1] = true;
        depth[1] = 0;
        q.push(1);
        while (!q.empty()) {
            int i = q.front(); q.pop();
            for (int j : g[i]) {
                if (visited[j]) continue;
                visited[j] = true;
                depth[j] = depth[i]+1;
                q.push(j);

                up[j][0] = i;
            }
        }

        // binary lifting
        for (int j = 1; j < 17; j++) {
            for (int i = 1; i < n; i++) {
                up[i][j] = up[up[i][j-1]][j-1];
            }
        }
    }

    int lca(vector<vector<int>> &up, vector<int> &depth, int u, int v) {
        if (depth[u] < depth[v]) swap(u,v);

        int d = depth[u]-depth[v];
        // decompose diff to sum of 2^i values
        for (int i = 0; i < 17; i++) {
            if ((d>>i)&1) u = up[u][i];
        }

        if (u == v) return u;

        for (int i = 16; i >= 0; i--) {
            if (up[u][i] != up[v][i]) {
                u = up[u][i];
                v = up[v][i];
            }
        }

        return up[u][0];
    }

    int pow2(int n) {
        if (n == 0) return 1;
        ll t = pow2(n>>1);
        if (n&1) return t*t*2%MOD;
        return t*t%MOD;
    }

    vector<int> assignEdgeWeights(vector<vector<int>>& edges, vector<vector<int>>& queries) {
        int n = edges.size()+1;
        vector<vector<int>> g(n+1,vector<int>());
        for (auto &e : edges) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }

        vector<int> depth(n+1);
        vector<vector<int>> up(n+1, vector<int>(17,0)); // up[i][j] is 2^j-th ancestor of i
        bfs(g, depth, up);

        vector<int> ans;
        for (auto &q : queries) {
            int t = lca(up, depth, q[0], q[1]);
            int l = depth[q[0]]+depth[q[1]] - depth[t]*2;
            ans.push_back(l ? pow2(l-1) : 0);
        }
        return ans;
    }
};
```
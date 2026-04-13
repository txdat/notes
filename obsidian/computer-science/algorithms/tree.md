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

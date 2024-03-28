1. [longest common suffix queries](https://leetcode.com/problems/longest-common-suffix-queries/)
```cpp
class Solution {
public:
    struct Node {
        Node* next[26] = {nullptr};
        int k = -1;
        int l = INT_MAX;
    };

    vector<int> stringIndices(vector<string>& words, vector<string>& queries) {
        int n = words.size();
        Node* root = new Node();
        for (int i = 0; i < n; i++) {
            auto &w = words[i];
            int l = w.length();
            // empty string
            if (l < root->l) {
                root->l = l;
                root->k = i;
            }
            
            auto curr = root;
            for (int t = l-1; t >= 0; t--) {
                int j = w[t]-'a';
                if (!curr->next[j]) curr->next[j] = new Node();
                curr = curr->next[j];
                if (l < curr->l) {
                    curr->l = l;
                    curr->k = i;
                }
            }
        }

        vector<int> ans;
        for (auto &w : queries) {
            auto curr = root;
            for (int t = w.length()-1; t >= 0; t--) {
                int j = w[t]-'a';
                if (!curr->next[j]) break;
                curr = curr->next[j];
            }
            ans.push_back(curr->k);
        }
        return ans;
    }
};
```
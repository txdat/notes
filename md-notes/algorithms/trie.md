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
2. [maximum xor of two numbers in an array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/)
```cpp
struct Node {
    Node* next[2] = {nullptr};
};

int q[31];

class Solution {
public:
    void add(Node* root, int d) {
        memset(q,0,sizeof(q));
        int i = 30;
        while (d) {
            q[i--] = d&1;
            d >>= 1;
        }

        auto curr = root;
        for (int i = 0; i < 31; i++) {
            if (!curr->next[q[i]]) curr->next[q[i]] = new Node();
            curr = curr->next[q[i]];
        }
    }

    int get(Node* root, int d) {
        memset(q,0,sizeof(q));
        int i = 30;
        while (d) {
            q[i--] = d&1;
            d >>= 1;
        }

        int ans = 0;
        auto curr = root;
        for (int i = 0; i < 31; i++) {
            ans <<= 1;
            if (curr->next[1-q[i]]) {
                ans++;
                curr = curr->next[1-q[i]];
            } else if (curr->next[q[i]]) {
                curr = curr->next[q[i]];
            } else {
                break;
            }
        }
        return ans;
    }

    int findMaximumXOR(vector<int>& nums) {
        int n = nums.size();
        auto root = new Node();
        for (int &d : nums) add(root,d);
        int ans = 0;
        for (int &d : nums) ans = max(ans, get(root,d));
        return ans;
    }
};
```
3. [maximum genetic difference query](https://leetcode.com/problems/maximum-genetic-difference-query/)
```cpp
int q[31];

void get_q(int d) {
    memset(q,0,sizeof(q));
    int i = 30;
    while (d) {
        q[i--] = d&1;
        d >>= 1;
    }
}

struct Node {
    Node* next[2] = {nullptr};
    int n = 0;
};

void add(Node* root, int d) {
    get_q(d);

    auto curr = root;
    for (int i = 0; i < 31; i++) {
        if (!curr->next[q[i]]) curr->next[q[i]] = new Node();
        curr = curr->next[q[i]];
        curr->n++;
    }
}

void remove(Node* root, int d) {
    get_q(d);

    auto curr = root;
    for (int i = 0; i < 31; i++) {
        if (--curr->next[q[i]]->n == 0) {
            curr->next[q[i]] = nullptr;
            return;
        }
        curr = curr->next[q[i]];
    }
}

int get_xor(Node* root, int d) {
    get_q(d);

    int ans = 0;
    auto curr = root;
    for (int i = 0; i < 31 && curr; i++) {
        ans <<= 1;
        if (curr->next[1-q[i]]) {
            ans++;
            curr = curr->next[1-q[i]];
        } else {
            curr = curr->next[q[i]];
        }
    }
    return ans;
}

class Solution {
public:
    vector<int> maxGeneticDifference(vector<int>& parents, vector<vector<int>>& queries) {
        int n = parents.size(), m = queries.size();
        unordered_map<int,vector<pair<int,int>>> q;
        for (int i = 0; i < m; i++) {
            q[queries[i][0]].push_back({queries[i][1],i});
        }

        vector<int> ans(m,-1);
        for (int i = 0; i < m; i++) {
            if (ans[i] != -1) continue;

            int d = queries[i][0], v = queries[i][1];
            auto root = new Node();
            while (d != -1) {
                add(root, d);
                d = parents[d];
            }

            d = queries[i][0];
            while (q != -1) {
                for (auto [v, i] : q[d]) {
                    ans[i] = get_xor(root,v);
                }
                remove(root,d);
                d = parents[d];
            }
        }
        return ans;
    }
};
```
- [construct string with minimum cost](https://leetcode.com/problems/construct-string-with-minimum-cost/) -> aho-corasick
```cpp

```
- [k-th smallest in lexicographical order](https://leetcode.com/problems/k-th-smallest-in-lexicographical-order/) (trie concept only, not implementation)
```cpp
```
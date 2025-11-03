- [longest subsequence repeated k times](https://leetcode.com/problems/longest-subsequence-repeated-k-times)
```cpp
class Solution {
public:
    // check t is a subsequence that is repeated k times in s
    bool check(string &s, string &t, int k) {
        if (t.empty()) return true;
        for (int i = 0, j = 0; i < s.length() && k > 0; i++) {
            if (s[i] == t[j] && ++j == t.length()) {
                k--;
                j = 0;
            }
        }
        return k == 0;
    }

    void dfs(string &s, string &t, string &ans, int k, int m, int *cnt) {
        int n = t.length();
        if (n > m || !check(s, t, k)) return;
        if (n > ans.length()) ans = t;
        for (int i = 25; i >= 0; i--) { // check larger subsequence first
            if (cnt[i] < k) continue;
            cnt[i] -= k;
            t.push_back('a'+i);
            dfs(s, t, ans, k, m, cnt);
            t.pop_back();
            cnt[i] += k;
        }
    }

    string longestSubsequenceRepeatedK(string s, int k) {
        // remove characters that doesnt appear greater than or equal k times
        int cnt[26] = {0};
		for (char &c : s) cnt[c-'a']++;
        int n = 0;
        for (int i = 0; i < s.length(); i++) if (cnt[s[i]-'a'] >= k) s[n++] = s[i];
        if (n == 0) return "";
        s.resize(n);
        string t, ans;
        dfs(s, t, ans, k, n/k, cnt);
        return ans;
    }
};
```

- [trapping rain water ii](https://leetcode.com/problems/trapping-rain-water-ii/description)
```cpp
constexpr int dij[4][2] = {{-1,0},{0,1},{1,0},{0,-1}};
using pii = pair<int,int>;

class Solution {
public:
    int trapRainWater(vector<vector<int>>& heightMap) {
        int m = heightMap.size(), n = heightMap[0].size(), m1 = m-1, n1 = n-1;

        auto cmp = [&](pii &p1, pii &p2) { return heightMap[p1.first][p1.second] > heightMap[p2.first][p2.second]; };
        priority_queue<pii,vector<pii>,decltype(cmp)> q(cmp);

        for (int i = 0; i < m; i++) {
            q.push({i, 0});
            q.push({i, n1});
        }
        for (int j = 1; j < n1; j++) {
            q.push({0, j});
            q.push({m1, j});
        }

        int ans = 0, h = 1;
        while (!q.empty()) {
            auto [i, j] = q.top(); q.pop();
            if (heightMap[i][j] == -1) continue;

            h = max(h, heightMap[i][j]);
            ans += h - heightMap[i][j];
            heightMap[i][j] = -1; // visited

            for (int k = 0; k < 4; k++) {
                int ii = i+dij[k][0], jj = j+dij[k][1];
                if (ii < 0 || jj < 0 || ii == m || jj == n || heightMap[ii][jj] == -1) continue;
                q.push({ii, jj});
            }
        }
        return ans;
    }
};
```
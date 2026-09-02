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
        // remove characters that doesn't appear greater than or equal k times
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

- [minimum moves to clean the classroom](https://leetcode.com/problems/minimum-moves-to-clean-the-classroom) -> BFS with bitmask
```cpp
constexpr int dij[4][2] = {{-1,0},{0,1},{1,0},{0,-1}};

class Solution {
public:
    int minMoves(vector<string>& grid, int e0) {
        int m = grid.size(), n = grid[0].size();
        int i0 = 0, j0 = 0, l_cnt = 0;
        unordered_map<int,unordered_map<int,int>> l_map;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == 'S') {
                    i0 = i;
                    j0 = j;
                } else if (grid[i][j] == 'L') {
                    l_map[i][j] = l_cnt++;
                }
            }
        }

        if (l_cnt == 0) return 0;

        vector<vector<vector<int>>> e_max(m,vector<vector<int>>(n,vector<int>(1<<l_cnt,-1))); // maximum energy of visited state s at (i,j)
        int mask = (1<<l_cnt)-1;

        queue<array<int,4>> q;
        q.push({i0,j0,e0,0});
        for (int moves = 0; !q.empty(); moves++) {
            for (int sz = q.size(); sz > 0; sz--) {
                auto [i,j,e,s] = q.front(); q.pop();

                if (grid[i][j] == 'R') {
                    e = e0;
                } else if (grid[i][j] == 'L') {
                    s |= 1<<l_map[i][j];
                    if (s == mask) return moves;
                }

                if (e <= e_max[i][j][s]) continue;
                e_max[i][j][s] = e;

                if (e == 0) continue;
                e--;
                for (int k = 0; k < 4; k++) {
                    int ii = i+dij[k][0], jj = j+dij[k][1];
                    if (ii < 0 || jj < 0 || ii == m || jj == n || grid[ii][jj] == 'X') continue;
                    q.push({ii,jj,e,s});
                }
            }
        }
        return -1;
    }
};
```
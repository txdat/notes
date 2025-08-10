1. dijkstra
```cpp
// g: {i: [{cost_ij, j},...]}
int shortest_path(vector<vector<pair<int,int>>> &g, int s, int t) {
	auto cmp = [&](pair<int,int> &p1, pair<int,int> &p2) { return p1.first > p2.first; }; // minimum queue
	priority_queue<pair<int,int>, vector<pair<int,int>>, decltype(cmp)> q;
	q.push({0, s});
	int n = g.size();
	vector<bool> visited(n, false);
	while (!q.empty()) {
		auto [c, i] = q.top();
		q.pop();
		if (i == t) return c;
		if (visited[i]) continue;
		visited[i] = true;
		for (auto [cj, j] : g[i]) {
			if (visited[j]) continue;
			q.push({c + cj, j});
		}
	}
	return -1;
}
```
2. floyd-warshall
```cpp
// find shortest path for any i, j
// g: {i: [{cost_ij,j},...]}
vector<vector<int>> shortest_path(vector<vector<pair<int,int>>> &g) {
	int n = g.size();
	vector<vector<int>> dist(n, vector<int>(n, INT_MAX));
	for (int i = 0; i < n; i++) {
		dist[i][i] = 0;
		for (auto [c, j] : g[i]) {
			dist[i][j] = c;
		}
	}
	for (int k = 0; k < n; k++) {
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++) dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
		}
	}
	return dist;
}
```
3. [minimum obstacle removal to reach corner](https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner)
- solved by djikstra
```cpp
using ia3 = array<int,3>; // {cost,x,y}

constexpr int dx[4] = {-1, 0, 1, 0}, dy[4] = {0, 1, 0, -1};

class Solution {
public:
    int minimumObstacles(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        priority_queue<ia3, vector<ia3>, greater<ia3>> q;
        q.push({grid[0][0], 0, 0});
        while (!q.empty()) {
            auto p = q.top(); q.pop();
            if (grid[p[1]][p[2]] == 2) continue; // visited
            grid[p[1]][p[2]] = 2;
            if (p[1] == m - 1 && p[2] == n - 1) return p[0];
            for (int i = 0; i < 4; i++) {
                int x = p[1] + dx[i], y = p[2] + dy[i];
                if (x < 0 || y < 0 || x == m || y == n || grid[x][y] == 2) continue;
                q.push({p[0] + grid[x][y], x, y});
            }
        }
        return -1;
    }
};
```
- using dfs
```cpp
using pii = pair<int,int>;

constexpr int dx[4] = {-1, 0, 1, 0}, dy[4] = {0, 1, 0, -1};

class Solution {
public:
    int minimumObstacles(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        vector<vector<int>> dp(m, vector<int>(n, -1));
        dp[0][0] = 0;
        deque<pii> q{{0,0}};
        while (!q.empty()) {
            auto [x, y] = q.front(); q.pop_front();
            for (int i = 0; i < 4; i++) {
                int xi = x + dx[i], yi = y + dy[i];
                if (xi < 0 || yi < 0 || xi == m || yi == n || dp[xi][yi] != -1) continue;
                dp[xi][yi] = dp[x][y] + grid[xi][yi];
                if (grid[xi][yi]) {
                    q.push_back({xi,yi});
                } else {
                    q.push_front({xi,yi});
                }
            }
        }
        return dp[m - 1][n - 1];
    }
};
```
4. [cheapest flights within k stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/)
```cpp
using ia2 = array<int,2>;
using ia3 = array<int,3>;

class Solution {
public:
	// too slow :(
    int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
        vector<vector<ia2>> g(n,vector<ia2>());
        for (auto &f : flights) g[f[0]].push_back({f[2],f[1]});

        k++; // include dst
        priority_queue<ia3,vector<ia3>,greater<ia3>> q;
        q.push({0, 0, src});
        vector<vector<bool>> visited(k+1,vector<bool>(n,false)); // state is {step,stop}
        while (!q.empty()) {
            auto p = q.top(); // {cost,stop,cnt}
            q.pop();
            if (visited[p[1]][p[2]]) continue;
            visited[p[1]][p[2]] = true;
            if (p[2] == dst) return p[0];
            p[1]++;
            for (auto &s : g[p[2]]) {
                if (p[1] > k || visited[p[1]][s[1]]) continue;
                q.push({p[0] + s[0], p[1], s[1]});
            }
        }

        return -1;
    }
};
```
- [minimum height trees](https://leetcode.com/problems/minimum-height-trees/description/)
```cpp
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        if (n == 1) return {0};

        vector<vector<int>> g(n,vector<int>());
        for (auto &e : edges) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }

        vector<int> deg(n);
        for (int i = 0; i < n; i++) deg[i] = g[i].size();

		// bfs from outside (increasing of vertex's degree)
        queue<int> q;
        for (int i = 0; i < n; i++) if (deg[i] == 1) q.push(i);

        vector<int> ans(n); // vertices with highest degree?
        int k;
        while (!q.empty()) {
            int sz = q.size();
            k = 0;
            while (sz--) {
                int i = q.front(); q.pop();
                ans[k++] = i;
                for (int &j : g[i]) if (deg[j] && --deg[j] == 1) q.push(j);
            }
        }

        ans.resize(k);
        return ans;
    }
};
```
- [sum of distances in tree](https://leetcode.com/problems/sum-of-distances-in-tree/description/) -> 2-time dfs (with moving root)
```cpp
class Solution {
public:
	// count number of nodes in subtree root i
    int dfs1(vector<vector<int>> &g, vector<int> &dist, vector<int> &cnt, int i, int p = -1) {
        int c = 1;
        for (int &j : g[i]) {
            if (j == p) continue;
            int cj = dfs1(g, dist, cnt, j, i);
            dist[i] += dist[j] + cj;
            c += cj;
        }
        return cnt[i] = c;
    }

    void dfs2(vector<vector<int>> &g, vector<int> &dist, vector<int> &cnt, int n, int i, int p = -1) {
        for (int &j : g[i]) {
            if (j == p) continue;
            // moving root to j
            dist[j] += dist[i] - dist[j] - cnt[j] + n - cnt[j];
            dfs2(g, dist, cnt, n, j, i);
        }
    }

    vector<int> sumOfDistancesInTree(int n, vector<vector<int>>& edges) {
        vector<vector<int>> g(n,vector<int>());
        for (auto &e : edges) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }
        vector<int> dist(n,0), cnt(n,0); // dist[i] is total distances of (sub)tree root i
        dfs1(g, dist, cnt, 0);
        dfs2(g, dist, cnt, n, 0);

        return dist;
    }
};
```
- [distribute coins in binary tree](https://leetcode.com/problems/distribute-coins-in-binary-tree/)
```cpp
class Solution {
public:
    int distributeCoins(TreeNode* root, TreeNode *prev = nullptr) {
        if (!root) return 0;
        // number of move from node's children to root
        int ans = distributeCoins(root->left,root) + distributeCoins(root->right,root), v = root->val-1;
        if (prev) prev->val += v; // move v coins from root to prev (may be negative - move coins from prev to root)
        return ans + abs(v);
    }
};
```
- [all ancestors of a node in a DAG](https://leetcode.com/problems/all-ancestors-of-a-node-in-a-directed-acyclic-graph/)
```cpp
class Solution {
public:
    void dfs(vector<vector<int>> &g, int &i, int &i0, vector<vector<int>> &ans) {
        for (int &j : g[i]) {
            if (ans[j].empty() || ans[j].back() != i0) {
                ans[j].push_back(i0);
                dfs(g, j, i0, ans); // neednt go deeper if ans[j] is not change
            }
        }
    }

    vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
        vector<vector<int>> g(n,vector<int>());
        for (auto &e : edges) g[e[0]].push_back(e[1]);

        vector<vector<int>> ans(n,vector<int>());
        for (int i = 0; i < n; i++) dfs(g, i, i, ans);
        return ans;
    }
};

// backward - too slow
// class Solution {
// public:
//     void dfs(vector<vector<int>> &g, int i, vector<bool> &visited, vector<unordered_set<int>> &a) {
//         visited[i] = true;
//         for (int &j : g[i]) {
//             a[i].insert(j);
//             if (!visited[j]) dfs(g, j, visited, a);
//             for (int t : a[j]) a[i].insert(t);
//         }
//     }
// 
//     vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
//         vector<vector<int>> g(n,vector<int>());
//         for (auto &e : edges) g[e[1]].push_back(e[0]);
// 
//         vector<vector<int>> ans;
//         vector<unordered_set<int>> a(n,unordered_set<int>());
//         vector<bool> visited(n,false);
//         for (int i = 0; i < n; i++) {
//             if (!visited[i]) dfs(g, i, visited, a);
//             vector<int> q(a[i].begin(),a[i].end());
//             sort(q.begin(),q.end());
//             ans.push_back(move(q));
//         }
//         return ans;
//     }
// };
```
- [find minimum diameter after merging two trees](https://leetcode.com/problems/find-minimum-diameter-after-merging-two-trees/)
- [second minimum time to reach destination](https://leetcode.com/problems/second-minimum-time-to-reach-destination)
```cpp
using pii = pair<int,int>;

class Solution {
public:
		// modified dijkstra -> slow
    int secondMinimum(int n, vector<vector<int>>& edges, int time, int change) {
        vector<vector<int>> g(n+1,vector<int>());
        for (auto &e : edges) {
            g[e[0]].push_back(e[1]);
            g[e[1]].push_back(e[0]);
        }

        priority_queue<pii,vector<pii>,greater<pii>> q;
        q.push({0,1});
        vector<int> visited(n+1,0), last(n+1,-1);
        int t0 = -1;
        while (!q.empty()) {
            auto [t,i] = q.top(); q.pop();
            if (t == last[i] || visited[i] == 2) continue; // dont reach with same value or more than 2 times
            visited[i]++;
            last[i] = t;
            if (i == n) {
                if (t0 != -1 && t > t0) return t;
                t0 = t;
            }
            if ((t/change)&1) t = (t/change+1)*change;
            t += time;
            for (int &j : g[i]) if (visited[j] < 2 && last[j] != t) q.push({t,j});
        }
        return t0;
    }
};
```
- [regions cut by slashes](https://leetcode.com/problems/regions-cut-by-slashes/description/)
```cpp
class Solution {
public:
    void dfs(vector<vector<int>> &g, int n, int i, int j) {
        g[i][j] = 0;
        if (i > 0 && g[i-1][j]) dfs(g, n, i-1, j);
        if (j > 0 && g[i][j-1]) dfs(g, n, i, j-1);
        if (i < n-1 && g[i+1][j]) dfs(g, n, i+1, j);
        if (j < n-1 && g[i][j+1]) dfs(g, n, i, j+1);
    }

    int regionsBySlashes(vector<string>& grid) {
        int n = grid.size();
        // x3 grid
        vector<vector<int>> g(n*3,vector<int>(n*3,1));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < grid[i].size(); j++) {
                if (grid[i][j] ==  '/') {
                    g[3*i][3*j+2] = g[3*i+1][3*j+1] = g[3*i+2][3*j] = 0;
                } else if (grid[i][j] == '\\') {
                    g[3*i][3*j] = g[3*i+1][3*j+1] = g[3*i+2][3*j+2] = 0;
                }
            }
        }
        n *= 3;
        int ans = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (g[i][j]) {
                    ans++;
                    dfs(g, n, i, j);
                }
            }
        }
        return ans;
    }
};
```
- [map of highest peak](https://leetcode.com/problems/map-of-highest-peak)
```cpp
constexpr int dxy[4][2] = {{-1,0}, {0,1}, {1,0}, {0,-1}};
using pii = pair<int,int>;

class Solution {
public:
    vector<vector<int>> highestPeak(vector<vector<int>>& isWater) {
        int m = isWater.size(), n = isWater[0].size();
        vector<vector<int>> ans(m,vector<int>(n));
        queue<pii> q;
        for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) if (isWater[i][j]) q.push({i,j});
        int h = 0;
        while (!q.empty()) {
            int sz = q.size();
            while (sz--) {
                auto [x, y] = q.front(); q.pop();
                if (isWater[x][y] == -1) continue;
                isWater[x][y] = -1;
                ans[x][y] = h;
                for (int k = 0; k < 4; k++) {
                    int xx = x + dxy[k][0], yy = y + dxy[k][1];
                    if (xx < 0 || yy < 0 || xx == m || yy == n || isWater[xx][yy] == -1) continue;
                    q.push({xx,yy});
                }
            }
            h++;
        }
        return ans;
    }
};
```

- [flight routes](https://cses.fi/problemset/task/1196/) - k shortest paths with node revisits
	- codeforces' note to find k shortest paths [link](https://codeforces.com/blog/entry/102085)
```cpp

```

- [longest flight route](https://cses.fi/problemset/task/1680/) - longest path in DAG -> topo sort
```cpp
```
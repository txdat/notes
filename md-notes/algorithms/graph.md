# shortest path in a directed weighted graph
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
1. [find all people with secret](https://leetcode.com/problems/find-all-people-with-secret/description/)
```cpp
class Solution {
public:
    int find_parent(vector<int> &p, vector<bool> &check, int i) {
        int j = i;
        while (!check[i] && p[i] != -1) i = p[i];
        if (j != i) return p[j] = i;
        return i;
    }

    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        sort(meetings.begin(), meetings.end(), [](vector<int> &m1, vector<int> &m2) { return m1[2] < m2[2]; });
        vector<bool> check(n,false); // have secret or not
        check[0] = true;
        check[firstPerson] = true;

        vector<int> p(n,-1);
        int ns = meetings.size(), i = 0;
        while (i < ns) {
            int t = meetings[i][2], j = i;
            while (j < ns && meetings[j][2] == t) {
                auto &m = meetings[j];
                int p0 = find_parent(p, check, m[0]), p1 = find_parent(p, check, m[1]);
                if (p0 != p1) {
                    p[p1] = p0;
                }
                check[m[0]] = check[p0] = check[m[1]] = check[p1] = (check[m[0]] || check[p0] || check[m[1]] || check[p1]);

                j++;
            }
            for (int k = i; k < j; k++) {
                auto &m = meetings[k];
                int p0 = find_parent(p, check, m[0]), p1 = find_parent(p, check, m[1]);
                check[m[0]] = check[p0] = check[m[1]] = check[p1] = (check[m[0]] || check[p0] || check[m[1]] || check[p1]);
                // only need reset people that don't have secret
                if (!check[m[0]]) {
                    p[m[0]] = p[m[1]] = -1;
                }
            }
            i = j;
        }

        vector<int> ans;
        for (int i = 0; i < n; i++) if (check[i]) ans.push_back(i);
        return ans;
    }
};
```
2. [greatest common divisor traversal](https://leetcode.com/problems/greatest-common-divisor-traversal/description/)
```cpp
class Solution {
public:
    int find_parent(vector<int> &p, int i) {
        int j = i;
        while (p[i] != -1) i = p[i];
        return j == i ? i : p[j] = i;
    }

    int div(int &n, int i) {
        while (n % i == 0) n /= i;
        return n;
    }

    bool canTraverseAllPairs(vector<int>& nums) {
        int n = nums.size(), mx = sqrt(*max_element(nums.begin(), nums.end()));
        vector<int> q{2};
        vector<bool> check(mx+1,false);
        for (int i = 3; i <= mx; i++) {
            if (check[i]) continue;
            q.push_back(i);
            for (int j = (i<<1); j <= mx; j += i) check[j] = true;
        }

        unordered_map<int,vector<int>> m;
        for (int i = 0; i < n; i++) {
            for (int &j : q) {
                if (nums[i] > div(nums[i], j)) m[j].push_back(i);
                if (j >= nums[i]) break;
            }
            if (nums[i] > 1) m[nums[i]].push_back(i); // is prime
        }

        vector<int> p(n,-1);
        for (auto &r : m) {
            auto &v = r.second;
            int p0 = find_parent(p, v[0]);
            for (int i = 1; i < v.size(); i++) {
                int pi = find_parent(p, v[i]);
                if (pi != p0) p[pi] = p0;
            }
        }

        int c = 0;
        for (int &d : p) if (d == -1 && ++c > 1) return false;
        return true;
    }
};
```
- [minimum cost walk in weighted graph](https://leetcode.com/problems/minimum-cost-walk-in-weighted-graph/)
```cpp
class Solution {
public:
    int find_parent(vector<int> &p, int i) {
        int j = i;
        while (p[i] != -1) i = p[i];
        if (j != i) p[j] = i;
        return i;
    }
    
    vector<int> minimumCost(int n, vector<vector<int>>& edges, vector<vector<int>>& query) {
        vector<int> p(n,-1);
        vector<int> m(n,INT_MAX);
        for (auto &e : edges) {
            int p0 = find_parent(p, e[0]), p1 = find_parent(p, e[1]);
            if (p0 != p1) {
                p[p1] = p0;
                m[p0] &= m[p1];
            }
            m[p0] &= e[2];
        }
        
        vector<int> ans;
        for (auto &e : query) {
            if (e[0] == e[1]) {
                ans.push_back(0);
                continue;
            }
            int p0 = find_parent(p, e[0]), p1 = find_parent(p, e[1]);
            if (p0 != p1) {
                ans.push_back(-1);
            } else {
                ans.push_back(m[p0]);
            }
        }
        return ans;
    }
};
```
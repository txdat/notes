1. Knuth-Morris-Pratt - prefix function
	- [cp-algorithms](https://cp-algorithms.com/string/prefix-function.html)
		- call $\pi[i] = max\{k: s[0..k-1] == s[i-k+1..i]\}$ and $\pi[0]=0?$
```cpp
class Solution {
public:
    vector<int> kmp(string &s) {
        int n = s.length();
        vector<int> pi(n);
        for (int i = 1; i < n; i++) {
            int j = pi[i-1];
            // if s[i] != s[j],
            // set j' = pi[j-1], we have s[0..j'-1] == s[j-j'..j-1] (1)
            // from s[0..j-1] == s[i-j..i-1], we have s[j-j'..j-1] == s[i-j'..i-1] (2)
            // from (1) and (2), we have s[0..j'-1] == s[i-j'..i-1] and continue to compare s[j'] with s[i]
            while (j > 0 && s[i] != s[j]) j = pi[j-1];
            // if s[i] == s[j] and s[0..j-1] == s[i-j..i-1] (the longest prefix of s[0..i-1]), so s[0..j] is the longest prefix of s[0..i]
            if (s[i] == s[j]) j++;
            pi[i] = j;
        }
        return pi;
    }
};
```

- find all occurences of target in string
```cpp
class Solution {
public:
	// find all occurences of t in s
	vector<int> kmp(string &s, string &t) {
		string w = t + "#" + s;
		int m = w.length(), n = t.length();
		vector<int> pi(m);
		for (int i = 1; i < m; i++) {
			int j = pi[i-1];
			while (j > 0 && w[j] != w[i]) j = pi[j-1];
			if (w[j] == w[i]) j++;
			pi[i] = j;
		}
		vector<int> pos;
		for (int i = n + 1; i < m; i++) {
			if (pi[i] == n) pos.push_back(i-2*n);
		}
		return pos;
	}
}
```
- find all prefixes as suffix of string
```cpp
```

- [shortest palindrome](https://leetcode.com/problems/shortest-palindrome/description/)
```cpp
class Solution {
public:
    string shortestPalindrome(string s) {
        string t = s;
        reverse(t.begin(), t.end());
        t = s + "#" + t;
        int m = t.length(), n = s.length();
        vector<int> pi(m);
        for (int i = 1; i < m; i++) {
            int j = pi[i-1];
            while (j && t[j] != t[i]) j=pi[j-1];
            if (t[j] == t[i]) j++;
            pi[i] = j;
        }
        t = s.substr(pi[m-1]); // make s[0..pi[m-1]-1] is longest palindrome prefix
        reverse(t.begin(), t.end());
        return t + s;
    }
};
```
- [time needed to rearrange a binary string](https://leetcode.com/problems/time-needed-to-rearrange-a-binary-string/description/)
```cpp
class Solution {
public:
    int secondsToRemoveOccurrences(string s) {
        int i = 0, n = s.length()-1;
        while (i < s.length() && s[i] == '1') i++;
        while (n >=0 && s[n] == '0') n--;
        int cnt = 0, z = -1, lz = 0;
        for (; i <= n; i++) {
            if (s[i] == '1') {
                cnt++; // count number of '1' -> move '1' to leftward
                z--; // number of zeros before '1', counted by cnt -> can swap multiple '01' at the same time
            } else {
                lz = max(lz, ++z); // maximum leading zeros before '1'
            }
        }
        return cnt + lz;
    }
};
```
2. Manacher - find the largest palindrome for each position in string
- maintain (l,r) of rightmost found (sub)palindrome `[s[l+1]...s[r-1]]` is palindrome
- for next i
	- if i >= r, just launch trivia algorithm
	- if i < r, 
		- get `j=l+r-i` is mirror of i in (l,r), and can set `dp[i] = dp[j]`, but if `j-dp[j] <= l` (out of range), `dp[i] = r-i`
- add '#' between each element of input to solve parities
	- `dp[2i] = 2dp_even[i]+1`, `dp[2i+1] = 2dp_odd[i]`
```cpp
vector<int> manacher(string &s) {
    string t = "#";
    for (char &c : s) {
        t.push_back(c);
        t.push_back('#');
    }

    int n = t.length();
    t = "$" + t + "^";
    vector<int> dp(n + 2);
    int l = 1, r = 1;
    for (int i = 1; i <= n; i++) {
        dp[i] = max(0, min(r - i, dp[l + r - i]));
        while (t[i - dp[i]] == t[i + dp[i]]) dp[i]++;
        if (i + dp[i] > r) r = i + dp[i], l = i - dp[i];
    }

    return vector<int>(dp.begin() + 1, dp.end() - 1);
}

```
- [check if dfs strings are palindromes](https://leetcode.com/problems/check-if-dfs-strings-are-palindromes)
```cpp
class Solution {
public:
    int dfs(vector<vector<int>> &g, string &s, string &t, vector<pair<int,int>> &pos, int i = 0) {
      int l = INT_MAX;
      for (int &j : g[i]) l = min(l, dfs(g, s, t, pos, j));
      t.push_back(s[i]), t.push_back('#');
      if (g[i].empty()) l = t.length()-2;
      pos[i] = {l,t.length()-2};
      return l;
    }

    vector<int> manacher(string &s) {
      int n = s.length();
      string t = "$" + s + "^";
      vector<int> dp(n+2);
      int l = 1, r = 1;
      for (int i = 1; i <= n; i++) {
        dp[i] = max(0,min(r-i, dp[l+r-i]));
        while (t[i-dp[i]] == t[i+dp[i]]) dp[i]++;
        if (i+dp[i] > r) l = i-dp[i], r = i+dp[i];
      }
      return vector<int>(dp.begin()+1,dp.end()-1);
    }

    vector<bool> findAnswer(vector<int>& parent, string s) {
      int n = parent.size();
      vector<vector<int>> g(n,vector<int>());
      for (int i = 1; i < n; i++) g[parent[i]].push_back(i);
      vector<pair<int,int>> pos(n);//[l,r]
      string t = "#";
      dfs(g,s,t,pos);
      auto dp = manacher(t);
      vector<bool> ans;
      // cout << t << endl;
      // for (int &d : dp) cout << d << " ";
      // cout << endl;
      for (auto &[l,r] : pos) {
        // cout << l << " " << r << " " << t.substr(l,r-l+1) << endl;
        int m = (l+r)/2, h = dp[m];
        ans.push_back(h >= r-m+1);
      }
      return ans;
    }
};
```
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
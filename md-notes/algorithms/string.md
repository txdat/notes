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
	vector<int> kmp(string &s, string &t) {
		string w = t + "#" + s;
		int m = w.length(), n = t.length();
		vector<int> pi(m);
		for (int i = 1; i < m; i++) {
			int j = pi[i-1];
			while (j > 0 && w[j] != w[i]) j = pi[j-1];
			if (s[j] == s[i]) j++;
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
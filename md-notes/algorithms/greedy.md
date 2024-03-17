1. [minimum deletions to make string k-special](https://leetcode.com/problems/minimum-deletions-to-make-string-k-special/description/)
```cpp
class Solution {
public:
    int minimumDeletions(string word, int k) {
        int cnt[26] = {0};
        for (char &c : word) cnt[c-'a']++;

        int ans = word.length();
        for (int i = 0; i < 26; i++) { // try to set char i is character with smallest frequency -> neednt delete any character of i in word
            if (cnt[i] == 0) continue;
            int s = 0;
            for (int j = 0; j < 26; j++) {
                if (j == i) continue;
                if (cnt[j] < cnt[i]) { // remove all characters j because character i is smallest
                    s += cnt[j];
                } else if (cnt[j] > cnt[i] + k) {
                    s += cnt[j] - cnt[i] - k;
                }
            }
            ans = min(ans, s);
        }
        return ans;
    }
};
```
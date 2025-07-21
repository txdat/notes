1. get nearest palindrome numbers
```cpp
using ll = long long;

class Solution {
public:
    int get_lt_palindrome(int n) {
        vector<int> q;
        while (n) {
            q.push_back(n % 10);
            n /= 10;
        }
        int m = q.size();
        int j = m/2;
        while (q[j] == 0) {
            q[j++] = 9;
        }
        q[j]--;
        if (q[m - 1] == 0) {
            fill(q.begin(), q.end(), 9);
            m--;
        }
        for (int i = 0; i < m/2; i++) q[i] = q[m - 1 - i];
        for (int i = 0; i < m; i++) {
            n *= 10;
            n += q[i];
        }
        return n;
    }

    int get_gt_palindrome(int n) {
        vector<int> q;
        while (n) {
            q.push_back(n % 10);
            n /= 10;
        }
        int m = q.size();
        int j = m/2;
        while (j < m && q[j] == 9) {
            q[j++] = 0;
        }
        if (j == m) {
            q.push_back(1);
            m++;
        } else {
            q[j]++;
        }
        for (int i = 0; i < m/2; i++) q[i] = q[m - 1 - i];
        for (int i = 0; i < m; i++) {
            n *= 10;
            n += q[i];
        }
        return n;
    }

    int get_palindrome(int n) {
        vector<int> q;
        while (n) {
            q.push_back(n % 10);
            n /= 10;
        }
        int m = q.size();
        for (int i = 0; i < m/2; i++) q[i] = q[m - 1 - i];
        for (int i = 0; i < m; i++) {
            n *= 10;
            n += q[i];
        }
        return n;
    }

	// https://leetcode.com/problems/minimum-cost-to-make-array-equalindromic/
    long long minimumCost(vector<int>& nums) {
        sort(nums.begin(), nums.end());
        int n = nums.size();
        int m = (n&1) ? nums[n/2] : (nums[n/2-1] + nums[n/2])/2;
        ll ans = 1e14;
        for (int p : {get_palindrome(m), get_gt_palindrome(m), get_lt_palindrome(m)}) {
            ll s = 0;
            for (int &d : nums) s += abs(d - p);
            ans = min(ans, s);
        }
        return ans;
    }
};
```
2. [randomized set](https://leetcode.com/problems/insert-delete-getrandom-o1/description/)
```cpp
class RandomizedSet {
public:
    unordered_map<int,int> m;
    vector<int> q;
    int n = 0;

    //random_device rd;
    //mt19937 rng;
    //uniform_int_distribution<> dist;

    //RandomizedSet() : rng(rd()), dist(0, 200000) {
    //}
    RandomizedSet() {}
    
    bool insert(int val) {
        if (m.find(val) != m.end()) return false;
        if (n == q.size()) {
            q.push_back(val);
        } else {
            q[n] = val;
        }
        m[val] = n++;
        return true;
    }
    
    bool remove(int val) {
        if (m.find(val) == m.end()) return false;
        int i = m[val];
        swap(q[i], q[--n]); // swap deleted element to end of array
        m[q[i]] = i;
        m.erase(val);
        return true;
    }
    
    int getRandom() {
        //return q[dist(rng) % n];
		return q[rand()%n];
    }
};

/**
 * Your RandomizedSet object will be instantiated and called as such:
 * RandomizedSet* obj = new RandomizedSet();
 * bool param_1 = obj->insert(val);
 * bool param_2 = obj->remove(val);
 * int param_3 = obj->getRandom();
 */
```
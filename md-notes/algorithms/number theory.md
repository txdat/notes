1. [perfect square](https://leetcode.com/problems/perfect-squares/) - sum of squares
	- Lagrange's four-square theorem:
		-> every natural number can be represented as sum of 4 non negative integer squares
	- Legendre's three-square theorem:
		-> n is a natural number, $n=x^2+y^2+z^2$ is solvable iff n is not of following form $4^a(8b+7)$
```cpp
class Solution {
public:
	// bool is_square(int n) {
    //     int m = sqrt(n);
    //     return m*m == n;
    // }

    // int numSquares(int n) {
    //     if (is_square(n)) return 1;
    //     vector<int> dp(n+1,n);
    //     for (int i = 1; i <= n; i++) {
    //         if (is_square(i)) {
    //             dp[i] = 1;
    //         } else {
    //             for (int j = 1; j <= sqrt(i); j++) dp[i] = min(dp[i], dp[i-j*j] + 1);
    //         }
    //     }
    //     return dp[n];
    // }

	// number theory
    int numSquares(int n) {
        while (n%4 == 0) n>>=2; // if n is square, 4*n is square
        if (n%8 == 7) return 4; // lagrange's four-square

        int s = sqrt(n);
        if (s*s == n) return 1;

        for (int i = 1; i <= s; i++) {
            int m = n-i*i, si = sqrt(m);
            if (si*si == m) return 2;
        }

        return 3; // legendre's three-square
    }
};
```
2. check a number is prime, prime factorization (split number into prime factors)
```cpp
bool checkPrime(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n%2 == 0) return false;
    for (int i = 3; i <= sqrt(n); i += 2) if (n%i == 0) return false;
    return true;
}

// prime factorization
bool factorizeDiv(int &n, int i) {
	int t = n;
	while (n%i == 0) n/=i;
	return n < t;
}

vector<int> factorizeNum(int n) {
	vector<int> f;
	if (factorizeDiv(n,2)) f.push_back(2);
	for (int i = 3; i <= sqrt(n); i += 2) if (factorizeDiv(n,i)) f.push_back(i);
	if (n > 1) f.push_back(n); // n is prime number
	return f;
}
```
3. find smallest/largest of positive modulo (> 0) between 2 elements in array - [D. Turtle Tenacity: Continual Mods](https://codeforces.com/contest/1933/problem/D)
```cpp
bool continualMods(vector<int> &a) {
	sort(a.begin(),a.end());
    if (a[1] > a[0]) {
        // cout << "yes\n";
        return true;
    }
    for (int i = 0; i < n; i++) {
        int t = a[i];
        while (t < a[n-1]) {
            auto it = upper_bound(all(a), t);
            if (it == a.end()) {
                // cout << "no\n";
                return false;
            }
            int r = *it%a[i];
            if (r && r < a[0]) {
                // cout << "yes\n";
                return true;
            }
            t = *it - r + a[i];
        }
    }
    //cout << "no\n";
    return false;
}
```
- [count array pairs divisible by k](https://leetcode.com/problems/count-array-pairs-divisible-by-k/description/)
**important property
- if $$(a*b)\%k=0 \leftrightarrow (gcd(a,k)*gcd(b,k))\%k=0$$
```cpp
using ll = long long;

class Solution {
public:
	long long countPairs(vector<int> &nums, int k) {
		unordered_map<int,ll> m;
		for (int &d : nums) m[gcd(d,k)]++;
		ll ans = 0;
		for (auto &[a, ca] : m) {
			for (auto &[b, cb] : m) {
				if ((ll(a)*b)%k == 0) ans += ca*cb - (a == b ? ca : 0);
			}
		}
		return ans/2;
	}
};
```
- [maximum and minimum sums of at most size k subsequences](https://leetcode.com/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/description/)
```cpp

```
- [find the maximum sum of node values](https://leetcode.com/problems/find-the-maximum-sum-of-node-values)
```cpp
using ll = long long;

class Solution {
public:
    long long maximumValueSum(vector<int>& nums, int k, vector<vector<int>>& edges) {
	  // we can change any pair of nodes in tree
      // cnt is number of nodes such that it value becomes greater if we change, if cnt is odd, m is smallest decrement value
      ll ans = 0;
      int cnt = 0, m = INT_MAX;
      for (int &d : nums) {
        int t = d^k;
        ans += max(d, t);
        cnt += t>d;
        m = min(m, abs(d-t));
      }
      return ans - ((cnt&1) ? m : 0);
    }
};
```
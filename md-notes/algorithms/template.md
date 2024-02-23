1. codeforces
```cpp
/*{{{*/
//#pragma GCC optimize("Ofast,unroll-loops")
//#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")

#include <bits/stdc++.h>
using namespace std;

#define all(x) x.begin(), x.end()

using ll = long long;
using pii = pair<int,int>;
using mii = unordered_map<int,int>;
using mli = unordered_map<long long,int>;

constexpr int MOD = 1e9 + 7;

// print pair of A,B
template <typename A, typename B>
ostream &operator<<(ostream &os, const pair<A, B> &p) {
    return os << '(' << p.first << ", " << p.second << ')';
}
// print array/vector of T
template <typename T_container, typename T = typename enable_if<
                                    !is_same<T_container, string>::value,
                                    typename T_container::value_type>::type>
ostream &operator<<(ostream &os, const T_container &v) {
    os << '{';
    string sep;
    for (const T &x : v) os << sep << x, sep = ", ";
    return os << '}';
}

// read array/vector of T
template <typename T_container, typename T = typename enable_if<
                                    !is_same<T_container, string>::value,
                                    typename T_container::value_type>::type>
istream &operator>>(istream &is, T_container &v) {
    for (T &x : v) is >> x;
    return is;
}

void dbg_out() { cerr << "\n"; }
template <typename T, typename... U>
void dbg_out(T t, U... u) {
    cerr << ' ' << t;
    dbg_out(u...);
}
#define dbg(...)                                              \
    cerr << 'L' << __LINE__ << "\t(" << #__VA_ARGS__ << "):", \
        dbg_out(__VA_ARGS__)
/*}}}*/

//#define INP ""
//#define OUT ""
#define MULTIPLE_TEST_CASES

void __solve(int __test_case = 1) {
}

/*{{{*/
int main(int argc, const char **argv) {
    cin.tie(0)->sync_with_stdio(0);
#ifdef INP
    freopen(INP, "r", stdin);
#endif
#ifdef OUT
    freopen(OUT, "w", stdout);
#endif

#ifdef MULTIPLE_TEST_CASES
    int n;
    cin >> n;
    for (int t = 1; t <= n; t++) {
        __solve(t);
    }
#else
    __solve();
#endif

    return 0;
} /*}}}*/

```
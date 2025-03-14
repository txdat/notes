- [maximum number of consecutive values from array](https://leetcode.com/problems/maximum-number-of-consecutive-values-you-can-make/description/)
	- follow up: [minimum number of coins to be added to reach target value](https://leetcode.com/problems/minimum-number-of-coins-to-be-added/)
	- suppose we have made consecutive values `[1...mx)`, if next value from array `d > mx`, so we have to add new value `mx` to array, and we have new consecutive values `[1..mx')`, `nx' = mx*2`
```cpp
class Solution {
	public:
	    int minimumAddedCoins(vector<int>& coins, int target) {
	        sort(coins.begin(), coins.end());
	        int n = coins.size();
	        int ans = 0, mx = 1;
	        for (int &d : coins) {
	            if (mx > target) break;
	            while (mx < d) {
	                ans++; // or return maximum value can reach
	                mx <<= 1;
	            }
	            mx += d;
	        }
	        while (mx <= target) {
	            ans++;
	            mx <<= 1;
	        }
	        return ans;
	    }
	};
```

- [sliding window maximum](https://leetcode.com/problems/sliding-window-maximum/description/)
```cpp
// using deque
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        deque<int> q;
        for (int i = 0; i < k - 1; i++) {
            while (!q.empty() && nums[q.back()] <= nums[i]) q.pop_back();
            q.push_back(i);
        }
        vector<int> ans;
        for (int i = k - 1; i < n; i++) {
            while (!q.empty() && nums[q.back()] <= nums[i]) q.pop_back();
            q.push_back(i);
            while (!q.empty() && i - q.front() >= k) q.pop_front();
            ans.push_back(nums[q.front()]);
        }
        return ans;
    }
};
```
- [sliding window median](https://leetcode.com/problems/sliding-window-median/)
```cpp
```
- [longest increasing subsequence](https://leetcode.com/problems/longest-increasing-subsequence)
```cpp
class Solution {
public:
	vector<int> lengthOfLIS(vector<int> &nums) {
		// N^2
		//int n = nums.size();
		//vector<int> dp(n, 1);
		//for (int i = 0; i < n; i++) {
		//	for (int j = i + 1; j < n; j++) dp[j] = max(dp[j], dp[i] + 1);
		//}
		//return *max_element(dp.begin(), dp.end());
		
		// Nlog(N)
		int n = nums.size();
		int ans = 1;
		vector<int> dp(n + 1, INT_MAX);
		dp[0] = INT_MIN;
		for (int &d : nums) {
			int i = upper_bound(dp.begin(), dp.end(), d) - dp.begin();
			// if subsequence must be strictly increasing, we need condition dp[i-1]=d, if not, we can omit this condition
			if (dp[i - 1] < d) dp[i] = d;
			ans = max(ans, i);
		}
		return ans;
	}
}
```
- [find the median in average O(n)](https://rcoh.me/posts/linear-time-median-finding/)
```cpp

```
- [longest non-decreasing subarray from 2 arrays](https://leetcode.com/problems/longest-non-decreasing-subarray-from-two-arrays/description/)
```cpp
class Solution {
public:
    int maxNonDecreasingLength(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size(), ans = 1;
        vector<vector<int>> dp(2,vector<int>(n)); // dp[*][i] is length of longest non-decreasing subarray ended by nums1[i] or nums2[i]
        dp[0][0] = dp[1][0] = 1;
        for (int i = 1; i < n; i++) {
            int t = 1;
            if (nums1[i] >= nums1[i-1]) {
                t = max(t, 1 + dp[0][i-1]);
            }
            if (nums1[i] >= nums2[i-1]) {
                t = max(t, 1 + dp[1][i-1]);
            }
            dp[0][i] = t;
            ans = max(ans, t);
            t = 1;
            if (nums2[i] >= nums1[i-1]) {
                t = max(t, 1 + dp[0][i-1]);
            }
            if (nums2[i] >= nums2[i-1]) {
                t = max(t, 1 + dp[1][i-1]);
            }
            dp[1][i] = t;
            ans = max(ans, t);
        }
        return ans;
    }
};
```
- [maximize consecutive elements in an array after modification](https://leetcode.com/problems/maximize-consecutive-elements-in-an-array-after-modification/) - similar to problem "longest non-decreasing subarray ..." above
```cpp
class Solution {
public:
	// better solution
	int better_maxSelectedElements(vector<int>& nums1) {
		int n = nums.size();
        sort(nums.begin(), nums.end());
        unordered_map<int,int> m;
        for (int &d : nums) {
            m[d+1] = m[d] + 1;
            m[d] = m[d-1] + 1;
        }
        int ans = 0;
        for (auto &p : m) ans = max(ans, p.second);
        return ans;
	}

    int maxSelectedElements(vector<int>& nums1) {
        int n = nums1.size();
        sort(nums1.begin(), nums1.end());
        vector<int> nums2(nums1);
        for (int &d : nums2) d++;
        
        vector<vector<int>> dp(2,vector<int>(n));
        dp[0][0] = dp[1][0] = 1;
        int ans = 1;
        for (int i = 1; i < n; i++) {
            int t = 1;
            if (nums1[i] == nums1[i-1] + 1) {
                t = max(t, 1 + dp[0][i-1]);
            } else if (nums1[i] == nums1[i-1]) {
                t = max(t, dp[0][i-1]);
            }
            if (nums1[i] == nums2[i-1] + 1) {
                t = max(t, 1 + dp[1][i-1]);
            } else if (nums1[i] == nums2[i-1]) {
                t = max(t, dp[1][i-1]);
            }
            dp[0][i] = t;
            ans = max(ans, t);
            t = 1;
            if (nums2[i] == nums1[i-1] + 1) {
                t = max(t, 1 + dp[0][i-1]);
            } else if (nums2[i] == nums1[i-1]) {
                t = max(t, dp[0][i-1]);
            }
            if (nums2[i] == nums2[i-1] + 1) {
                t = max(t, 1 + dp[1][i-1]);
            } else if (nums2[i] == nums2[i-1]) {
                t = max(t, dp[1][i-1]);
            }
            dp[1][i] = t;
            ans = max(ans, t);
        }
        return ans;
    }
};
```
- [count of smaller numbers after self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/description/)
```cpp
// using merge-sort can count number of smaller numbers
class Solution {
public:
    void merge_sort(vector<pair<int,int>> &q, int l, int r, vector<int> &cnt) {
        if (l >= r) return ;
        
        int m = (l+r)>>1;
        merge_sort(q, l, m, cnt);
        merge_sort(q, m+1, r, cnt);

        vector<pair<int,int>> t;
        int i = l, j = m+1;
        // sort desc
        while (i <= m && j <= r) {
            if (q[i].first > q[j].first) {
                cnt[q[i].second] += r-j+1; // q[i] is larger than all q[j..r]
                t.push_back(q[i++]);
            } else {
                t.push_back(q[j++]);
            }
        }
        while (i <= m) t.push_back(q[i++]);
        while (j <= r) t.push_back(q[j++]);

        move(t.begin(), t.end(), q.begin()+l);
    }

    vector<int> countSmaller(vector<int>& nums) {
        int n = nums.size();
        vector<pair<int,int>> q;
        for (int i = 0; i < n; i++) q.push_back({nums[i], i});
        vector<int> ans(n,0);
        merge_sort(q, 0, n-1, ans);
        return ans;
    }
};
```
- count frequencies of all elements - O(n) time complexity, O(1) space complexity
	- count frequencies of n-length array elements, whose elements are between 1-n -> use element as an index and store their count at the index (negative number)
	- [solution](https://www.geeksforgeeks.org/count-frequencies-elements-array-o1-extra-space-time/)
```cpp
unordered_map<int,int> count1(vector<int> &a) { // use a[a[i]] to store counts of a[i]
	int n = a.size();
	a.push_back(0); // for value n

	for (int i = 0; i < n; i++) {
		if (a[i] <= 0) continue;
		if (a[i] > i && a[a[i]] > 0) {
			// keep larger and not visited element
			int t = a[i];
			a[i] = a[t];
			a[t] = -1;
			i--; // keep current i
		} else {
			a[a[i]] = min(-1, a[a[i]]-1); // -1 for visited element before
		}
	}

	unordered_map<int,int> m;
	for (int i = 1; i <= n; i++) {
		if (a[i] < 0) m[i] = -a[i]; // count of i is stored as negative
	}
	return m;
}

unordered_map<int,int> count2(vector<int> &a) { // use a[a]
}
```

- [find all duplicates in an array](https://leetcode.com/problems/find-all-duplicates-in-an-array)
```cpp
class Solution {
public:
    vector<int> findDuplicates(vector<int>& nums) {
        int n = nums.size();
        nums.push_back(0);

        for (int i = 0; i < n; i++) {
            if (nums[i] <= 0) continue;
            if (nums[i] > i && nums[nums[i]] > 0) {
                int t = nums[i];
                nums[i] = nums[t];
                nums[t] = -1;
                i--;
            } else {
                nums[nums[i]] = min(-1, nums[nums[i]]-1);
            }
        }

        vector<int> ans;
        for (int i = 1; i <= n; i++) if (nums[i] == -2) ans.push_back(i);
        return ans;
    }
};
```
- [find first missing positive](https://leetcode.com/problems/first-missing-positive/description/)
```cpp
// find all numbers disappeared in array - leetcode 448
class Solution_LC448 {
public:
    vector<int> findDisappearedNumbers(vector<int>& nums) {
        int n = nums.size();
        nums.push_back(0);
        for (int i = 0; i < n; i++) {
            // use nums[i] to store i if i is met
            while (nums[i] != nums[nums[i]]) swap(nums[i],nums[nums[i]]);
        }
        vector<int> ans;
        for (int i = 1; i <= n; i++) if (nums[i] != i) ans.push_back(i);
        return ans;
    }
};

// O(n) time complexity - O(1) space complexity
class Solution {
public:
    int firstMissingPositive(vector<int>& nums) {
        int n = nums.size();
        nums.push_back(0);
        for (int i = 0; i < n; i++) {
	        // ignore non-positive or larger than n integers (missing positive in [1..n+1])
	        // use nums[i] to store i if i is met
            while (nums[i] > 0 && nums[i] <= n && nums[nums[i]] != nums[i]) swap(nums[i], nums[nums[i]]);
        }
        for (int i = 1; i <= n; i++) if (nums[i] != i) return i;
        return n+1;
    }
};
```
- [minimize manhattan distance](https://leetcode.com/problems/minimize-manhattan-distances/)
	- [compute maximum manhattan distance between 2 points from n points](https://www.geeksforgeeks.org/maximum-manhattan-distance-between-a-distinct-pair-from-n-coordinates/)
```cpp
int get_max_distance(vector<vector<int>> &points) {
	int n = points.size();
	int min_s, max_s, min_d, max_d;
	min_s = max_s = points[0][0] + points[0][1];
	min_d = max_d = points[0][0] - points[0][1];
	for (int i = 1; i < n; i++) {
		int s = points[i][0] + points[i][1], d = points[i][0] - points[i][1];
		if (s < min_s) {
			min_s = s;
		} else if (s > max_s) {
			max_s = s;
		}
		if (d < min_d) {
			min_d = d;
		} else if (d > max_d) {
			max_d = d;
		}
	}
	return max(max_s-min_s,max_d-min_d);
}
```
```cpp
class Solution {
public:
	// get max manhattan distance with index of 2 points having maximum distance
    vector<int> get_max_distance(vector<vector<int>> &points, int ignore=-1) {
        int n = points.size();
        int i0 = ignore == 0;
        int min_s, max_s, min_d, max_d;
        min_s = max_s = points[i0][0] + points[i0][1];
        min_d = max_d = points[i0][0] - points[i0][1];
        int min_si = i0, max_si = i0, min_di = i0, max_di = i0;
        for (int i = i0+1; i < n; i++) {
            if (i == ignore) continue;
            int s = points[i][0] + points[i][1], d = points[i][0] - points[i][1];
            if (s < min_s) {
                min_s = s;
                min_si = i;
            } else if (s > max_s) {
                max_s = s;
                max_si = i;
            }
            if (d < min_d) {
                min_d = d;
                min_di = i;
            } else if (d > max_d) {
                max_d = d;
                max_di = i;
            }
        }
        int ds = max_s - min_s, dd = max_d - min_d;
        if (ds > dd) {
            return {ds, min_si, max_si};
        }
        return {dd, min_di, max_di};
    }
    
    int minimumDistance(vector<vector<int>>& points) {
        auto v = get_max(points);
        // ignore 2 points that create maximum manhattan distance
        auto v1 = get_max(points,v[1]);
        auto v2 = get_max(points,v[2]);
        return min(v[0],min(v1[0],v2[0]));
    }
};
```
- [longest consecutive sequence - O(n)](https://leetcode.com/problems/longest-consecutive-sequence/description/)
```cpp
// using union-find
class Solution {
public:
    int find_parent(unordered_map<int,int> &p, int i) {
        int j = i;
        while (p[i] != INT_MIN) i = p[i];
        if (j != i) p[j] = i;
        return i;
    }

    int longestConsecutive(vector<int>& nums) {
        int n = nums.size();
        int ans = 0;
        unordered_map<int,int> p, m;
        for (int &d : nums) {
            if (p.find(d) != p.end()) continue;
            p[d] = INT_MIN;
            m[d] = 1;
            if (p.find(d+1) != p.end()) {
                int t = find_parent(p,d+1);
                p[t] = d;
                m[d] += m[t];
            }
            ans = max(ans, m[d]);
            if (p.find(d-1) != p.end()) {
                int t = find_parent(p,d-1);
                p[d] = t;
                ans = max(ans, m[t] += m[d]);
            }
        }
        return ans;
    }
};
```
- [minimum number of flips to make binary grid palindromic ii](https://leetcode.com/problems/minimum-number-of-flips-to-make-binary-grid-palindromic-ii/description/) -> greedy
```cpp
class Solution {
public:
    int minFlips(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size(), m1 = m/2, n1 = n/2;
        int ans = 0;
        for (int i = 0; i < m1; i++) {
            for (int j = 0; j < n1; j++) {
                int i1 = m-1-i, j1 = n-1-j;
                int s = grid[i][j] + grid[i][j1] + grid[i1][j] + grid[i1][j1];
                ans += min(s, 4-s);
            }
        }

        if ((m&1) && (n&1) && grid[m1][n1]) ans++;

        int c = 0, t = 0;
        if (m&1) {
            for (int j = 0; j < n1; j++) {
                if (grid[m1][j] != grid[m1][n-1-j]) {
                    ans++;
                    t++;
                } else if (grid[m1][j]) {
                    c += 2;
                }
            }
        }
        
        if (n&1) {
            for (int i = 0; i < m1; i++) {
                if (grid[i][n1] != grid[m-1-i][n1]) {
                    ans++;
                    t++;
                } else if (grid[i][n1]) {
                    c += 2;
                }
            }
        }

        return t ? ans : ans + c%4;
    }
};
```
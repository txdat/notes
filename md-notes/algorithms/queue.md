1. deque (double-ended queue) -> combine queue and monotonic stack
- [sliding window maximum](https://leetcode.com/problems/sliding-window-maximum/)
```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        deque<int> q;
        for (int i = 0; i < k-1; i++) {
            while (!q.empty() && nums[q.back()] <= nums[i]) q.pop_back();
            q.push_back(i);
        }
        vector<int> ans;
        for (int i = k-1, j = 0; i < n; i++, j++) {
            while (!q.empty() && q.front() < j) q.pop_front();
            while (!q.empty() && nums[q.back()] <= nums[i]) q.pop_back();
            q.push_back(i);
            ans.push_back(nums[q.front()]);
        }
        return ans;
    }
};
```
- [longest continuous subarray with absolute diff less than or equal limit](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/description/)
```cpp
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        int n = nums.size();
        deque<int> minq, maxq;
        int j = 0;
        for (int i = 0; i < n; i++) {
            while (!minq.empty() && nums[minq.back()] > nums[i]) minq.pop_back();
            minq.push_back(i);
            while (!maxq.empty() && nums[maxq.back()] < nums[i]) maxq.pop_back();
            maxq.push_back(i);
            if (nums[maxq.front()] - nums[minq.front()] > limit) {
		        // if k<j and k is not front of maxq (or minq), k is popped before
                if (maxq.front() == j) maxq.pop_front();
                if (minq.front() == j) minq.pop_front();
                j++;
            }
        }
        return n-j;
    }
	int longestSubarray2(vector<int>& nums, int limit) {
		int n = nums.size();
        deque<int> minq, maxq;
        int ans = 0;
        for (int i = 0, j = 0; j < n;) {
            while (!minq.empty() && minq.front() < i) minq.pop_front();
            while (!maxq.empty() && maxq.front() < i) maxq.pop_front();
            while (!minq.empty() && nums[minq.back()] > nums[j]) minq.pop_back();
            minq.push_back(j);
            while (!maxq.empty() && nums[maxq.back()] < nums[j]) maxq.pop_back();
            maxq.push_back(j);
            if (nums[maxq.front()]-nums[minq.front()] > limit) {
                i++;
                continue;
            }
            ans = max(ans, j-i+1);
            j++;
        }
        return ans;
	}
};
```
- [constrained subsequence sum](https://leetcode.com/problems/constrained-subsequence-sum/)
```cpp
class Solution {
public:
    int constrainedSubsetSum(vector<int>& nums, int k) {
        int n = nums.size();
        deque<int> q;
        for (int i = 0; i < n; i++) {
            if (!q.empty()) nums[i] += nums[q.front()]; // i - q.front() <= k

            while (!q.empty() && i - q.front() >= k) q.pop_front();
            while (!q.empty() && nums[q.back()] <= nums[i]) q.pop_back();
            if (nums[i] > 0) q.push_back(i);
        }

        return *max_element(nums.begin(), nums.end());
    }
};
```
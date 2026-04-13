- [lru cache](https://leetcode.com/problems/lru-cache/description/)
```cpp
class LRUCache {
public:
    int n;
    list<pair<int,int>> q;
    unordered_map<int,list<pair<int,int>>::iterator> m;

    LRUCache(int capacity) : n(capacity) {
    }
    
    int get(int key) {
        if (m.find(key) == m.end()) return -1;
        int value = m[key]->second;
        q.erase(m[key]);
        q.push_front({key, value});
        m[key] = q.begin();
        return value;
    }
    
    void put(int key, int value) {
        if (m.find(key) != m.end()) {
            q.erase(m[key]);
        } else if (m.size() == n) {
            m.erase(q.back().first);
            q.pop_back();
        }
        q.push_front({key, value});
        m[key] = q.begin();
    }
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```

- [lfu cache](https://leetcode.com/problems/lfu-cache/description/)
```cpp
class LFUCache {
public:
    int capacity, n = 0, low = 0;
    vector<list<pair<int,int>>> q{list<pair<int,int>>()};
    unordered_map<int,pair<int,list<pair<int,int>>::iterator>> m;

    LFUCache(int capacity): capacity(capacity) {
    }
    
    int get(int key) {
        if (m.find(key) == m.end()) return -1;
        auto [k, it] = m[key];
        int value = it->second;
        q[k].erase(it);
        if (k == low && q[k].empty()) low++;
        k++;
        if (q.size() == k) q.push_back(list<pair<int,int>>());
        q[k].push_front({key, value});
        m[key] = {k, q[k].begin()};
        return value;
    }
    
    void put(int key, int value) {
        if (m.find(key) != m.end()) {
            auto [k, it] = m[key];
            q[k].erase(it);
            if (k == low && q[k].empty()) low++;
            k++;
            if (q.size() == k) q.push_back(list<pair<int,int>>());
            q[k].push_front({key,value});
            m[key] = {k, q[k].begin()};
            return;
        }
        if (n == capacity) {
            auto k = q[low].back().first;
            q[low].pop_back();
            m.erase(k);
            n--;
        }
        low = 0;
        q[low].push_front({key, value});
        m[key] = {low, q[low].begin()};
        n++;
    }
};

/**
 * Your LFUCache object will be instantiated and called as such:
 * LFUCache* obj = new LFUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```
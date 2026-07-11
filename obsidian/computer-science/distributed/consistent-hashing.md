# Consistent Hashing

[[consistent hashing.excalidraw]]

[highscalability blog](https://highscalability.com/consistent-hashing-algorithm/)
[systemdesign.one blog](https://systemdesign.one/consistent-hashing-explained/)

# Hash Ring

# Virtual Nodes
- adding 1 node to 5-node ring remaps ~17% of keys
- virtual nodes reduce load imbalance to <5%

# Implementation
- ring.AddNode(id, tokens)
- ring.GetNode(key)

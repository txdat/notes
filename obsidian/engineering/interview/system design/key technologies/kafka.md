
- [kafka deep dive](https://www.redpanda.com/guides/kafka-architecture)
# motivation
- events are placed on queue with producers and consumers
- messages are sent and received through kafka require a user specified distribution strategy -> keep causal ordering (all associated events must be placed on same queue)
- each event is associated with a topic and consumers can subscribe to specific topics
![[Pasted image 20251007015429.png | 800]]

# kafka architecture
### basic terminology
- broker
- partition
- topic
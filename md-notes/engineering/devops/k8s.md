- [kubenetes architecture - devopcube](https://devopscube.com/kubernetes-architecture-explained/)
- ![[Pasted image 20240209210714.png | 800]]
1. the need of system like k8s
	- moving from monolithic app to microservices -> scaling based on service basis
	- providing consistent environment to applications
2. container
	- isolating components of each microservice -> run multiple services on same host machine
	- includes: namespace (isolate container with others) and cgroup (limit cpu/memory resources)
	- compared to VMs (require theirs system processes), container is just isolated process (less resources)
	- 3 main concepts:
		- image: packages application and its environment, includes multiple layers to distribute more efficient and reduce storage
			- each invidual command is a new layer
				- ![[Pasted image 20231228203918.png | 600]]
		- registry: stores docker images (eg. dockerhub, ECR, ...)
		- container: created from docker images, is isolated process on host machine
![[Pasted image 20231228202624.png | 800]]
- debug crashed containers by ephemeral debug container
```bash
kubectl debug <target-container-name> --image=<debug-container-image> --target=<target-pod-name>
```
3. architecture of k8s
![[Pasted image 20231228203156.png | 800]]
	 - cluster may be public (all k8s's vm have external IPs) or private (only internal IPs, only accessible inside subnet)
	 includes:
		- control plane
			- api server:
				- central hub of k8s cluster, expose kubernetes api for users and third-party services (using http rest for users and grpc)
				- connection point for k8s components and users
				- ![[Pasted image 20240209211121.png | 600]]
			- scheduler: 
				- determine where workloads should run (optimal node) by filtering-scoring operations (2-phase)
				- schedule pods based on their priority (high to low)
				- ![[Pasted image 20240209211648.png | 600]]
			- controller manager: 
				- run infinite control loops for: perform creating/replicating pods, keeping track of worker nodes, handling node failures, ...
				- watch actual and desired state of cluster
			- etcd: 
				- strongly consistent distributed data store for storing cluster's state/configuration
				- stores configurations under `/registry` directory
				- only can communicate through api server
			- cloud controller manager (CCM) for cloud platform deployment
				- provision vm instances, load balancers, storages, ...
		- worker nodes
			- container runtime: docker, containerd, ...
				- run on all nodes of cluster
				- pull images, run containers (with allocating/isolating resources)
				- contains:
					- Container runtime interface (CRI): set of apis for different runtimes
					- open container initiative (OCI)
			- kubelet: 
				- manage pods (from podSpec) on its node by connection with api server and container runtime (like create/modify/delete pods, handle liveness/readiness probe, mount volumes, ...)
				- run as daemon process (managed by `systemd)
				- manage static pods directly (not from api-server): api-server, scheduler, and controller manager are static pods during control plane boostraping
					- static pod spec are stored under directory `/ect/kubernetes/manifests`
				- ![[Pasted image 20240209212825.png | 600]]
			- kube-proxy: 
				- k8s' service is a way to expose pods, create an endpoint object that contains all ip addresses of pods under service
				- is daemonset deployment (not daemon process like kubelet), implements k8s services concept (single dns for a set of pods with load balancing)
				- proxies TCP, UDP, SCTP, and **not understand HTTP**
				- network traffic routing to backend pods (using iptables)
				- ![[Pasted image 20240209220243.png | 600]]
![[Pasted image 20231228203731.png | 800]]
	- k8s interfaces:
		- extend and customize k8s' core functions
		- some interfaces:
			- container networking interface (CNI)
				- assign CIDR (ip addresses range) for each node, and configure pod network
				- enable networking between pods across the same or different nodes using overlay network
				- ![[Pasted image 20240209220742.png | 600]]
			- container storage interface
			- container runtime interface: for create, delete, ... containers, pull container images, ...
4. pod and deployment
	1. Pod
		- co-located group of containers - basic building block of k8s (all pod's containers run on same node) -> group of cohesive containers
		- all pod's containers share same ip address and port space
		- all pods can access other pods by their ip address (flat inter-pod network)
		- pods are managed by labels
		- why running pod instead of container?
			- use multi processes (each process per container). if running multiple processes on same container, have to keep all processes running, manage their logs, ... (pdf)
			-
		- k8s checks if pod is alive by `liveness probe` (send HTTP request, TCP socket, execute command, ...) -> restart unhealthy pods automatically
		- k8s checks if pod is able to receive user's request or not (not restart pods)
		- ![[Pasted image 20231228214750.png | 600]]
		- ![[Pasted image 20240226160524.png | 600]]
		- **Static pod**
			- managed directly by kubelet on a specific node, without the api server (from control plane like deployment) observing them (always bound to one kubelet)
			- kubelet creates a mirror pod on api server for each static pod, all pods are visible from api server (but cannot control static pods from here)
	- Replication Controller / Replica Set (RC with improved selector) / Daemon Set / Stateful Set -> Deployment
		- k8s resources keep pods running and replace unhealthy pods
			- 3 main components:
				- label selector: determine pods in scope (if pod's label is modified, it can be removed from RC's scope)
				- replica count: desired number of pods
				- pod template: container's configuration for new pod deployment
		- ![[Pasted image 20231228210944.png | 600]]
	- Modify single pod's template
		![[Pasted image 20231228211524.png | 800]]
	- Update deployment's template and replace all pods with new ones
		- Rolling update (create and replace in same time)
		- ![[Pasted image 20231228213113.png | 800]]
		- ![[Pasted image 20231228214335.png | 800]]
		- Blue-green update: create new pods and change service's pod selector
		- ![[Pasted image 20231228212551.png | 800]]
	- DaemonSet (run exactly one pod on each node)
		![[Pasted image 20231228211829.png | 600]]
	- Graceful termination
		![[Pasted image 20231228220015.png | 600]]
	- stateful application
		- stateful pods are initialized sequentially, based on their indices
		- scaling statefulset relates to increase/decrease number of replicas
5. service
	- pods are ephemeral, pods' ip addresses are assigned after pods have been scheduled to nodes, and many pods may provide same service
	- service is k8s resource to make single, constant entry to a group of pods providing same service (using pods selector)
	- can use session affinity to force service's requests to certain pod
	- 3 service types:
		- node port
			- cluster node opens port (30000-32767) on node itself, and redirect traffic from this port to underlying service
				![[Pasted image 20231228221958.png | 600]]
		- load balancer
			- same as node port, and make service accessible from load balancer (provisioned by k8s cloud infrastructure like GCP, AWS, ...)
			- each load balancer service requires a load balancer and its external ip address
				![[Pasted image 20231228222039.png | 600]]
		- cluster ip
			- only accessible inside cluster (require internal ip address)
			- use ingress or gateway for external access
		- headless service
			- not create ip address for service, but dns for each pod
6. gateway and ingress
	- are implementation for routing rules
	- expose multiple services using single load balancer and external ip address (to access cluster's service from outside)
	- support TLS termination (client -> LB: HTTPs, LB -> services: HTTP)
	- use rules (url, header, ... matching) for routing traffic
	- ingress
		- http host, path matching
		- TLS
		- many load balancer implementations
		- requires ingress controllers inside cluster
	    ![[Pasted image 20231229024400.png | 800]]
	- gateway
		- all ingress' features
		- http header matching and manipulation
		- rate limiting
		- weighted traffic splitting
		![[Pasted image 20231229103619.png | 800]]
	- ingress vs gateway
		![[Pasted image 20231229025302.png | 800]]
7. auto scaling for pods and cluster nodes
	- node autoscaling:
		- increase/decrease number of nodes in node pool (create new node pool if neccessary)
	- pod autoscaling:
		- need to set CPU/memory's requests and metrics
		- vertical scaling: replace current pods with more resources (CPU and memory) pods
			![[Pasted image 20231229031527.png | 600]]
		- horizontal scaling: increase/decrease number of pods
			- use stablization window for scaling (short for scale up, long for scale down)
			![[Pasted image 20231229031657.png | 600]]
8. kubernetes event driven autoscaling (KEDA)
	- usually use HPA for pod scaling in k8s with limited predefined metrics (like CPU, memory, ...) -> KDEA supports custom metrics
	- KEDA is custom resource definition (CRD) extends HPA
	- key roles:
		- activates/deactivates deployments to scale from/to 0 on no event (different from HPA)
		- acts as k8s metrics server, exposes event data to HPA to drive scale out
		- validates resource change to prevent misconfiguration
9. service mesh
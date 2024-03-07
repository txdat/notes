# Virtual private cloud
[GCP doc](https://cloud.google.com/vpc/docs/vpc)
- VPC is virtual version of physical network
- VPCs and their routes, firewall rules are *global* resources, are not associated with any region or zone
- Firewall supports ingress (inbound) and egress (outbound) rules for TCP, UDP, ICMP (`ping` command), ... protocols
- VPC has one or more subnets, subnet is *regional* resource, has specific IPv4/v6 range [wiki](https://en.wikipedia.org/wiki/Subnet)
- VPC can be shared between projects (shared VPC)
	- shared VPC is defined in host project and made available in shared projects
- VPC can connect with each other with virtual private network (VPN), cloud interconnect, network peering using internal ip addresses. VPC can connect to Google's service by using private service access
## Subnet
[GCP doc](https://cloud.google.com/vpc/docs/subnets)
- subnets are *regional* resources (in one or more zones), have ip addresses associated with them
- public subnets can access internet directly, private subnets require NAT
- 3 main types of subnet:
	- **regular**
		- for VM, GKE, backend services ...
	- proxy-only:
		- for regional load balancers (connection from proxy-only subnet to LB backend services)
		- provide a pool of ip address (subnet `/26` or more) that are *reserved exclusively* for envoy-based load balancers [GCP doc for proxy network load balancer](https://cloud.google.com/load-balancing/docs/proxy-network-load-balancer) (*regional only*), terminates client's request and send to target backend using forwarding rules
	- private-nat: for private-to-private translations across Google Cloud networks
![[Pasted image 20231229030749.png | 600]]
## Network peering
[GCP doc](https://cloud.google.com/vpc/docs/vpc-peering)
- Network peering connects *only* 2 VPCs so each network can connect with each other using internal ip addresses, their subnets' ip range cannot overlap
- **Transitive peering is not supported**. N1 is peered with N2, N3, but N2 and N3 cannot communicate (are not direclty connected)
- Some GCP services use network peering as default mode to connect VPC and service's *Google-managed* VPC -> use private service access to support transitive connection
- Support between VPCs:
	- route exchanges
	- internal LB (both application and network LB)
- Not support:
	- network security (firewall rules, policies)
	- DNS
## Private service access
[GCP doc](https://cloud.google.com/vpc/docs/private-services-access)
[GCP doc for private access options for services](https://cloud.google.com/vpc/docs/private-access-options)
[terraform](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/service_networking_connection)
- Private service access allow to use *internal IP addresses* of GCP services by private connections
- Private service access uses network peering for connection
- Must allocate internal ip address (subnet `/16` to `/24`) to VPC (allow transitive connection)
- **To support on-premises or other cloud connectivity through VPN or Cloud interconnect, allocated ip address for private service address must be advertised by VPN router in `bgp` block [terraform](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_router#bgp)**
# Virtual private network
[GCP doc](https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview)
- VPN connects peered network to VPC, support encryption by gateways
- too expensive (not recommended)
- 2 types of VPN
	- Classic VPN:
		- supports 1 interface, 1 external ip address, static routing
	- HA VPN:
		[GCP doc](https://cloud.google.com/network-connectivity/docs/vpn/concepts/topologies)
		- provide service availability SLA
		- uses 2 interfaces (1 external ip address for each), dynamic routing (BGP - border gateway (routing) protocol) (flexible and scalable network), and multiple tunnels
		- uses cloud-interconnect (physical connection) for encryption
		- to use HA-VPN encryption, deploy tunnels over VLAN attachments [GCP doc](https://cloud.google.com/network-connectivity/docs/interconnect/concepts/ha-vpn-interconnect) (requires cloud-interconnect)
		- HA-VPN gateway to peer devices:
			- 2 peer VPN devices: `TWO_IPS_REDUNDANCY`
				- redundancy and failover
				- 2 tunnels, one for each peer device
			- 1 peer VPN device with 2 ip addresses: `TWO_IPS_REDUNDANCY`
				- 2 tunnels, one for each ip address of peer device
			- 1 peer VPN device with 1 ip address: `SINGLE_IP_INTERNALLY_REDUNDANT`
				- 2 tunnels, both for ip address of peer device
			- AWS HA-VPN: `FOUR_IPS_REDUNDANCY`
				- 2 gateway interfaces
				- 2 peer VPN endpoints (2 customer gateways)
				- 4 tunnels, 2 tunnels from 1 VPN gateway inteface to peer endpoint (with 2 ip addresses)
				- Create HA-VPN between GCP and AWS step by step [tech.deriv's blog](https://tech.deriv.com/aws-gcp-ha-site-to-site-vpn/)
# Google kubernetes engine [[k8s]]
# Cloud load balancing
[GCP doc](https://cloud.google.com/load-balancing/docs/load-balancing-overview)
- distributes user traffic across multiple services, instances, ... (load balancing backend services) -> reduce risk
- connections are splitted to 2 paths: client -> LB and LB -> backend services
- supports:
	- single IP address
	- software-defined
	- seamless autoscaling
	- L4/L7, internal (inside VPC)/external, regional/global load balancing
	- TLS termination
	- cloud CDN, cloud armor, ...
- three-tier of web services:
	- web tier: client (web) -> web frontend (external application LB)
	- application tier: web frontend -> middlewares (internal application LB)
	- database tier: middlewares -> database (passthrough network LB)
- application (L7 - application layer) load balancer
	- for HTTP/HTTPs
	- LB terminates user traffic (and SSL), and creates new connections to backend services
	- support GKE gateway, ingress, or NEG
![[Pasted image 20231229031112.png | 600]]
- network (L4 - transport layer) load balancer
	- for TCP, UDP, ICMP, ...
	- (reversed) proxy network LB
		- LB terminates user traffic, and creates new connections to backend services
			![[Pasted image 20231229031207.png | 600]]
	- passthrough network LB
		 - keep packets' source, destination ip addresses, protocol, ...
		 - connections are terminated at backend services, and responses come go directely to clients, not back through LB
			 ![[Pasted image 20231229031245.png | 600]]
- proxy-only subnet for LB (regional internal/external load balancers)
	- requires reserved exclusively ip addresses for LB
	- client -> LB -> proxies (use internal ip addresses) -> backend services
- container-native load balancer through ingress
	- send requests from load balancer to services directly (through network endpoint groups - NEG), without using instances group and IP tables -> faster (without extra hops)
[[GCP - Network endpoint group]]
# Cloud DNS
- domain name system service publishes domain to global DNS
- distributed database stores ip addresses, other data and look up by name
- support DNSSEC for verifying origin of DNS data and validating data was modified or not
- some DNS' record types
![[Pasted image 20240116135156.png | 600]]
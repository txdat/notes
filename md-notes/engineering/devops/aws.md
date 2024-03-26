# VPC - isolated cloud resources
- launch aws resources in a logically isolated virtual network -> resemble a traditional network
- VPC spans all availability zones, and add one or more subnets to each zone
- each VPC has - [[AWS VPC]]
	- DHCP options - network settings (like DNS,NTP,...) used by resources in VPC [doc](https://docs.aws.amazon.com/vpc/latest/userguide/DHCPOptionSetConcepts.html)
	- network ACL - network access control list - [doc](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
		- allows or denies inbound/outbound traffic ==at subnet level== (between rounter and subnet)
		- each subnet has a network ACL
		- ACL is stateless, not save any information of previous requests/responses
		- ACL cannot block DNS requests from/to Route53 DNS resolver
	- security group
		- SG is assigned to EC2 instances ==at instance level==, acts as virtual firewall
	- route table
	- (optional) internet gateway
# EC2
# ECS
# EKS

# Load balancing
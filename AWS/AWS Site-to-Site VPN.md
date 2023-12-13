# AWS Site-to-Site VPN

## Customer gateway device

Physical device or software on our side of the VPN connection. When creating the connection, AWS provides the required configuration information, and network admin performs the configuration.

When creating Site-to-Site VPN Connection, you will be able to download configuration for most networking devices/appliances e.g.

- Check Point Security Gateway running R77.10 (or later) software
- Cisco ASA running Cisco ASA 8.2 (or later) software
- Cisco IOS running Cisco IOS 12.4 (or later) software
- SonicWALL running SonicOS 5.9 (or later) software
- Fortinet Fortigate 40+ Series running FortiOS 4.0 (or later) software 
- Juniper J-Series running JunOS 9.5 (or later) software
- Juniper SRX running JunOS 11.0 (or later) software
- Juniper SSG running ScreenOS 6.1, or 6.2 (or later) software
- Juniper ISG running ScreenOS 6.1, or 6.2 (or later) software
- Netgate pfSense running OS 2.2.5 (or later) software.
- Palo Alto Networks PANOS 4.1.2 (or later) software
- Yamaha RT107e, RTX1200, RTX1210, RTX1500, RTX3000 and SRT100 routers
- Microsoft Windows Server 2008 R2 (or later) software
- Microsoft Windows Server 2012 R2 (or later) software 
- Zyxel Zywall Series 4.20 (or later) software for statically routed VPN connections, or 4.30 (or later) software for dynamically routed VPN connections

### Creating customer gateway resource

Need the following info for a static IP connection:

* IP of customer gateway device's external interface
* Type of routing - static or dynamic (should be static)

## Virtual private gateway

Gateway for AWS side of the VPN connection

![img](https://docs.aws.amazon.com/vpn/latest/s2svpn/images/vpn-how-it-works-vgw.png)

## Transit gateway

Transit hub to interconnect VPCs and on-premise network. Can use either Transit or Virtual Private Gateway on AWS side. Acts as single target.

![img](https://docs.aws.amazon.com/vpn/latest/s2svpn/images/vpn-how-it-works-tgw.png)

## Authentication options

### Pre-shared keys

Default option. String you enter when configuring customer gateway device

### Private certificate

Use a private cert from AWS Certificate Manager Private Certificate Authority

## Steps to set up Site-to-Site VPN

### Prerequisites

1. Customer gateway device
   1. Physical or software device on our side of the connection, e.g. router. Need to provide vendor, platform and version
2. Customer gateway resource
   1. Externally-facing IP of our device
   2. Type of routing (static or dynamic)
   3. Optional: Private certificate
3. IP prefixes for the private network

### Steps

1. Create customer gateway on AWS Console - provide IP for on-premise device

2. Create Virtual Private Gateway on AWS side, and attach to the VPC

3. Configure routing
4. Update security group if necessary
5. Create Site-To-Site VPN connection
6. Download configuration file.
   1. Use this info to configure customer gateway device
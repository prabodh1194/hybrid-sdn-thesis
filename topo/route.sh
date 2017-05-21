#!/usr/bin/env bash

ip route add 10.0.0.0/16 dev s1-eth1 table 2 proto static scope link
ip route add 10.0.1.0/24 dev vlan11 table 6 proto static scope link
ip route add 10.0.2.0/24 dev vlan12 table 6 proto static scope link
ip route add 10.0.3.0/24 dev vlan13 table 6 proto static scope link
ip route add 10.0.4.0/24 dev vlan14 table 6 proto static scope link

ip route add 10.0.0.0/16 dev s2-eth1 table 3 proto static scope link
ip route add 10.0.1.0/24 dev vlan21 table 7 proto static scope link
ip route add 10.0.2.0/24 dev vlan22 table 7 proto static scope link
ip route add 10.0.3.0/24 dev vlan23 table 7 proto static scope link
ip route add 10.0.4.0/24 dev vlan24 table 7 proto static scope link

ip route add 10.0.0.0/16 dev s3-eth1 table 4 proto static scope link
ip route add 10.0.1.0/24 dev vlan31 table 8 proto static scope link
ip route add 10.0.2.0/24 dev vlan32 table 8 proto static scope link
ip route add 10.0.3.0/24 dev vlan33 table 8 proto static scope link
ip route add 10.0.4.0/24 dev vlan34 table 8 proto static scope link

ifconfig | grep "s[1-4]-eth1\|vlan.[12345]"|sed "s/-//"|sed "s/   Link encap:Ethernet  HWaddr//"|sed "s/  */=/" > macs
. $PWD/macs

for i in {1..4}; do for j in {1..16}; do for k in {1..4}; do sudo arp -s 10.0.$i.$j 10:00:00:00:00:01 -i s$k-eth1; done; done; done;

ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.1,in_port=2,actions=strip_vlan,set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.2,in_port=2,actions=strip_vlan,set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.3,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.4,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.1,actions=strip_vlan,set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.2,actions=strip_vlan,set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.3,actions=strip_vlan,set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.4,actions=strip_vlan,set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.1.0/24,in_port=5,actions=mod_vlan_vid:4,set_field:$vlan14"->"eth_dst,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.2.0/24,in_port=5,actions=mod_vlan_vid:1,set_field:$vlan11"->"eth_dst,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.3.0/24,in_port=5,actions=mod_vlan_vid:2,set_field:$vlan12"->"eth_dst,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.4.0/24,in_port=5,actions=mod_vlan_vid:3,set_field:$vlan13"->"eth_dst,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan14"->"eth_dst,set_field:$s1eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan11"->"eth_dst,set_field:$s1eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan12"->"eth_dst,set_field:$s1eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan13"->"eth_dst,set_field:$s1eth1"->"eth_src,output:5

ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.5,in_port=2,actions=strip_vlan,set_field:00:00:00:00:00:11"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.6,in_port=2,actions=strip_vlan,set_field:00:00:00:00:00:12"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.7,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:13"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.8,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:14"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.5,actions=strip_vlan,set_field:00:00:00:00:00:11"->"eth_dst,set_field:$vlan21"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.6,actions=strip_vlan,set_field:00:00:00:00:00:12"->"eth_dst,set_field:$vlan21"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.7,actions=strip_vlan,set_field:00:00:00:00:00:13"->"eth_dst,set_field:$vlan21"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.8,actions=strip_vlan,set_field:00:00:00:00:00:14"->"eth_dst,set_field:$vlan21"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.1.0/24,in_port=5,actions=mod_vlan_vid:4,set_field:$vlan24"->"eth_dst,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.2.0/24,in_port=5,actions=mod_vlan_vid:1,set_field:$vlan21"->"eth_dst,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.3.0/24,in_port=5,actions=mod_vlan_vid:2,set_field:$vlan22"->"eth_dst,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.4.0/24,in_port=5,actions=mod_vlan_vid:3,set_field:$vlan23"->"eth_dst,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan24"->"eth_dst,set_field:$s2eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan21"->"eth_dst,set_field:$s2eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan22"->"eth_dst,set_field:$s2eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan23"->"eth_dst,set_field:$s2eth1"->"eth_src,output:5

ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.9,in_port=2,actions=strip_vlan,set_field:00:00:00:00:00:21"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.10,in_port=2,actions=strip_vlan,set_field:00:00:00:00:00:22"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.11,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:23"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.12,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:24"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.9,actions=strip_vlan,set_field:00:00:00:00:00:21"->"eth_dst,set_field:$vlan31"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.10,actions=strip_vlan,set_field:00:00:00:00:00:22"->"eth_dst,set_field:$vlan31"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.11,actions=strip_vlan,set_field:00:00:00:00:00:23"->"eth_dst,set_field:$vlan31"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.12,actions=strip_vlan,set_field:00:00:00:00:00:24"->"eth_dst,set_field:$vlan31"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.1.0/24,in_port=5,actions=mod_vlan_vid:4,set_field:$vlan34"->"eth_dst,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.2.0/24,in_port=5,actions=mod_vlan_vid:1,set_field:$vlan31"->"eth_dst,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.3.0/24,in_port=5,actions=mod_vlan_vid:2,set_field:$vlan32"->"eth_dst,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.4.0/24,in_port=5,actions=mod_vlan_vid:3,set_field:$vlan33"->"eth_dst,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan34"->"eth_dst,set_field:$s3eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan31"->"eth_dst,set_field:$s3eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan32"->"eth_dst,set_field:$s3eth1"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan33"->"eth_dst,set_field:$s3eth1"->"eth_src,output:5

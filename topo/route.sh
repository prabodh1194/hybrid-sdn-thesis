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

ip route add 10.0.0.0/16 dev s4-eth1 table 5 proto static scope link
ip route add 10.0.1.0/24 dev vlan41 table 9 proto static scope link
ip route add 10.0.2.0/24 dev vlan42 table 9 proto static scope link
ip route add 10.0.3.0/24 dev vlan43 table 9 proto static scope link
ip route add 10.0.4.0/24 dev vlan44 table 9 proto static scope link

ifconfig | grep "s[1-4]-eth1\|vlan.[12345]"|sed "s/-//"|sed "s/   Link encap:Ethernet  HWaddr//"|sed "s/  */=/" > macs
. $PWD/macs

for i in {1..4}; do for j in {1..16}; do for k in {1..4}; do sudo arp -s 10.0.$i.$j 10:00:00:00:00:01 -i s$k-eth1; done; done; done;

ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.1,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.2,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.3,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.4,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.1,actions=strip_vlan,set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.2,actions=strip_vlan,set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.3,actions=strip_vlan,set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.4,actions=strip_vlan,set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.2.1,in_port=5,actions=strip_vlan,set_field:00:00:00:00:00:05"->"eth_dst,set_field:$vlan12"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.2.2,in_port=5,actions=strip_vlan,set_field:00:00:00:00:00:06"->"eth_dst,set_field:$vlan12"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.2.3,in_port=6,actions=strip_vlan,set_field:00:00:00:00:00:07"->"eth_dst,set_field:$vlan12"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.2.4,in_port=6,actions=strip_vlan,set_field:00:00:00:00:00:08"->"eth_dst,set_field:$vlan12"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.2.1,actions=strip_vlan,set_field:00:00:00:00:00:05"->"eth_dst,set_field:$vlan12"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.2.2,actions=strip_vlan,set_field:00:00:00:00:00:06"->"eth_dst,set_field:$vlan12"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.2.3,actions=strip_vlan,set_field:00:00:00:00:00:07"->"eth_dst,set_field:$vlan12"->"eth_src,output:6
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.2.4,actions=strip_vlan,set_field:00:00:00:00:00:08"->"eth_dst,set_field:$vlan12"->"eth_src,output:6
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.1,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.2,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.3,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.4,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.1,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.2,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.3,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.4,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.1,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.2,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.3,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.4,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.1,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.2,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.3,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.4,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan24"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan21"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan22"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan23"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.1.0/24,actions=IN_PORT,output:9,output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.2.0/24,actions=IN_PORT,output:9,output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.3.0/24,actions=IN_PORT,output:9,output:10
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.4.0/24,actions=IN_PORT,output:9,output:10

ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.9,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:21"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.10,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:22"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.11,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:23"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.12,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:24"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.9,actions=strip_vlan,set_field:00:00:00:00:00:21"->"eth_dst,set_field:$vlan31"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.10,actions=strip_vlan,set_field:00:00:00:00:00:22"->"eth_dst,set_field:$vlan31"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.11,actions=strip_vlan,set_field:00:00:00:00:00:23"->"eth_dst,set_field:$vlan31"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.12,actions=strip_vlan,set_field:00:00:00:00:00:24"->"eth_dst,set_field:$vlan31"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.2.9,in_port=5,actions=strip_vlan,set_field:00:00:00:00:00:25"->"eth_dst,set_field:$vlan32"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.2.10,in_port=5,actions=strip_vlan,set_field:00:00:00:00:00:26"->"eth_dst,set_field:$vlan32"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.2.11,in_port=6,actions=strip_vlan,set_field:00:00:00:00:00:27"->"eth_dst,set_field:$vlan32"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.2.12,in_port=6,actions=strip_vlan,set_field:00:00:00:00:00:28"->"eth_dst,set_field:$vlan32"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.2.9,actions=strip_vlan,set_field:00:00:00:00:00:25"->"eth_dst,set_field:$vlan32"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.2.10,actions=strip_vlan,set_field:00:00:00:00:00:26"->"eth_dst,set_field:$vlan32"->"eth_src,output:5
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.2.11,actions=strip_vlan,set_field:00:00:00:00:00:27"->"eth_dst,set_field:$vlan32"->"eth_src,output:6
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.2.12,actions=strip_vlan,set_field:00:00:00:00:00:28"->"eth_dst,set_field:$vlan32"->"eth_src,output:6
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.3.9,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.3.10,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.3.11,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.3.12,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.3.9,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.3.10,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.3.11,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.3.12,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.4.9,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.4.10,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.4.11,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=4,nw_dst=10.0.4.12,in_port=9,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.4.9,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.4.10,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.4.11,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=3,nw_dst=10.0.4.12,actions=output:10
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan34"->"eth_dst,set_field:$s3eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan31"->"eth_dst,set_field:$s3eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan32"->"eth_dst,set_field:$s3eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan33"->"eth_dst,set_field:$s3eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=2,nw_src=10.0.1.0/24,actions=IN_PORT,output:9,output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=2,nw_src=10.0.2.0/24,actions=IN_PORT,output:9,output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=2,nw_src=10.0.3.0/24,actions=IN_PORT,output:9,output:10
ovs-ofctl -OOpenFlow13 add-flow s13 table=1,ip,priority=2,nw_src=10.0.4.0/24,actions=IN_PORT,output:9,output:10

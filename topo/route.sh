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

ip route add 10.0.0.0/16 dev s3-eth5 table 4 proto static scope link
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
for i in {1..4}; do for j in {1..16}; do sudo arp -s 10.0.$i.$j 10:00:00:00:00:01 -i s3-eth5; done; done;

ovs-ofctl -OOpenFlow13 add-flow s17 dl_dst=ff:ff:ff:ff:ff:ff,actions=push_vlan:0x8100,set_field:4'->'vlan_vid,FLOOD,goto_table:1 
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,dl_dst=ff:ff:ff:ff:ff:ff,actions=strip_vlan,FLOOD,CONTROLLER:65535
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.1,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.2,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.3,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.4,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.1,actions=strip_vlan,set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.2,actions=strip_vlan,set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.3,actions=strip_vlan,set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.4,actions=strip_vlan,set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.2.1,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.2.2,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.2.3,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.2.4,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.2.1,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.2.2,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.2.3,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.2.4,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.1,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.2,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.3,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.3.4,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.1,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.2,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.3,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.3.4,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.1,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.2,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.3,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=4,nw_dst=10.0.4.4,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.1,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.2,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.3,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=3,nw_dst=10.0.4.4,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan14"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan11"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan12"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan13"->"eth_dst,set_field:$s1eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,in_port=8,nw_src=10.0.1.0/24,actions=set_field:$vlan24"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,in_port=8,nw_src=10.0.2.0/24,actions=set_field:$vlan21"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,in_port=8,nw_src=10.0.3.0/24,actions=set_field:$vlan22"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,in_port=8,nw_src=10.0.4.0/24,actions=set_field:$vlan23"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.1.0/24,actions=set_field:$vlan24"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.2.0/24,actions=set_field:$vlan21"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.3.0/24,actions=set_field:$vlan22"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s5 table=1,ip,priority=2,nw_src=10.0.4.0/24,actions=set_field:$vlan23"->"eth_dst,output:8

ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.13,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:31"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.14,in_port=3,actions=strip_vlan,set_field:00:00:00:00:00:32"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.15,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:33"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.16,in_port=4,actions=strip_vlan,set_field:00:00:00:00:00:34"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.13,actions=strip_vlan,set_field:00:00:00:00:00:31"->"eth_dst,set_field:$vlan41"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.14,actions=strip_vlan,set_field:00:00:00:00:00:32"->"eth_dst,set_field:$vlan41"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.15,actions=strip_vlan,set_field:00:00:00:00:00:33"->"eth_dst,set_field:$vlan41"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.16,actions=strip_vlan,set_field:00:00:00:00:00:34"->"eth_dst,set_field:$vlan41"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.2.13,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.2.14,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.2.15,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.2.16,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.2.13,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.2.14,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.2.15,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.2.16,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.3.13,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.3.14,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.3.15,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.3.16,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.3.13,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.3.14,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.3.15,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.3.16,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.4.13,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.4.14,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.4.15,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=4,nw_dst=10.0.4.16,in_port=7,actions=IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.4.13,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.4.14,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.4.15,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=3,nw_dst=10.0.4.16,actions=output:7
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=2,nw_src=10.0.1.0/24,actions=mod_vlan_vid:4,set_field:$vlan44"->"eth_dst,set_field:$s4eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=2,nw_src=10.0.2.0/24,actions=mod_vlan_vid:1,set_field:$vlan41"->"eth_dst,set_field:$s4eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=2,nw_src=10.0.3.0/24,actions=mod_vlan_vid:2,set_field:$vlan42"->"eth_dst,set_field:$s4eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=2,nw_src=10.0.4.0/24,actions=mod_vlan_vid:3,set_field:$vlan43"->"eth_dst,set_field:$s4eth1"->"eth_src,goto_table:1
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,in_port=8,nw_src=10.0.1.0/24,actions=set_field:$vlan34"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,in_port=8,nw_src=10.0.2.0/24,actions=set_field:$vlan31"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,in_port=8,nw_src=10.0.3.0/24,actions=set_field:$vlan32"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,in_port=8,nw_src=10.0.4.0/24,actions=set_field:$vlan33"->"eth_dst,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,nw_src=10.0.1.0/24,actions=set_field:$vlan34"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,nw_src=10.0.2.0/24,actions=set_field:$vlan31"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,nw_src=10.0.3.0/24,actions=set_field:$vlan32"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,ip,priority=2,nw_src=10.0.4.0/24,actions=set_field:$vlan33"->"eth_dst,output:8
ovs-ofctl -OOpenFlow13 add-flow s17 dl_dst=ff:ff:ff:ff:ff:ff,actions=push_vlan:0x8100,set_field:4'->'vlan_vid,FLOOD,goto_table:1 
ovs-ofctl -OOpenFlow13 add-flow s17 table=1,dl_dst=ff:ff:ff:ff:ff:ff,actions=strip_vlan,FLOOD,CONTROLLER:65535

ip route add 10.0.0.0/16 dev s1-eth1 table 2 proto static scope link
ip route add 10.0.1.0/24 dev vlan11 table 6 proto static scope link src 10.0.1.251
ip route add 10.0.2.0/24 dev vlan12 table 6 proto static scope link src 10.0.2.251
ip route add 10.0.3.0/24 dev vlan13 table 6 proto static scope link src 10.0.3.251
ip route add 10.0.4.0/24 dev vlan14 table 6 proto static scope link src 10.0.4.251

ip route add 10.0.0.0/16 dev s2-eth1 table 3 proto static scope link
ip route add 10.0.1.0/24 dev vlan21 table 7 proto static scope link src 10.0.1.252
ip route add 10.0.2.0/24 dev vlan22 table 7 proto static scope link src 10.0.2.252
ip route add 10.0.3.0/24 dev vlan23 table 7 proto static scope link src 10.0.3.252
ip route add 10.0.4.0/24 dev vlan24 table 7 proto static scope link src 10.0.4.252

ip route add 10.0.0.0/16 dev s3-eth1 table 4 proto static scope link
ip route add 10.0.1.0/24 dev vlan31 table 8 proto static scope link src 10.0.1.253
ip route add 10.0.2.0/24 dev vlan32 table 8 proto static scope link src 10.0.2.253
ip route add 10.0.3.0/24 dev vlan33 table 8 proto static scope link src 10.0.3.253
ip route add 10.0.4.0/24 dev vlan34 table 8 proto static scope link src 10.0.4.253

ip route add 10.0.0.0/16 dev s4-eth1 table 5 proto static scope link
ip route add 10.0.1.0/24 dev vlan41 table 9 proto static scope link src 10.0.1.254
ip route add 10.0.2.0/24 dev vlan42 table 9 proto static scope link src 10.0.2.254
ip route add 10.0.3.0/24 dev vlan43 table 9 proto static scope link src 10.0.3.254
ip route add 10.0.4.0/24 dev vlan44 table 9 proto static scope link src 10.0.4.254

ifconfig | grep "s[1-4]-eth1\|vlan.[15]"|sed "s/-//"|sed "s/   Link encap:Ethernet  HWaddr//"|sed "s/  */=/" > macs
. $PWD/macs
arp -s 10.0.1.1 $s1eth1 -i s1-eth1
arp -s 10.0.1.2 $s1eth1 -i s1-eth1
arp -s 10.0.1.3 $s1eth1 -i s1-eth1
arp -s 10.0.1.4 $s1eth1 -i s1-eth1
arp -s 10.0.2.1 $s1eth1 -i s1-eth1
arp -s 10.0.2.2 $s1eth1 -i s1-eth1
arp -s 10.0.2.3 $s1eth1 -i s1-eth1
arp -s 10.0.2.4 $s1eth1 -i s1-eth1
arp -s 10.0.3.1 $s1eth1 -i s1-eth1
arp -s 10.0.3.2 $s1eth1 -i s1-eth1
arp -s 10.0.3.3 $s1eth1 -i s1-eth1
arp -s 10.0.3.4 $s1eth1 -i s1-eth1
arp -s 10.0.4.1 $s1eth1 -i s1-eth1
arp -s 10.0.4.2 $s1eth1 -i s1-eth1
arp -s 10.0.4.3 $s1eth1 -i s1-eth1
arp -s 10.0.4.4 $s1eth1 -i s1-eth1

arp -s 10.0.1.5 $s2eth1 -i s2-eth1
arp -s 10.0.1.6 $s2eth1 -i s2-eth1
arp -s 10.0.1.7 $s2eth1 -i s2-eth1
arp -s 10.0.1.8 $s2eth1 -i s2-eth1
arp -s 10.0.2.5 $s2eth1 -i s2-eth1
arp -s 10.0.2.6 $s2eth1 -i s2-eth1
arp -s 10.0.2.7 $s2eth1 -i s2-eth1
arp -s 10.0.2.8 $s2eth1 -i s2-eth1
arp -s 10.0.3.5 $s2eth1 -i s2-eth1
arp -s 10.0.3.6 $s2eth1 -i s2-eth1
arp -s 10.0.3.7 $s2eth1 -i s2-eth1
arp -s 10.0.3.8 $s2eth1 -i s2-eth1
arp -s 10.0.4.5 $s2eth1 -i s2-eth1
arp -s 10.0.4.6 $s2eth1 -i s2-eth1
arp -s 10.0.4.7 $s2eth1 -i s2-eth1
arp -s 10.0.4.8 $s2eth1 -i s2-eth1

arp -s 10.0.1.9  $s3eth1 -i s3-eth1
arp -s 10.0.1.10 $s3eth1 -i s3-eth1
arp -s 10.0.1.11 $s3eth1 -i s3-eth1
arp -s 10.0.1.12 $s3eth1 -i s3-eth1
arp -s 10.0.2.9  $s3eth1 -i s3-eth1
arp -s 10.0.2.10 $s3eth1 -i s3-eth1
arp -s 10.0.2.11 $s3eth1 -i s3-eth1
arp -s 10.0.2.12 $s3eth1 -i s3-eth1
arp -s 10.0.3.9  $s3eth1 -i s3-eth1
arp -s 10.0.3.10 $s3eth1 -i s3-eth1
arp -s 10.0.3.11 $s3eth1 -i s3-eth1
arp -s 10.0.3.12 $s3eth1 -i s3-eth1
arp -s 10.0.4.9  $s3eth1 -i s3-eth1
arp -s 10.0.4.10 $s3eth1 -i s3-eth1
arp -s 10.0.4.11 $s3eth1 -i s3-eth1
arp -s 10.0.4.12 $s3eth1 -i s3-eth1

arp -s 10.0.1.13 $s4eth1 -i s4-eth1
arp -s 10.0.1.14 $s4eth1 -i s4-eth1
arp -s 10.0.1.15 $s4eth1 -i s4-eth1
arp -s 10.0.1.16 $s4eth1 -i s4-eth1
arp -s 10.0.2.13 $s4eth1 -i s4-eth1
arp -s 10.0.2.14 $s4eth1 -i s4-eth1
arp -s 10.0.2.15 $s4eth1 -i s4-eth1
arp -s 10.0.2.16 $s4eth1 -i s4-eth1
arp -s 10.0.3.13 $s4eth1 -i s4-eth1
arp -s 10.0.3.14 $s4eth1 -i s4-eth1
arp -s 10.0.3.15 $s4eth1 -i s4-eth1
arp -s 10.0.3.16 $s4eth1 -i s4-eth1
arp -s 10.0.4.13 $s4eth1 -i s4-eth1
arp -s 10.0.4.14 $s4eth1 -i s4-eth1
arp -s 10.0.4.15 $s4eth1 -i s4-eth1
arp -s 10.0.4.16 $s4eth1 -i s4-eth1

ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.1,in_port=2,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.2,in_port=2,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.3,in_port=3,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=4,nw_dst=10.0.1.4,in_port=3,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.1,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:$vlan11"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.2,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:$vlan11"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.3,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=3,nw_dst=10.0.1.4,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:$vlan11"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.2.0/24,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.3.0/24,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.4.0/24,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=1,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=1,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,priority=1,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT

ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.5,in_port=2,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.6,in_port=2,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.7,in_port=3,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=4,nw_dst=10.0.1.8,in_port=3,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:$vlan21"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.5,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:$vlan21"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.6,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:$vlan21"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.7,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:$vlan21"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=3,nw_dst=10.0.1.8,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:$vlan21"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.2.0/24,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.3.0/24,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.4.0/24,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=1,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=1,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,priority=1,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT

ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.9,in_port=2,actions=set_field:00:00:00:00:00:09"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.10,in_port=2,actions=set_field:00:00:00:00:00:0a"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.11,in_port=3,actions=set_field:00:00:00:00:00:0b"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=4,nw_dst=10.0.1.12,in_port=3,actions=set_field:00:00:00:00:00:0c"->"eth_dst,set_field:$vlan31"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.9,actions=set_field:00:00:00:00:00:09"->"eth_dst,set_field:$vlan31"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.10,actions=set_field:00:00:00:00:00:0a"->"eth_dst,set_field:$vlan31"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.11,actions=set_field:00:00:00:00:00:0b"->"eth_dst,set_field:$vlan31"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=3,nw_dst=10.0.1.12,actions=set_field:00:00:00:00:00:0c"->"eth_dst,set_field:$vlan31"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.2.0/24,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.3.0/24,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.4.0/24,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=1,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=1,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,priority=1,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT

ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.13,in_port=2,actions=set_field:00:00:00:00:00:0d"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.14,in_port=2,actions=set_field:00:00:00:00:00:0e"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.15,in_port=3,actions=set_field:00:00:00:00:00:0f"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=4,nw_dst=10.0.1.16,in_port=3,actions=set_field:00:00:00:00:00:10"->"eth_dst,set_field:$vlan41"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.13,actions=set_field:00:00:00:00:00:0d"->"eth_dst,set_field:$vlan41"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.14,actions=set_field:00:00:00:00:00:0e"->"eth_dst,set_field:$vlan41"->"eth_src,output:2
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.15,actions=set_field:00:00:00:00:00:0f"->"eth_dst,set_field:$vlan41"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=3,nw_dst=10.0.1.16,actions=set_field:00:00:00:00:00:10"->"eth_dst,set_field:$vlan41"->"eth_src,output:3
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.2.0/24,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.3.0/24,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=1,nw_src=10.0.1.0/24,nw_dst=10.0.4.0/24,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,output:4
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=1,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=1,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,priority=1,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT

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

s1eth1=76:e4:14:1e:d2:5f
s2eth1=72:a9:28:1e:19:ec
s3eth1=62:e2:4f:41:a4:cb
s4eth1=da:e2:f7:2a:bc:99
vlan15=7a:94:95:48:49:81
vlan25=f6:a1:a9:65:5f:a2
vlan35=ba:37:7f:8f:9b:62
vlan45=3a:96:3f:2c:36:70

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

ovs-ofctl -OOpenFlow13 add-flow s5 ip,nw_src=10.0.1.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s5 ip,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan15"->"eth_dst,mod_vlan_vid:5,set_field:$s1eth1"->"eth_src,IN_PORT

ovs-ofctl -OOpenFlow13 add-flow s9 ip,nw_src=10.0.1.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s9 ip,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan25"->"eth_dst,mod_vlan_vid:5,set_field:$s2eth1"->"eth_src,IN_PORT

ovs-ofctl -OOpenFlow13 add-flow s13 ip,nw_src=10.0.1.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s13 ip,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan35"->"eth_dst,mod_vlan_vid:5,set_field:$s3eth1"->"eth_src,IN_PORT

ovs-ofctl -OOpenFlow13 add-flow s17 ip,nw_src=10.0.1.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,nw_src=10.0.2.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,nw_src=10.0.3.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT
ovs-ofctl -OOpenFlow13 add-flow s17 ip,nw_src=10.0.4.0/24,in_port=4,actions=set_field:$vlan45"->"eth_dst,mod_vlan_vid:5,set_field:$s4eth1"->"eth_src,IN_PORT

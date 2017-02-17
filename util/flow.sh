sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:01,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:01"->"eth_src,output:1

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:02,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:02"->"eth_src,output:1

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:03,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:03"->"eth_src,output:1

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,output:1
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:04,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:04"->"eth_src,output:1

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:05,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:05"->"eth_src,IN_PORT

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:06,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:06"->"eth_src,IN_PORT

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:07,dl_dst=10:00:00:00:00:08,actions=set_field:00:00:00:00:00:08"->"eth_dst,set_field:10:00:00:00:00:07"->"eth_src,IN_PORT

sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:01,actions=set_field:00:00:00:00:00:01"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:02,actions=set_field:00:00:00:00:00:02"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,output:2
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:03,actions=set_field:00:00:00:00:00:03"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:04,actions=set_field:00:00:00:00:00:04"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,output:3
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:05,actions=set_field:00:00:00:00:00:05"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:06,actions=set_field:00:00:00:00:00:06"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,IN_PORT
sudo ovs-ofctl -O OpenFlow13 add-flow s2 dl_src=00:00:00:00:00:08,dl_dst=10:00:00:00:00:07,actions=set_field:00:00:00:00:00:07"->"eth_dst,set_field:10:00:00:00:00:08"->"eth_src,IN_PORT


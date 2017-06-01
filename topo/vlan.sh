#sudo ovs-vsctl del-port s3 s3-eth3
#sudo ovs-vsctl add-port s3 s3-eth3 tag=10
#
#sudo ovs-vsctl del-port s1 s1-eth1
#sudo ovs-vsctl add-port s1 s1-eth1 trunks=10,20

sudo ovs-vsctl del-port s1 s1-eth5
sudo ovs-vsctl add-port s1 s1-eth5 trunks=1,2,3,4
sudo ovs-vsctl del-port s2 s2-eth5
sudo ovs-vsctl add-port s2 s2-eth5 trunks=1,2,3,4
sudo ovs-vsctl del-port s2 s2-eth6
sudo ovs-vsctl add-port s2 s2-eth6 trunks=1,2,3,4
sudo ovs-vsctl del-port s3 s3-eth5
sudo ovs-vsctl add-port s3 s3-eth5 trunks=1,2,3,4
sudo ovs-vsctl del-port s3 s3-eth6
sudo ovs-vsctl add-port s3 s3-eth6 trunks=1,2,3,4
sudo ovs-vsctl del-port s4 s4-eth5
sudo ovs-vsctl add-port s4 s4-eth5 trunks=1,2,3,4
sudo ovs-vsctl del-port s4 s4-eth6
sudo ovs-vsctl add-port s4 s4-eth6 trunks=1,2,3,4
sudo ovs-vsctl del-port s5 s5-eth5
sudo ovs-vsctl add-port s5 s5-eth5 trunks=1,2,3,4
sudo ovs-vsctl del-port s1 s1-eth1
sudo ovs-vsctl add-port s1 s1-eth1 trunks=1,2,3,4
sudo ovs-vsctl del-port s5 s5-eth1
sudo ovs-vsctl add-port s5 s5-eth1 trunks=1,2,3,4

sudo ovs-vsctl add-port s1 vlan11 tag=1 -- set interface vlan11 type=internal
sudo ovs-vsctl add-port s1 vlan12 tag=2 -- set interface vlan12 type=internal
sudo ovs-vsctl add-port s1 vlan13 tag=3 -- set interface vlan13 type=internal
sudo ovs-vsctl add-port s1 vlan14 tag=4 -- set interface vlan14 type=internal
sudo ifconfig vlan11 10.0.1.251/24
sudo ifconfig vlan12 10.0.2.251/24
sudo ifconfig vlan13 10.0.3.251/24
sudo ifconfig vlan14 10.0.4.251/24

# sudo ovs-vsctl add-port s2 vlan21 tag=1 -- set interface vlan21 type=internal
# sudo ovs-vsctl add-port s2 vlan22 tag=2 -- set interface vlan22 type=internal
# sudo ovs-vsctl add-port s2 vlan23 tag=3 -- set interface vlan23 type=internal
# sudo ovs-vsctl add-port s2 vlan24 tag=4 -- set interface vlan24 type=internal
# sudo ifconfig vlan21 10.0.1.252/24
# sudo ifconfig vlan22 10.0.2.252/24
# sudo ifconfig vlan23 10.0.3.252/24
# sudo ifconfig vlan24 10.0.4.252/24
 
# sudo ovs-vsctl add-port s3 vlan31 tag=1 -- set interface vlan31 type=internal
# sudo ovs-vsctl add-port s3 vlan32 tag=2 -- set interface vlan32 type=internal
# sudo ovs-vsctl add-port s3 vlan33 tag=3 -- set interface vlan33 type=internal
# sudo ovs-vsctl add-port s3 vlan34 tag=4 -- set interface vlan34 type=internal
# sudo ifconfig vlan31 10.0.1.253/24
# sudo ifconfig vlan32 10.0.2.253/24
# sudo ifconfig vlan33 10.0.3.253/24
# sudo ifconfig vlan34 10.0.4.253/24

# sudo ovs-vsctl add-port s4 vlan41 tag=1 -- set interface vlan41 type=internal
# sudo ovs-vsctl add-port s4 vlan42 tag=2 -- set interface vlan42 type=internal
# sudo ovs-vsctl add-port s4 vlan43 tag=3 -- set interface vlan43 type=internal
# sudo ovs-vsctl add-port s4 vlan44 tag=4 -- set interface vlan44 type=internal
# sudo ifconfig vlan41 10.0.1.254/24
# sudo ifconfig vlan42 10.0.2.254/24
# sudo ifconfig vlan43 10.0.3.254/24
# sudo ifconfig vlan44 10.0.4.254/24

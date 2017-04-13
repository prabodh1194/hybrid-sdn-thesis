sudo ovs-vsctl del-port s4 s4-eth1
sudo ovs-vsctl add-port s4 s4-eth1 tag=10
sudo ovs-vsctl del-port s4 s4-eth2
sudo ovs-vsctl add-port s4 s4-eth2 tag=10
sudo ovs-vsctl del-port s4 s4-eth3
sudo ovs-vsctl add-port s4 s4-eth3 tag=10

sudo ovs-vsctl del-port s5 s5-eth1
sudo ovs-vsctl add-port s5 s5-eth1 tag=20
sudo ovs-vsctl del-port s5 s5-eth2
sudo ovs-vsctl add-port s5 s5-eth2 tag=20
sudo ovs-vsctl del-port s5 s5-eth3
sudo ovs-vsctl add-port s5 s5-eth3 tag=20

sudo ovs-vsctl del-port s6 s6-eth1
sudo ovs-vsctl add-port s6 s6-eth1 tag=20
sudo ovs-vsctl del-port s6 s6-eth2
sudo ovs-vsctl add-port s6 s6-eth2 tag=20
sudo ovs-vsctl del-port s6 s6-eth3
sudo ovs-vsctl add-port s6 s6-eth3 tag=20

sudo ovs-vsctl del-port s7 s7-eth1
sudo ovs-vsctl add-port s7 s7-eth1 tag=10
sudo ovs-vsctl del-port s7 s7-eth2
sudo ovs-vsctl add-port s7 s7-eth2 tag=10
sudo ovs-vsctl del-port s7 s7-eth3
sudo ovs-vsctl add-port s7 s7-eth3 tag=10

sudo ovs-vsctl del-port s2 s2-eth1
sudo ovs-vsctl add-port s2 s2-eth1 trunks=10,20
sudo ovs-vsctl del-port s2 s2-eth2
sudo ovs-vsctl add-port s2 s2-eth2 tag=10
sudo ovs-vsctl del-port s2 s2-eth3
sudo ovs-vsctl add-port s2 s2-eth3 tag=20

sudo ovs-vsctl del-port s3 s3-eth1
sudo ovs-vsctl add-port s3 s3-eth1 trunks=10,20
sudo ovs-vsctl del-port s3 s3-eth2
sudo ovs-vsctl add-port s3 s3-eth2 tag=20
sudo ovs-vsctl del-port s3 s3-eth3
sudo ovs-vsctl add-port s3 s3-eth3 tag=10

sudo ovs-vsctl del-port s1 s1-eth1
sudo ovs-vsctl add-port s1 s1-eth1 trunks=10,20
sudo ovs-vsctl del-port s1 s1-eth2
sudo ovs-vsctl add-port s1 s1-eth2 trunks=10,20

sudo ovs-vsctl add-port s1 vlan10 tag=10 -- set interface vlan10 type=internal
sudo ovs-vsctl add-port s1 vlan20 tag=20 -- set interface vlan20 type=internal
sudo ifconfig vlan10 10.0.1.1/24
sudo ifconfig vlan20 10.0.2.1/24


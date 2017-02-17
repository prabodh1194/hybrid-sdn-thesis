#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, Host, Controller, RemoteController, OVSController
from mininet.log import setLogLevel, info
import os, pdb, re

os.system('sudo mn -c')

net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='secure')
s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='secure')
s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')
s6 = net.addSwitch('s6', cls=OVSKernelSwitch, failMode='standalone')
s7 = net.addSwitch('s7', cls=OVSKernelSwitch, failMode='standalone')
s8 = net.addSwitch('s8', cls=OVSKernelSwitch, failMode='standalone')
s9 = net.addSwitch('s9', cls=OVSKernelSwitch, failMode='standalone')
s10= net.addSwitch('s10', cls=OVSKernelSwitch, failMode='standalone')

h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
h8 = net.addHost('h8', cls=Host, ip='10.0.0.8 ', defaultRoute=None)
h9 = net.addHost('h9', cls=Host, ip='10.0.0.9 ', defaultRoute=None)
h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)
h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
h13 = net.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None)

net.addLink(s1,s2)
net.addLink(s1,s3)
net.addLink(s1,s4)
net.addLink(s1,h13)

net.addLink(s2,s5)
net.addLink(s2,s6)

net.addLink(s3,s7)
net.addLink(s3,s8)

net.addLink(s4,s9)
net.addLink(s4,s10)

net.addLink(s5,h1)
net.addLink(s5,h2)

net.addLink(s6,h3)
net.addLink(s6,h4)

net.addLink(s7,h5)
net.addLink(s7,h6)

net.addLink(s8,h7)
net.addLink(s8,h8)

net.addLink(s9,h9)
net.addLink(s9,h10)

net.addLink(s10,h11)
net.addLink(s10,h12)

c0=net.addController(name='c0',
                  controller=RemoteController,
                  protocol='tcp',
                  port=6633)

net.build()

h1.setMAC('00:00:00:00:00:01')
h2.setMAC('00:00:00:00:00:02')
h3.setMAC('00:00:00:00:00:03')
h4.setMAC('00:00:00:00:00:04')
h5.setMAC('00:00:00:00:00:05')
h6.setMAC('00:00:00:00:00:06')
h7.setMAC('00:00:00:00:00:07')
h8.setMAC('00:00:00:00:00:08')
h9.setMAC('00:00:00:00:00:09')
h10.setMAC('00:00:00:00:00:0a')
h11.setMAC('00:00:00:00:00:0b')
h12.setMAC('00:00:00:00:00:0c')

h1.setARP('10.0.0.2','10:00:00:00:00:02')
h1.setARP('10.0.0.3','10:00:00:00:00:03')
h1.setARP('10.0.0.4','10:00:00:00:00:04')
h1.setARP('10.0.0.5','10:00:00:00:00:05')
h1.setARP('10.0.0.6','10:00:00:00:00:06')
h1.setARP('10.0.0.7','10:00:00:00:00:07')
h1.setARP('10.0.0.8 ','10:00:00:00:00:08')
h1.setARP('10.0.0.9 ','10:00:00:00:00:09')
h1.setARP('10.0.0.10','10:00:00:00:00:0a')
h1.setARP('10.0.0.11','10:00:00:00:00:0b')
h1.setARP('10.0.0.12','10:00:00:00:00:0c')

h2.setARP('10.0.0.1','10:00:00:00:00:01')
h2.setARP('10.0.0.3','10:00:00:00:00:03')
h2.setARP('10.0.0.4','10:00:00:00:00:04')
h2.setARP('10.0.0.5','10:00:00:00:00:05')
h2.setARP('10.0.0.6','10:00:00:00:00:06')
h2.setARP('10.0.0.7','10:00:00:00:00:07')
h2.setARP('10.0.0.8 ','10:00:00:00:00:08')
h2.setARP('10.0.0.9 ','10:00:00:00:00:09')
h2.setARP('10.0.0.10','10:00:00:00:00:0a')
h2.setARP('10.0.0.11','10:00:00:00:00:0b')
h2.setARP('10.0.0.12','10:00:00:00:00:0c')

h3.setARP('10.0.0.1','10:00:00:00:00:01')
h3.setARP('10.0.0.2','10:00:00:00:00:02')
h3.setARP('10.0.0.4','10:00:00:00:00:04')
h3.setARP('10.0.0.5','10:00:00:00:00:05')
h3.setARP('10.0.0.6','10:00:00:00:00:06')
h3.setARP('10.0.0.7','10:00:00:00:00:07')
h3.setARP('10.0.0.8','10:00:00:00:00:08')
h3.setARP('10.0.0.9','10:00:00:00:00:09')
h3.setARP('10.0.0.10','10:00:00:00:00:0a')
h3.setARP('10.0.0.11','10:00:00:00:00:0b')
h3.setARP('10.0.0.12','10:00:00:00:00:0c')

h4.setARP('10.0.0.1','10:00:00:00:00:01')
h4.setARP('10.0.0.2','10:00:00:00:00:02')
h4.setARP('10.0.0.3','10:00:00:00:00:03')
h4.setARP('10.0.0.5','10:00:00:00:00:05')
h4.setARP('10.0.0.6','10:00:00:00:00:06')
h4.setARP('10.0.0.7','10:00:00:00:00:07')
h4.setARP('10.0.0.8','10:00:00:00:00:08')
h4.setARP('10.0.0.9','10:00:00:00:00:09')
h4.setARP('10.0.0.10','10:00:00:00:00:0a')
h4.setARP('10.0.0.11','10:00:00:00:00:0b')
h4.setARP('10.0.0.12','10:00:00:00:00:0c')

h5.setARP('10.0.0.1','10:00:00:00:00:01')
h5.setARP('10.0.0.2','10:00:00:00:00:02')
h5.setARP('10.0.0.3','10:00:00:00:00:03')
h5.setARP('10.0.0.4','10:00:00:00:00:04')
h5.setARP('10.0.0.6','10:00:00:00:00:06')
h5.setARP('10.0.0.7','10:00:00:00:00:07')
h5.setARP('10.0.0.8','10:00:00:00:00:08')
h5.setARP('10.0.0.9','10:00:00:00:00:09')
h5.setARP('10.0.0.10','10:00:00:00:00:0a')
h5.setARP('10.0.0.11','10:00:00:00:00:0b')
h5.setARP('10.0.0.12','10:00:00:00:00:0c')

h6.setARP('10.0.0.1','10:00:00:00:00:01')
h6.setARP('10.0.0.2','10:00:00:00:00:02')
h6.setARP('10.0.0.3','10:00:00:00:00:03')
h6.setARP('10.0.0.4','10:00:00:00:00:04')
h6.setARP('10.0.0.5','10:00:00:00:00:05')
h6.setARP('10.0.0.7','10:00:00:00:00:07')
h6.setARP('10.0.0.8','10:00:00:00:00:08')
h6.setARP('10.0.0.9','10:00:00:00:00:09')
h6.setARP('10.0.0.10','10:00:00:00:00:0a')
h6.setARP('10.0.0.11','10:00:00:00:00:0b')
h6.setARP('10.0.0.12','10:00:00:00:00:0c')

h7.setARP('10.0.0.1','10:00:00:00:00:01')
h7.setARP('10.0.0.2','10:00:00:00:00:02')
h7.setARP('10.0.0.3','10:00:00:00:00:03')
h7.setARP('10.0.0.4','10:00:00:00:00:04')
h7.setARP('10.0.0.5','10:00:00:00:00:05')
h7.setARP('10.0.0.6','10:00:00:00:00:06')
h7.setARP('10.0.0.8','10:00:00:00:00:08')
h7.setARP('10.0.0.9 ','10:00:00:00:00:09')
h7.setARP('10.0.0.10','10:00:00:00:00:0a')
h7.setARP('10.0.0.11','10:00:00:00:00:0b')
h7.setARP('10.0.0.12','10:00:00:00:00:0c')

h8.setARP('10.0.0.1','10:00:00:00:00:01')
h8.setARP('10.0.0.2','10:00:00:00:00:02')
h8.setARP('10.0.0.3','10:00:00:00:00:03')
h8.setARP('10.0.0.4','10:00:00:00:00:04')
h8.setARP('10.0.0.5','10:00:00:00:00:05')
h8.setARP('10.0.0.6','10:00:00:00:00:06')
h8.setARP('10.0.0.7','10:00:00:00:00:07')
h8.setARP('10.0.0.9 ','10:00:00:00:00:09')
h8.setARP('10.0.0.10','10:00:00:00:00:0a')
h8.setARP('10.0.0.11','10:00:00:00:00:0b')
h8.setARP('10.0.0.12','10:00:00:00:00:0c')

h9.setARP('10.0.0.1','10:00:00:00:00:01')
h9.setARP('10.0.0.2','10:00:00:00:00:02')
h9.setARP('10.0.0.3','10:00:00:00:00:03')
h9.setARP('10.0.0.4 ','10:00:00:00:00:04')
h9.setARP('10.0.0.5','10:00:00:00:00:05')
h9.setARP('10.0.0.6','10:00:00:00:00:06')
h9.setARP('10.0.0.7','10:00:00:00:00:07')
h9.setARP('10.0.0.8','10:00:00:00:00:08')
h9.setARP('10.0.0.10','10:00:00:00:00:0a')
h9.setARP('10.0.0.11','10:00:00:00:00:0b')
h9.setARP('10.0.0.12','10:00:00:00:00:0c')

h10.setARP('10.0.0.1','10:00:00:00:00:01')
h10.setARP('10.0.0.2','10:00:00:00:00:02')
h10.setARP('10.0.0.3','10:00:00:00:00:03')
h10.setARP('10.0.0.4','10:00:00:00:00:04')
h10.setARP('10.0.0.5','10:00:00:00:00:05')
h10.setARP('10.0.0.6','10:00:00:00:00:06')
h10.setARP('10.0.0.7','10:00:00:00:00:07')
h10.setARP('10.0.0.8 ','10:00:00:00:00:08')
h10.setARP('10.0.0.9 ','10:00:00:00:00:09')
h10.setARP('10.0.0.11','10:00:00:00:00:0b')
h10.setARP('10.0.0.12','10:00:00:00:00:0c')

h11.setARP('10.0.0.1','10:00:00:00:00:01')
h11.setARP('10.0.0.2','10:00:00:00:00:02')
h11.setARP('10.0.0.3','10:00:00:00:00:03')
h11.setARP('10.0.0.4','10:00:00:00:00:04')
h11.setARP('10.0.0.5','10:00:00:00:00:05')
h11.setARP('10.0.0.6','10:00:00:00:00:06')
h11.setARP('10.0.0.7','10:00:00:00:00:07')
h11.setARP('10.0.0.8 ','10:00:00:00:00:08')
h11.setARP('10.0.0.9 ','10:00:00:00:00:09')
h11.setARP('10.0.0.10','10:00:00:00:00:0a')
h11.setARP('10.0.0.12','10:00:00:00:00:0c')

h12.setARP('10.0.0.1 ','10:00:00:00:00:01')
h12.setARP('10.0.0.2 ','10:00:00:00:00:02')
h12.setARP('10.0.0.3 ','10:00:00:00:00:03')
h12.setARP('10.0.0.4 ','10:00:00:00:00:04')
h12.setARP('10.0.0.5 ','10:00:00:00:00:05')
h12.setARP('10.0.0.6 ','10:00:00:00:00:06')
h12.setARP('10.0.0.7 ','10:00:00:00:00:07')
h12.setARP('10.0.0.8 ','10:00:00:00:00:08')
h12.setARP('10.0.0.9 ','10:00:00:00:00:09')
h12.setARP('10.0.0.10','10:00:00:00:00:0a')
h12.setARP('10.0.0.11','10:00:00:00:00:0b')

# mirrors for debugging purpose
# h14 = net.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None)
# h15 = net.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None)
# h16 = net.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None)
# 
h13.setMAC('00:00:00:00:00:0d')
# h14.setMAC('00:00:00:00:00:0e')
# h15.setMAC('00:00:00:00:00:0f')
# h16.setMAC('00:00:00:00:00:10')
# 
# net.addLink(s1,h13)
# net.addLink(s2,h14)
# net.addLink(s3,h15)
# net.addLink(s4,h16)


s1.start([])
s2.start([c0])
s3.start([])
s4.start([c0])
s5.start([])
s6.start([])
s7.start([])
s8.start([])
s9.start([])
s10.start([])

os.system('sudo ovs-vsctl set bridge \"s1\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s2\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s3\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s4\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s5\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s6\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s7\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s8\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s9\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s10\" protocols=OpenFlow13')

pattern = '[sh]([0-9]+)-eth([0-9]+)'

# Try to change MACs of interfaces. Didn't work. Were reset.
# for l in net.links:
#     print l.intf1, l.intf2
#     m1 = re.search(pattern, str(l.intf1))
#     m2 = re.search(pattern, str(l.intf2))
#
#     if m1 is not None and str(l.intf1)[0] != 'h':
#         mac = "00:00:00:0{4}:{2}{3}:{0}{1}".format(m1.group(1), m1.group(2),m1.group(1),m2.group(1),1 if str(l.intf2)[0] == 'h' else 0)
#         l.intf1.setMAC(mac)
#
#     if m2 is not None and str(l.intf2)[0] != 'h':
#         mac = "00:00:00:00:{2}{3}:{0}{1}".format(m2.group(1), m2.group(2),m2.group(1),m1.group(1))
#         l.intf2.setMAC(mac)

CLI(net)
net.stop()

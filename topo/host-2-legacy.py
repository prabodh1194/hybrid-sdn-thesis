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

s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='secure')
s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')


h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)

net.addLink(s1,s2)
net.addLink(s1,s3)
net.addLink(s1,h5)

net.addLink(s2,h1)
net.addLink(s2,h2)

net.addLink(s3,h3)
net.addLink(s3,h4)

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

s1.start([c0])
s2.start([])
s3.start([])

os.system('sudo ovs-vsctl set bridge \"s1\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s2\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s3\" protocols=OpenFlow13')

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

h5.cmd("python ../stats/packet.py 10.0.0.1")

CLI(net)
net.stop()

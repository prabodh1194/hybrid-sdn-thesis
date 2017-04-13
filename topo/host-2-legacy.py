#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, Host, Controller, RemoteController, OVSController, Node
from mininet.log import setLogLevel, info
import os, pdb, re

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."
    def config( self, **params ):
        print(params)
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

os.system('sudo mn -c')

net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')
s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')
s6 = net.addSwitch('s6', cls=OVSKernelSwitch, failMode='standalone')
s7 = net.addSwitch('s7', cls=OVSKernelSwitch, failMode='standalone')

h1 = net.addHost('h1', cls=Host, ip='10.0.1.2/24', defaultRoute=None)
h2 = net.addHost('h2', cls=Host, ip='10.0.1.3/24', defaultRoute=None)
h3 = net.addHost('h3', cls=Host, ip='10.0.2.2/24', defaultRoute=None)
h4 = net.addHost('h4', cls=Host, ip='10.0.2.3/24', defaultRoute=None)
h5 = net.addHost('h5', cls=Host, ip='10.0.2.4/24', defaultRoute=None)
h6 = net.addHost('h6', cls=Host, ip='10.0.2.5/24', defaultRoute=None)
h7 = net.addHost('h7', cls=Host, ip='10.0.1.4/24', defaultRoute=None)
h8 = net.addHost('h8', cls=Host, ip='10.0.1.5/24', defaultRoute=None)

l = net.addLink(s1,s2)
l = net.addLink(s1,s3)

net.addLink(s2,s4)
net.addLink(s2,s5)

net.addLink(s3,s6)
net.addLink(s3,s7)

net.addLink(s4,h1)
net.addLink(s4,h2)

net.addLink(s5,h3)
net.addLink(s5,h4)

net.addLink(s6,h5)
net.addLink(s6,h6)

net.addLink(s7,h7)
net.addLink(s7,h8)

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

h1.cmd('sudo route add default gw 10.0.1.1 h1-eth0')
h2.cmd('sudo route add default gw 10.0.1.1 h2-eth0')
h3.cmd('sudo route add default gw 10.0.2.1 h3-eth0')
h4.cmd('sudo route add default gw 10.0.2.1 h4-eth0')
h5.cmd('sudo route add default gw 10.0.2.1 h5-eth0')
h6.cmd('sudo route add default gw 10.0.2.1 h6-eth0')
h7.cmd('sudo route add default gw 10.0.1.1 h7-eth0')
h8.cmd('sudo route add default gw 10.0.1.1 h8-eth0')

h1.cmd('sudo ip route del 10.0.1.0/24 ')
h2.cmd('sudo ip route del 10.0.1.0/24 ')
h3.cmd('sudo ip route del 10.0.2.0/24 ')
h4.cmd('sudo ip route del 10.0.2.0/24 ')
h5.cmd('sudo ip route del 10.0.2.0/24 ')
h6.cmd('sudo ip route del 10.0.2.0/24 ')
h7.cmd('sudo ip route del 10.0.1.0/24 ')
h8.cmd('sudo ip route del 10.0.1.0/24 ')

s1.start([])
s2.start([])
s3.start([])
s4.start([])
s5.start([])
s6.start([])
s7.start([])

os.system('sudo ovs-vsctl set bridge \"s1\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s2\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s3\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s4\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s5\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s6\" protocols=OpenFlow13')
os.system('sudo ovs-vsctl set bridge \"s7\" protocols=OpenFlow13')

CLI(net)
net.stop()

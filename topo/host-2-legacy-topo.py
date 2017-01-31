#!/usr/bin/python
"""Custom topology example

Two directly connected switches plus a host for each switch:

    host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import CPULimitedHost, Host, Node
from mininet.link import TCLink, Intf
class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
        s1 = self.addSwitch( 's1', cls=OVSKernelSwitch, failMode='standalone')

        # Add links
        hs = {'bw':100}
        self.addLink( h1, s1, cls=TCLink, **hs)
        self.addLink( h2, s1, cls=TCLink, **hs)
        self.addLink( h3, s1, cls=TCLink, **hs)


topos = { 'mytopo': ( lambda: MyTopo() ) }

#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
from mininet.topolib import TreeNet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
import pdb

class legacySwitch( OVSSwitch ):
    def start( self, *args, **kwargs ):
        OVSSwitch.start( self, *args, **kwargs )
        self.cmd( 'ovs-vsctl set-fail-mode', self, 'standalone' )

if __name__ == '__main__':
    setLogLevel( 'info' )
    network = TreeNet( depth=1, fanout=2, switch=legacySwitch)
    info( "Dumping host connections\n" )
    # dumpNodeConnections(network.hosts)
    network.run( CLI, network )

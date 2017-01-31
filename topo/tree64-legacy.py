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
import pdb,os,sys

class legacySwitch( OVSSwitch ):
    def start( self, *args, **kwargs ):
        OVSSwitch.start( self, *args, **kwargs )
        self.cmd( 'ovs-vsctl set-fail-mode', self, 'standalone' )

def startIperf(net):
    num_hosts = len(net.hosts)
    res = {}

    for i in range(num_hosts/2):
        h1 = net.hosts[i]
        h2 = net.hosts[-i-1]

        h1.cmd('iperf -us -f M > '+folder+'/servout'+str(h1)+' &')
        # h1.cmd('tcpdump > '+folder+'/servouttcp'+str(h1)+' &')
        h2.cmd('iperf -c '+h1.IP()+' -f M -b 80M -t 10 > '+folder+'/cliout'+str(h2)+' &')
        # h2.cmd('tcpdump > '+folder+'/cliouttcp'+str(h2)+' &')
        # h1.terminate()
        # h2.cmd('ping -c10 '+h1.IP()+' > out'+str(h2)+' &')

if __name__ == '__main__':

    if len(sys.argv) !=2:
        print "Argument l for legacy test required"
        sys.exit(-1)

    global switch
    global folder

    if sys.argv[1] == "l":
        switch = legacySwitch
        folder = "legacy"
    else:
        switch = OVSSwitch
        folder = "SDN"

    setLogLevel( 'info' )
    network = TreeNet( depth=2, fanout=8, switch=switch)
    # network.run (CLI, network)
    network.start()
    startIperf(network)

    network.run (CLI, network)

    # while True:
    #     pid = os.waitpid(-1,0)
    #     print pid
    #     if pid is None:
    #         break

    # network.stop()

    # sys.exit(0)

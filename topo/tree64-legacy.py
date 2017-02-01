#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import OVSKernelSwitch, OVSSwitch, Host
from mininet.topolib import TreeNet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
import pdb,os,sys, argparse

def setMirrors(depth, fanout):

    cmd = "sudo ovs-vsctl -- set Bridge {0} mirrors=@m"
    mirr = "-- --id=@eth{0} get Port s{1}-eth{0}"
    ports = []
    mirrors = (pow(fanout,depth-1)-1)/(fanout-1)

    for i in range(mirrors):
        print i

def treeNet(net, depth, fanout, switches):
    '''
    @param net
        The Mininetnet network refernce
    @param depth
        Depth of tree. e.g., depth of 3 means the root switch and host have 2
        more switches in between
    @param fanout
        Number of links on each switch
    @param switches
        A list of switches which should be SDN enabled. Default is standalone
    '''

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    switchCount = 1
    mirrors = []
    for i in range (depth):
        level = pow(fanout, i)
        for j in range(level):
            switchName = 's'+str(switchCount)
            s = net.addSwitch(switchName,
                          cls=OVSKernelSwitch,
                          failMode='secure' if switchName in switches else 'standalone')

            # add a mirror port for logging purpose
            if i < depth-1:
                h = net.addHost('hmirror'+str(switchCount), cls=Host, ip='10.0.0.'+str(255-switchCount), defaultRoute=None)
                net.addLink(s,h)

            if i > 0:
                prevSwitch = switchCount - j - level/fanout + j/fanout
                l = net.addLink(s, net.get('s'+str(prevSwitch)))

            switchCount += 1

    info( '*** Add hosts\n')
    numHosts = pow(fanout, depth)
    switchOff = 1+(pow(fanout, depth-1)-1)/(fanout-1)
    for i in range(numHosts):
        h = net.addHost('h'+str(i+1), cls=Host, ip='10.0.0.'+str(i+1), defaultRoute=None)
        net.addLink(h, net.get('s'+str(switchOff+i/fanout)))


    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    for switch in net.switches:
        if str(switch) in switches:
            info('*** switch connected to controller ',switch,'\n')
            switch.start([c0])
        else:
            switch.start([])

    info( '*** Post configure switches and hosts\n')

    setMirrors(depth, fanout)

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

        h1.cmd('iperf -us -f M > servout'+str(h1)+' &')
        # h1.cmd('tcpdump > servouttcp'+str(h1)+' &')
        h2.cmd('iperf -c '+h1.IP()+' -f M -b 80M -t 10 > cliout'+str(h2)+' &')
        # h2.cmd('tcpdump > cliouttcp'+str(h2)+' &')
        # h1.terminate()
        # h2.cmd('ping -c10 '+h1.IP()+' > out'+str(h2)+' &')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a mininet simulation for tree topology')
    parser.add_argument('-d', '--depth', help='Depth of mininet tree', nargs=1, default=[3], type=int)
    parser.add_argument('-f', '--fanout', help='Number of links on each switch', nargs=1, default=[4], type=int)
    parser.add_argument('-s', '--switches', help='Names of switches to have SDN. Switches are numbered in level-order of a tree starting from 1. Enter a space seperated list', nargs='*', default={}, type=str)

    args = parser.parse_args()

    print args

    setLogLevel( 'info' )

    info('*** building a tree of depth',args.depth[0],'and fanout',args.fanout[0],'\n')
    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
    treeNet(net, args.depth[0], args.fanout[0], set(args.switches))
    CLI(net)
    net.stop()

    # startIperf(network)

    # while True:
    #     pid = os.waitpid(-1,0)
    #     print pid
    #     if pid is None:
    #         break

    # sys.exit(0)

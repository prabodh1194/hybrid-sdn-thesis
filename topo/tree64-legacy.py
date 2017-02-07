#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import OVSKernelSwitch, OVSSwitch, Host
from mininet.topolib import TreeNet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import pdb,os,sys,argparse,re,time

def parseDumps(hostCount, name):

    res = []
    servers = hostCount/2
    pattern = ".*\s+([0-9\.]*)\s+MBytes/sec.*"
    for i in range(servers):
        files = open('servout'+name+'h'+str(i+1))

        for l in files:
            if 'receiver' in l:
                m = re.match(pattern,l)
                res += [float(m.group(1))]
    return res

def setMirrors(switchCount, fanout):
    cmd = ''
    ovs = "sudo ovs-vsctl -- set Bridge s{0} mirrors=@m"
    mirr = " -- --id=@eth{0} get Port s{1}-eth{0}"
    set = " -- --id=@m create Mirror name=mymirror{0} select-dst-port={1} select-src-port={1} output-port=@eth1"
    ports = ''
    mirrors = switchCount

    for j in range(fanout):
        ports += '@eth'+str(j+2)+','
    ports = ports[:-1]

    for i in range(mirrors):
        cmd = ''
        cmd += ovs.format(i+1)
        for j in range(fanout+1):
            cmd += mirr.format(j+1,i+1)
        cmd += set.format(i+1,ports)
        info(cmd)
        os.system(cmd)

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
    hs100 = {'bw':100} #Mbit/s
    hs1000 = {'bw':1000} #Mbit/s
    mirrors = []
    for i in range (depth):
        level = pow(fanout, i)
        for j in range(level):
            switchName = 's'+str(switchCount)
            s = net.addSwitch(switchName,
                          cls=OVSKernelSwitch,
                          failMode='secure' if switchName in switches else 'standalone')

            # add a mirror port for logging purpose
            # h = net.addHost('hmirror'+str(switchCount), cls=Host, ip='10.0.0.'+str(255-switchCount), defaultRoute=None)
            # net.addLink(s, h, cls=TCLink, **hs100)

            if i > 0:
                prevSwitch = switchCount - j - level/fanout + j/fanout
                hs = hs1000 if i == 1 else hs100
                l = net.addLink(s, net.get('s'+str(prevSwitch)), cls=TCLink, **hs)

            switchCount += 1

    info( '*** Add hosts\n')
    numHosts = pow(fanout, depth)
    switchOff = 1+(pow(fanout, depth-1)-1)/(fanout-1)
    for i in range(numHosts):
        h = net.addHost('h'+str(i+1), cls=Host, ip='10.0.0.'+str(i+1), defaultRoute=None)
        net.addLink(h, net.get('s'+str(switchOff+i/fanout)), cls=TCLink, **hs100)


    info( '*** Starting network\n')
    net.build()

    info( '*** Starting switches\n')
    for switch in net.switches:
        if str(switch) in switches:
            info('*** switch connected to controller ',switch,'\n')
            switch.start([c0])
            os.system('sudo ovs-vsctl set bridge \"'+str(switch)+'\" protocols=OpenFlow13')
        else:
            switch.start([])

    info( '*** Post configure switches and hosts\n')
    return c0,numHosts

def startIperf(net,name):
    hosts = []
    mirrors = []

    for h in net.hosts:
        if 'mirror' in str(h):
            mirrors += [h]
        else:
            hosts += [h]

    num_hosts = len(hosts)
    res = {}

    # start tcpdump on mirrors
    # for m in mirrors:
    #     m.cmd('tcpdump -nnvvS udp and net 10.0.0.0/8 > '+str(m)+' &')

    for i in range(num_hosts/2):
        h1 = hosts[i]
        h2 = hosts[-i-1]
        h1.cmd('/usr/local/bin/iperf3 -1 -s -f M > servout'+name+str(h1)+' &')

        # We want to close server as soon as the client is done, hence using
        # this hack to extract the pid of iperf3 server and supplying it to
        # the iperf3 client to kill after it's done executing
        # ps = h1.cmdPrint('ps')
        # b = ''
        # for line in ps.split('\r\n'):
        #     b = re.match('\s*([0-9]+).*iperf3',line)
        #     if b is not None:
        #         break

        # Can not record client side data too
        h2.cmd('iperf3 -c '+h1.IP()+' -f M -b 800M -t 10 &')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a mininet simulation for tree topology')
    parser.add_argument('-d', '--depth', help='Depth of mininet tree', nargs=1, default=[3], type=int)
    parser.add_argument('-f', '--fanout', help='Number of links on each switch', nargs=1, default=[4], type=int)
    parser.add_argument('-s', '--switches', help='Names of switches to have SDN. Switches are numbered in level-order of a tree starting from 1. Enter a space seperated list', nargs='*', default={}, type=str)
    parser.add_argument('-c', '--cli', help='Display CLI on given topology.', action='store_true')

    args = parser.parse_args()

    setLogLevel( 'warning' )

    info('*** building a tree of depth',args.depth[0],'and fanout',args.fanout[0],'\n')

    switchCount = (pow(args.fanout[0],args.depth[0])-1)/(args.fanout[0]-1)

    if args.cli:
	setLogLevel('info')
        net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
        treeNet(net, args.depth[0], args.fanout[0], set(args.switches))
        CLI(net)
        net.stop()
        exit(0)

    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
    c0,hostCount = treeNet(net, args.depth[0], args.fanout[0], set(args.switches))

    # setMirrors(switchCount, args.fanout[0])
    print "Testing",','.join(args.switches)
    k = ','.join([str(a) for a in args.depth]+[str(b) for b in args.fanout]+[] if args.switches == {} else args.switches)
    startIperf(net,k)

    # poll for iperfs to die
    while True:
        ps = os.popen('ps a').read()
        if 'iperf' not in ps:
            break

    net.stop()

    data = parseDumps(hostCount, k)

    pair = (k,data)

    print pair

    exit(0)

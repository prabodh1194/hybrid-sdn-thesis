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
    mirr = " -- --id=@eth{2} get Port s{1}-eth{0}"
    setm = " -- --id=@m create Mirror name=mymirror{0} select-dst-port={1} select-src-port={1} output-port=@eth{2}"
    ports = ''
    mirrors = switchCount

    for j in range(fanout):
        ports += '@eth'+str(j+1)+','
    ports = ports[:-1]

    for i in range(mirrors):
        cmd = ''
        cmd += ovs.format(i+1)
        for j in range(fanout+1):
            if i != 0:
                cmd += mirr.format(j+2,i+1,j+1)
            else:
                cmd += mirr.format(j+1,i+1,j+1)
        cmd += setm.format(i+1,ports,fanout+1)
        info(cmd)
        os.system(cmd, )

def close(switch, switches):
    for s in switches:
        if s>=switch:
            return s
    return switches[-1]

def generateFlows(topo,switches,fanout,numHosts):
    stdout = sys.stdout
    # 2 -- output:_ / IN_PORT
    # 3 -- switch
    sdn_switch = [int(s[1:]) for s in switches if int(s[1:]) in range(2,2+fanout)]
    sdn_switch.sort()
    flow = 'sudo ovs-ofctl -O OpenFlow13 add-flow {3} dl_src=00:00:00:00:00:{0},dl_dst=10:00:00:00:00:{1},actions=set_field:00:00:00:00:00:{1}"->"eth_dst,set_field:10:00:00:00:00:{0}"->"eth_src,{2}'
    sys.stdout = open(FLOW_FILE, 'w+')

    # pdb.set_trace()
    for i in range(0,numHosts):
        print
        for j in range(i,numHosts):

            if i == j:
                continue

            h_src = 'h'+str(i+1)
            h_dst = 'h'+str(j+1)
            print '>&2 echo \'',h_src,h_dst,'\''
            s = topo[topo[h_dst][0]] # distro layer switch
            # port = 'IN_PORT' if topo[h_src][0] == topo[h_dst][0] else 'output:'+ (s[1] if s[0] == topo[topo[h_src][0]][0] else '2' if mirror else '1')

            if topo[topo[h_src][0]][0] in switches: # src host is connected to an OF switch
                switch = topo[topo[h_src][0]][0]
            elif s[0] in switches: # dst host is connected to an OF switch
                switch = s[0]
            else: # neither src nor dst are on OF switches; greedily select a switch closest of two options
                s_no = int(s[0][1:])
                switch = close(s_no, sdn_switch)
                # switch = 's'+str(switch[0] if abs(switch[0]-s_no) <= abs(switch[1]-s_no) else switch[1])
                switch = 's'+str(switch)

            # there can be a number of cases in which a packet is re-directed to an OF port.

            # both src and dst are under same distro switch
            if s[0] == topo[topo[h_src][0]][0]:
                if topo[h_src][0] == topo[h_dst][0] or s[0] != switch:
                    # same access switch or under a distro switch which is not OF
                    port = 'IN_PORT'
                else:
                    port = 'output:'+s[1]
            # or under different distro switch
            else:
                if s[0] == switch:
                    # dst lies under a distro switch which is OF enabled
                    port = 'output:'+s[1]
                elif topo[topo[h_src][0]][0] == switch:
                    # src lies under an OF switch
                    port = 'output:1'
                else:
                    # dst and src lie on separate non-of switch
                    port = 'IN_PORT'

            print '#'+switch
            flowadd = flow.format(hex(i+1)[2:].zfill(2), hex(j+1)[2:].zfill(2),port,switch)
            print flowadd

            h_src, h_dst = h_dst, h_src
            print '>&2 echo \'',h_src,h_dst,'\''
            s = topo[topo[h_dst][0]] # distro layer switch
            # port = 'IN_PORT' if topo[h_src][0] == topo[h_dst][0] else 'output:'+ (s[1] if s[0] == topo[topo[h_src][0]][0] else '2' if mirror else '1')

            # there can be a number of cases in which a packet is re-directed to an OF port.

            # both src and dst are under same distro switch
            if s[0] == topo[topo[h_src][0]][0]:
                if topo[h_src][0] == topo[h_dst][0] or s[0] != switch:
                    # same access switch or under a distro switch which is not OF
                    port = 'IN_PORT'
                else:
                    port = 'output:'+s[1]
            # or under different distro switch
            else:
                if s[0] == switch:
                    # dst lies under a distro switch which is OF enabled
                    port = 'output:'+s[1]
                elif topo[topo[h_src][0]][0] == switch:
                    # src lies under an OF switch
                    port = 'output:1'
                else:
                    # dst and src lie on separate non-of switch
                    port = 'IN_PORT'

            print '#'+switch
            flowadd = flow.format(hex(j+1)[2:].zfill(2), hex(i+1)[2:].zfill(2),port,switch)
            print flowadd

    sys.stdout = stdout

def printTopoDS(net,switches):
    topo = {}
    pattern = "([sh][0-9]+)-eth([0-9]+)"
    for l in net.links:

        if 'mirror' in str(l):
            continue
        i1 = re.search(pattern,str(l.intf1)).group(1)
        i2 = re.search(pattern,str(l.intf2)).group(1)
        topo[i1] = (i2,re.search(pattern,str(l.intf2)).group(2))

    stdout = sys.stdout
    sys.stdout = open(TOPO_FILE, 'w+')
    print len(topo)
    for k in topo:
        print k,topo[k]
    print ','.join([s[1:] for s in switches])
    sys.stdout = stdout
    return topo

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

            # # add a mirror port for logging purpose
            # if mirror:
            #     h = net.addHost('hmirror'+str(switchCount), cls=Host, ip='10.0.0.'+str(255-switchCount), defaultRoute=None)
            #     net.addLink(s, h, cls=TCLink, **hs100)

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

    for host in net.hosts:

        if 'mirror' in str(host):
            continue
        mac = '00:00:00:00:00:'+hex(int(str(host)[1:]))[2:].zfill(2)
        host.setMAC(mac)
        for host2 in net.hosts:
            if 'mirror' in str(host2):
                continue
            if str(host) == str(host2):
                continue
            mac = '10:00:00:00:00:'+hex(int(str(host2)[1:]))[2:].zfill(2)
            host.setARP(host2.IP(), mac)

    info( '*** Starting switches\n')
    for switch in net.switches:

        # add a mirror port for logging purpose
        if mirror:
            h = net.addHost('hmirror'+str(switch)[1:], cls=Host, ip='10.0.0.'+str(255-int(str(switch)[1:])), defaultRoute=None)
            net.addLink(switch, h, cls=TCLink, **hs100)

        if str(switch) in switches:
            info('*** switch connected to controller ',switch,'\n')
            switch.start([c0])
            os.system('sudo ovs-vsctl set bridge \"'+str(switch)+'\" protocols=OpenFlow13')
        else:
            switch.start([])

    info( '*** Post configure switches and hosts\n')

    topo = printTopoDS(net, switches)
    generateFlows(topo,switches,fanout,numHosts)

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

    for i in range(num_hosts/2):
        h1 = hosts[i]
        h2 = hosts[-i-1]
        h1.cmd('/usr/local/bin/iperf3 -1 -s -f M > servout'+name+str(h1)+' &')

        # Can not record client side data too
        h2.cmd('iperf3 -c '+h1.IP()+' -f M -b 800M -t 10 >> cli &')

if __name__ == '__main__':

    TOPO_FILE = 'topo_tree_adj_list'
    FLOW_FILE = 'flow.sh'

    parser = argparse.ArgumentParser(description='Run a mininet simulation for tree topology')
    parser.add_argument('-c', '--cli', help='Display CLI on given topology.', action='store_true')
    parser.add_argument('-d', '--depth', help='Depth of mininet tree', nargs=1, default=[3], type=int)
    parser.add_argument('-f', '--fanout', help='Number of links on each switch', nargs=1, default=[4], type=int)
    parser.add_argument('-m', '--mirrors', help='Setup mirrors on internal switches for debugging purpose', action='store_true')
    parser.add_argument('-s', '--switches', help='''Names of switches to have
                        SDN. Switches are numbered in level-order of a tree
                        starting from 1. Enter a space seperated list''',
                        nargs='*', default={}, type=str)

    global mirror
    args = parser.parse_args()
    mirror = args.mirrors

    info('*** building a tree of depth',args.depth[0],'and fanout',args.fanout[0],'\n')

    switchCount = (pow(args.fanout[0],args.depth[0])-1)/(args.fanout[0]-1)

    if args.cli:
        setLogLevel( 'info' )
        net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
        treeNet(net, args.depth[0], args.fanout[0], set(args.switches))
        if args.mirrors:
            setMirrors(switchCount, args.fanout[0])
        os.system('sh flow.sh')
        CLI(net)
        net.stop()
        exit(0)

    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
    c0,hostCount = treeNet(net, args.depth[0], args.fanout[0], set(args.switches))
    if args.mirrors:
        setMirrors(switchCount, args.fanout[0])

    print "Testing",','.join(args.switches)
    k = ','.join([str(a) for a in args.depth]+[str(b) for b in args.fanout]+[] if args.switches == {} else args.switches)
    os.system('sh flow.sh')
    setLogLevel( 'info' )
    net.pingAll()
    setLogLevel( 'warning' )
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

#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import OVSSwitch, Host, Node
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from math import ceil
import os,sys,argparse,re,time,json,pdb

range1 = lambda start, end: range(start, end+1)

def back(topo):
    topo_back = {}
    for k in topo:
        for i in range1(*topo[k]):
            topo_back[i] = k
    return topo_back

topo_vlan = {1:[6,10,14,18,22],2:[7,11,15,19,23],3:[8,13,16,20,24],4:[9,13,17,21,25]}

topo_vlan_back = {}
for vlan in topo_vlan:
    for i in topo_vlan[vlan]:
        topo_vlan_back[i] = topo_vlan_back.get(i,[]) + [vlan]

topo_core = {1:[6,9],2:[10,13],3:[14,17],4:[18,21],5:[22,25]}
topo_distro = {6:[26,27],7:[28,29],8:[30,31],9:[32,33],10:[34,35],11:[36,37],12:[38,39],13:[40,41],14:[42,43],15:[44,45],16:[46,47],17:[48,49],18:[50,51],19:[52,53],20:[54,55],21:[56,57],22:[58,59],23:[60,61],24:[62,63],25:[64,65]}
topo_access = {26: [1, 2], 27: [3, 4], 28: [5, 6], 29: [7, 8], 30: [9, 10], 31:
        [11, 12], 32: [13, 14], 33: [15, 16], 34: [17, 18], 35: [19, 20], 36:
        [21, 22], 37: [23, 24], 38: [25, 26], 39: [27, 28], 40: [29, 30], 41:
        [31, 32], 42: [33, 34], 43: [35, 36], 44: [37, 38], 45: [39, 40], 46:
        [41, 42], 47: [43, 44], 48: [45, 46], 49: [47, 48], 50: [49, 50], 51:
        [51, 52], 52: [53, 54], 53: [55, 56], 54: [57, 58], 55: [59, 60], 56:
        [61, 62], 57: [63, 64], 58: [65, 66], 59: [67, 68], 60: [69, 70], 61:
        [71, 72], 62: [73, 74], 63: [75, 76], 64: [77, 78], 65: [79, 80]}
topo_subnet = {1:[[1,4],[17,20],[33,36],[49,52],[65,68]],2:[[5,8],[21,24],[37,40],[53,56],[69,72]],3:[[9,12],[25,28],[41,44],[57,60],[73,76]],4:[[13,16],[29,32],[45,48],[61,64],[77,80]]}

topo_core_back = back(topo_core)
topo_distro_back = back(topo_distro)
topo_access_back = back(topo_access)
topo_subnet_back = {}

for k in topo_subnet:
    for l in topo_subnet[k]:
        for i in range1(*l):
            topo_subnet_back[i] = k

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

def close(switch, switches):
    for s in switches:
        if s>=switch:
            return s
    return switches[-1]

def printTopoDS(net,switches):
    topo = {}
    pattern = "eth([0-9]+)"
    for l in net.links:

        if 'mirror' in str(l):
            continue
        i1 = str(l.intf1.node)
        i2 = str(l.intf2.node)
        topo[i1] = (i2,re.search(pattern,str(l.intf2)).group(1),l.intf1.IP())

    stdout = sys.stdout
    sys.stdout = open(TOPO_FILE, 'w+')
    print json.dumps(topo)
    sys.stdout = stdout
    return topo

def treeNet(net, switches):
    '''
    @param net
        The Mininetnet network refernce
    @param switches
        A list of switches which should be SDN enabled. Default is standalone
    '''

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
            controller=RemoteController,
            protocol='tcp',
            port=6633)

    info( '*** Add switches\n')

    hs100 = {'bw':100,'delay':'10ms'} #Mbit/s
    hs1000 = {'bw':1000,'delay':'10ms'} #Mbit/s

    info( '*** Add core and distribution\n')
    for sw in topo_core:
        s_core = net.addSwitch('s'+str(sw), cls=OVSSwitch, failMode='standalone')

        for i in range1(*topo_core[sw]):
            switchName = 's'+str(i)
            s = None
            try:
                s = net.get(switchName)
            except KeyError:
                s = net.addSwitch(switchName, cls=OVSSwitch,
                        failMode='secure' if switchName in switches else
                        'standalone')
            link = net.addLink(s, s_core, cls=TCLink, **hs1000)

    info( '*** Add access\n')
    for sw in topo_distro:
        for i in range1(*topo_distro[sw]):
            switchName = 's'+str(i)
            s = None
            try:
                s = net.get(switchName)
            except KeyError:
                s = net.addSwitch(switchName, cls=OVSSwitch,
                        failMode='standalone')
            link = net.addLink(s, net.get('s'+str(sw)), cls=TCLink, **hs1000)

    info( '*** Add hosts\n')
    for sw in topo_access:
        for i in range1(*topo_access[sw]):
            hostName = 'h'+str(i)
            h = None
            try:
                h = net.get(hostName)
            except KeyError:
                h = net.addHost(hostName, defaultRoute=None, ip='10.0.{0}.2/24'.format(topo_subnet_back[i]))
            link = net.addLink(h, net.get('s'+str(sw)), cls=TCLink, **hs100)

    core_switches = topo_core.keys()
    core_switches.sort()

    i = 0
    while i < len(core_switches)-1:
        net.addLink(net.get('s'+str(core_switches[i])), net.get('s'+str(core_switches[i+1])), cls=TCLink, **hs1000)
        i += 1

    info( '*** Starting network\n')
    net.build()

    for sub in topo_subnet:
        count = 1
        for l in topo_subnet[sub]:
            for i in range1(*l):
                hostName = 'h'+str(i)
                h = net.get(hostName)
                h.setIP('10.0.{0}.{1}/24'.format(sub, count))
                count += 1

    topo = printTopoDS(net, switches)

    for host in net.hosts:
        if 'mirror' in str(host) or 's1' in str(host):
            continue
        mac = '00:00:00:00:00:'+hex(int(str(host)[1:]))[2:].zfill(2)
        host.setMAC(mac)

    info( '*** Starting switches\n')

    for switch in net.switches:
        if str(switch) in switches:
            info('*** switch connected to controller ',switch,'\n')
            switch.start([c0])
            os.system('sudo ovs-vsctl set bridge \"'+str(switch)+'\" protocols=OpenFlow13')
        else:
            switch.start([])

    info( '*** Post configure switches and hosts\n')

    for sub in topo_subnet:
        count = 251
        for l in topo_subnet[sub]:
            for i in range1(*l):
                hostName = 'h'+str(i)
                h = net.get(hostName)
                h.cmd('sudo route add default gw 10.0.{0}.{1} h{2}-eth0'.format(sub,count,i))
                if len(switches) != 0:
                    h.cmd('sudo ip route del 10.0.{0}.0/24 table main'.format(sub,i))

    #configure VLANs
    vlans = [1,1,2,2,3,3,4,4]
    c = 0
    for i in range1(26,65):
        sw = net.get('s'+str(i))
        for inf in sw.intfs:
            intf = sw.intfs[inf]
            if 'lo' in str(intf):
                continue
            os.system('sudo ovs-vsctl del-port {0} {1}'.format(str(sw),intf))
            os.system('sudo ovs-vsctl add-port {0} {1} tag={2}'.format(str(sw),intf,vlans[c]))
            if str(sw) in str(intf.link.intf1):
                sw1 = str(intf.link.intf2).split('-')[0]
                os.system('sudo ovs-vsctl del-port {0} {1}'.format(sw1,intf.link.intf2))
                os.system('sudo ovs-vsctl add-port {0} {1} tag={2}'.format(sw1,intf.link.intf2,vlans[c]))
        c = (c+1)%8

    #configure trunk
    for s in topo_vlan_back:
        sw = net.get('s'+str(s))
        for inf in sw.intfs:
            intf = sw.intfs[inf]
            if 'lo' in str(intf):
                continue
            if str(sw) in str(intf.link.intf1):
                os.system('sudo ovs-vsctl del-port {0} {1}'.format(str(sw),intf))
                os.system('sudo ovs-vsctl add-port {0} {1} trunks={2}'.format(str(sw),intf,','.join(map(str,topo_vlan_back[s]))))
                sw1 = str(intf.link.intf2).split('-')[0]
                os.system('sudo ovs-vsctl del-port {0} {1}'.format(sw1,intf.link.intf2))
                os.system('sudo ovs-vsctl add-port {0} {1} trunks={2}'.format(sw1,intf.link.intf2,','.join(map(str,topo_vlan_back[s]))))

    # generateFlows(net,topo,switches)

def startTG(net):
    'Traffic generation'

    hosts = [[1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40],
            [41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]]
    flag = 0

    for i in range(len(hosts[0])):
        flag ^= 1

        serv = net.get('h'+str(hosts[flag][i]))
        cli  = net.get('h'+str(hosts[flag^1][i]))

        print cli,cli.IP(),'->',serv,serv.IP()

        serv.cmd('ping -c1 {0}'.format(cli.IP()))

        serv.cmd('ITGRecv &')
        cli.cmd('sleep 2 && ITGSend -T UDP -a '+serv.IP()+' -t 120000 -C 2560 -c 4096 -l $HOME/prabodh/stat/send{0}.log -x $HOME/prabodh/stat/recv{0}.log &'.format(str(serv)))
        # cli.cmd('sleep 2 && ITGSend -T UDP -a '+serv.IP()+' -z 12648 -Fs ps -Ft idts -l $HOME/prabodh/stat/send{0}.log -x $HOME/prabodh/stat/recv{0}.log &'.format(str(serv)))

if __name__ == '__main__':

    TOPO_FILE = 'topo_tree_adj_list'
    FLOW_FILE = 'flow.sh'

    parser = argparse.ArgumentParser(description='Run a mininet simulation for tree topology')
    parser.add_argument('-c', '--cli', help='Display CLI on given topology.', action='store_true')
    parser.add_argument('-s', '--switches', help='''Names of switches to have
                        SDN. Switches are numbered in level-order of a tree
                        starting from 1. Enter a space seperated list''',
                        nargs='*', default={}, type=str)
    parser.add_argument('-t', '--stats', help='Start TCPdump on all switch interfaces for stats collection purpose', action='store_true')

    args = parser.parse_args()

    if args.cli:
        setLogLevel( 'info' )

    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
    treeNet(net, set(args.switches))

    os.system('sh vlan.sh')
    os.system('bash clear.sh')
    if len(args.switches) != 0:
        os.system('bash conff')

    if args.stats:
        for switch in net.switches:
            for i in switch.intfs:
                switch.cmd('tcpdump -s 58 -B 65536 -nS -XX -i {0} net 10.0.0.0/16 -w $HOME/prabodh/stat/{0} &'.format(str(switch.intfs[i])))
        for i in range(1,6):
            for j in range(1,5):
                os.system('tcpdump -s 58 -B 65536 -nS -XX -i vlan{0}{1} net 10.0.0.0/16 -w $HOME/prabodh/stat/vlan{0}{1} &'.format(j,i))

    os.system('sh flow.sh')

    if args.cli:
        CLI(net)
        net.stop()
        exit(0)

    print "Testing",','.join(args.switches)

    print net.get('s1').cmdPrint('ip rule list')

    # net.pingAll()

    setLogLevel( 'warning' )
    k = ','.join([] if args.switches == {} else args.switches)
    startTG(net)

    # poll for iperfs to die
    time.sleep(10)
    while True:
        ps = os.popen('ps -a').read()
        if 'ITGSend' not in ps:
            os.system('sleep 2 && pkill ITGRecv')
        if 'ITG' not in ps:
            break

    net.stop()

    exit(0)

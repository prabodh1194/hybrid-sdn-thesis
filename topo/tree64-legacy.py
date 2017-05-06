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

topo_vlan = {1:[5,9,13,17],2:[6,10,14,18],3:[7,12,15,19],4:[8,12,16,20]}

topo_vlan_back = {}
for vlan in topo_vlan:
    for i in topo_vlan[vlan]:
        topo_vlan_back[i] = topo_vlan_back.get(i,[]) + [vlan]

topo_core = {1:[5,8],2:[9,12],3:[13,16],4:[17,20]}
topo_distro = {5:[21,22],6:[23,24],7:[25,26],8:[27,28],9:[29,30],10:[31,32],11:[33,34],12:[35,36],13:[37,38],14:[39,40],15:[41,42],16:[43,44],17:[45,46],18:[47,48],19:[49,50],20:[51,52]}
topo_access = {21: [1, 2], 22: [3, 4], 23: [5, 6], 24: [7, 8], 25: [9, 10], 26:
        [11, 12], 27: [13, 14], 28: [15, 16], 29: [17, 18], 30: [19, 20], 31:
        [21, 22], 32: [23, 24], 33: [25, 26], 34: [27, 28], 35: [29, 30], 36:
        [31, 32], 37: [33, 34], 38: [35, 36], 39: [37, 38], 40: [39, 40], 41:
        [41, 42], 42: [43, 44], 43: [45, 46], 44: [47, 48], 45: [49, 50], 46:
        [51, 52], 47: [53, 54], 48: [55, 56], 49: [57, 58], 50: [59, 60], 51:
        [61, 62], 52: [63, 64]}
topo_subnet = {1:[[1,4],[17,20],[33,36],[49,52]],2:[[5,8],[21,24],[37,40],[53,56]],3:[[9,12],[25,28],[41,44],[57,60]],4:[[13,16],[29,32],[45,48],[61,64]]}

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

def generateFlows(net,topo,switches):

    subs = topo_subnet.keys()
    sdn_switch = [int(s[1:]) for s in switches]
    sdn_switch.sort()
    flow = 'sudo ovs-ofctl -O OpenFlow13 add-flow {0} ip,nw_dst={1},priority={2}{3},actions=set_field:{4}"->"eth_dst,mod_vlan_vid:{5},{6}'

    flows = {}
    f = open("flows","w")
    stdout = sys.stdout
    sys.stdout = open(FLOW_FILE, 'w+')
    if len(switches) == 0:
        return

    for i in subs:
        sw_i = i+1
        for j in subs:
            sw_j = j+1

            if i == j:
                if sw_i in sdn_switch:
                    hosts = topo_subnet[i]
                    for l in hosts:
                        for h in range1(*l):
                            host = 'h'+str(h)
                            intf = topo[topo[host][0]][1]
                            print flow.format('s'+str(sw_i),topo[host][2],3,',in_port='+intf,net.get(host).MAC(),topo[host][2].split('.')[2],'set_field:{0}"->"eth_src,IN_PORT'.format(net.get('s'+str(sw_i)).intfs[int(intf)].MAC()))
                            print flow.format('s'+str(sw_i),topo[host][2],2,'',net.get(host).MAC(),topo[host][2].split('.')[2],'set_field:{0}"->"eth_src,output:{1}'.format(net.get('s'+str(sw_i)).intfs[int(intf)].MAC(),intf))
                else:
                    switch = str(close(sw_i, sdn_switch))
                    flows[str(i)+'-'+str(j)] = switch
                    router = topo['s'+switch]
                    print flow.format('s'+switch,'10.0.{0}.1/24'.format(i),2,',in_port=1',net.get(router[0]).intfs[int(router[1])-1].MAC(),i,'IN_PORT')
            else:
                if sw_i not in sdn_switch and sw_j not in sdn_switch:
                    switch = str(close(sw_i, sdn_switch))
                    flows[str(i)+'-'+str(j)] = switch
                    router = topo['s'+switch]
                    print flow.format('s'+switch,'10.0.{0}.1/24'.format(i),2,',in_port=1',net.get(router[0]).intfs[int(router[1])-1].MAC(),i,'IN_PORT')

    print '>&2 printf "%.2f%%\r" ',(100.0*1/100)
    print '>&2 echo'
    sys.stdout = stdout

    json.dump(flows, f)
    f.close()

    f = open("pbr.sh","w")
    f.write("""
ip rule del table local
ip rule add pref 32765 table local
ip rule add to 10.0.1.1 pref 0 table local
ip rule add to 10.0.2.1 pref 0 table local
ip rule add to 10.0.3.1 pref 0 table local
ip rule add to 10.0.4.1 pref 0 table local
""")

    # policies are written such that, packets meant for one particular intf are
    # written on that table
    # e.g., outs for intf s1-eth1 are written to table 2.
    for dist in topo_core:
        fanout = len(range1(*topo_core[dist]))
        for i in range(fanout): # table - intf
            for j in range(fanout): # subnet
                f.write('ip route add 10.0.{0}.0/24 table {1} proto kernel scope link dev s{2}-eth{3}\n'.format(j+1,i+2,dist,i+1))

    for fl in flows:
        sub_src = fl.split('-')[0]
        sub_dst = fl.split('-')[1]
        sw_src = int(sub_src)+1
        sw_dst = int(sub_dst)+1
        sub_src = '10.0.{0}.0/24'.format(sub_src)
        sub_dst = '10.0.{0}.0/24'.format(sub_dst)
        intf = flows[fl]

        if sw_src not in switches and sw_dst not in switches:
            f.write('ip rule add to {0} from {1} dev s1-eth{2} pref 1 table {3}\n'.format(sub_dst,sub_src,sub_src.split('.')[2],intf))

    f.close()

    os.system('cat pbr.sh')
    # net.get('s1').cmd('sh pbr.sh')

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
        count = 250
        for l in topo_subnet[sub]:
            count += 1
            for i in range1(*l):
                hostName = 'h'+str(i)
                h = net.get(hostName)
                h.cmd('sudo route add default gw 10.0.{0}.{1} h{2}-eth0'.format(sub,count,i))
                if len(switches) != 0:
                    h.cmd('sudo ip route del 10.0.{0}.0/24 table main'.format(sub,i))

    #configure VLANs
    vlans = [1,1,2,2,3,3,4,4]
    c = 0
    for i in range1(21,52):
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
                os.system('sudo ovs-vsctl add-port {0} {1} trunks={2}{3}'.format(str(sw),intf,','.join(map(str,topo_vlan_back[s])),',5' if str(sw) in switches else ''))
                sw1 = str(intf.link.intf2).split('-')[0]
                os.system('sudo ovs-vsctl del-port {0} {1}'.format(sw1,intf.link.intf2))
                os.system('sudo ovs-vsctl add-port {0} {1} trunks={2}{3}'.format(sw1,intf.link.intf2,','.join(map(str,topo_vlan_back[s])),',5' if str(sw) in switches else ''))

    # generateFlows(net,topo,switches)

def startTG(net):
    'Traffic generation'

    hosts = [[1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],
            [33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64]]
    flag = 0

    for i in range(len(hosts[0])):
        flag ^= 1

        serv = net.get('h'+str(hosts[flag][i]))
        cli  = net.get('h'+str(hosts[flag^1][i]))

        print cli,'->',serv

        serv.cmd('ITGRecv &')
        cli.cmd('sleep 2 && ITGSend -T UDP -a '+serv.IP()+' -t 10000 -C 2560 -c 4096 -l $HOME/prabodh/stat/send{0}.log -x $HOME/prabodh/stat/recv{0}.log &'.format(str(serv)))
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
    os.system('bash route.sh')

    if args.stats:
        for switch in net.switches:
            for i in switch.intfs:
                switch.cmd('tcpdump -s 54 -B 102400 -nS -XX -i {0} net 10.0.0.0/16 -w $HOME/prabodh/stat/{0} &'.format(str(switch.intfs[i])))
        for i in range(1,6):
            for j in range(1,5):
                os.system('tcpdump -s 54 -B 102400 -nS -XX -i vlan{0}{1} net 10.0.0.0/16 -w $HOME/prabodh/stat/vlan{0}{1} &'.format(j,i))

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

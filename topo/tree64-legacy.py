#!/usr/bin/python

"""
Taken from examples/tree1024.py
Create a 64-host network on legacy switch, and run the CLI on it.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import OVSKernelSwitch, OVSSwitch, Host, Node
from mininet.topolib import TreeNet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from math import ceil
import os,sys,argparse,re,time,pprint,json

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
    flows = {}
    f = open("flows","w")
    stdout = sys.stdout
    sys.stdout = open(FLOW_FILE, 'w+')
    if len(switches) == 0:
        return
    # 2 -- output:_ / IN_PORT
    # 3 -- switch
    sdn_switch = [int(s[1:]) for s in switches if int(s[1:]) in range(2,2+fanout)]
    sdn_switch.sort()
    printCount = 0
    printTotal = numHosts*(numHosts-1.0)

    flow = 'sudo ovs-ofctl -O OpenFlow13 add-flow {0} ip,nw_src={1},dl_dst={2},actions=set_field:{3}"->"eth_dst,set_field:{4}"->"eth_src,{5}'
    mm = '00:00:00:00:00:'
    fm = '10:00:00:00:00:'
    for i in range(0,numHosts):
        print
        for j in range(i,numHosts):

            if i == j:
                continue

            h_src = 'h'+str(i+1)
            h_dst = 'h'+str(j+1)
            eth_dst = ''
            #print '>&2 echo \'',h_src,h_dst,'\''
            s = topo[topo[h_dst][0]] # distro layer switch for the dst

            #find a candidate OF switch to install a flow
            if topo[topo[h_src][0]][0] in switches: # src host is connected to an OF switch
                switch = topo[topo[h_src][0]][0]
            elif s[0] in switches: # dst host is connected to an OF switch
                switch = s[0]
            else: # neither src nor dst are on OF switches; greedily select a switch closest of two options
                s_no = int(s[0][1:])
                switch = close(s_no, sdn_switch)
                # switch = 's'+str(switch[0] if abs(switch[0]-s_no) <= abs(switch[1]-s_no) else switch[1])
                switch = 's'+str(switch)
                flows[h_src+"-"+h_dst] = switch

            # determine a port number on which the flow outputs the packet after
            # processing
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

            if switch == s[0]:
                eth_dst = mm+hex(j+1)[2:].zfill(2)
            else:
                parent_intf = int(topo[switch][1])
                eth_dst = net.get('s1').intfs[parent_intf-1].MAC()
                net.get('s1').cmd('arp -i {0} -s {1} {2}'.format('s1-eth'+str(parent_intf), net.get(h_dst).IP(), fm+hex(j+1)[2:].zfill(2)))

            print '#'+switch,h_src,'->',h_dst
            # 'sudo ovs-ofctl -O OpenFlow13 add-flow {0} ip,nw_src={1},dl_dst={2},actions=set_field:{3}"->"eth_dst,set_field:{4}"->"eth_src,{5}'
            flowadd = flow.format(switch,net.get(h_src).IP(),fm+hex(j+1)[2:].zfill(2),eth_dst,fm+hex(i+1)[2:].zfill(2),port)
            print flowadd

            h_src, h_dst = h_dst, h_src
            eth_dst = ''
            # print '>&2 echo \'',h_src,h_dst,'\''
            s = topo[topo[h_dst][0]] # distro layer switch

            if topo[topo[h_src][0]][0] in switches: # src host is connected to an OF switch
                switch = topo[topo[h_src][0]][0]

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

            if switch == s[0]:
                eth_dst = mm+hex(i+1)[2:].zfill(2)
            else:
                parent_intf = int(topo[switch][1])
                eth_dst = net.get('s1').intfs[parent_intf-1].MAC()
                net.get('s1').cmd('arp -i {0} -s {1} {2}'.format('s1-eth'+str(parent_intf), net.get(h_dst).IP(), fm+hex(i+1)[2:].zfill(2)))

            print '#'+switch,h_src,'->',h_dst
            flowadd = flow.format(switch,net.get(h_src).IP(),fm+hex(i+1)[2:].zfill(2),eth_dst,fm+hex(j+1)[2:].zfill(2),port)
            print flowadd

            printCount += 2
            print '>&2 printf "%.2f%%\r" ',(100.0*printCount/printTotal)

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
    for i in range(fanout): # table - intf
        for j in range(fanout): # subnet
            f.write('ip route add 10.0.{0}.0/24 table {1} proto kernel scope link dev s1-eth{2}\n'.format(j+1,i+2,i+1))

    subnets = {}

    for fl in flows:
        h_src = fl.split('-')[0]
        h_dst = fl.split('-')[1]
        sub_src = net.get(h_src).IP()
        sub_src = sub_src[:sub_src.rfind('.')]+".0/24"
        sub_dst = net.get(h_dst).IP()
        sub_dst = sub_dst[:sub_dst.rfind('.')]+".0/24"
        sw_src = topo[topo[h_src][0]][0]
        sw_dst = topo[topo[h_dst][0]][0]
        k = sub_src+"-"+sub_dst
        intf = flows[fl][1:]

        if sw_src not in switches and sw_dst not in switches and k not in subnets:
            f.write('ip rule add to {0} from {1} dev s1-eth{2} pref 1 table {3}\n'.format(sub_dst,sub_src,sub_src.split('.')[2],intf))

            if sub_src != sub_dst:
                f.write('ip rule add to {0} from {1} dev s1-eth{2} pref 1 table {3}\n'.format(sub_src,sub_dst,sub_dst.split('.')[2],intf))
            subnets[k] = 1

    f.close()

    os.system('cat pbr.sh')
    net.get('s1').cmd('sh pbr.sh')

def printTopoDS(net,switches):
    topo = {}
    pattern = "eth([0-9]+)"
    for l in net.links:

        if 'mirror' in str(l):
            continue
        i1 = str(l.intf1.node)
        i2 = str(l.intf2.node)
        topo[i1] = (i2,re.search(pattern,str(l.intf2)).group(1))

    stdout = sys.stdout
    sys.stdout = open(TOPO_FILE, 'w+')
    print json.dumps(topo)
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

    router = net.addHost( 's1', cls=LinuxRouter, ip='10.0.1.1/24')

    switchCount = 2
    hs100 = {'bw':100,'delay':'10ms'} #Mbit/s
    hs1000 = {'bw':1000,'delay':'10ms'} #Mbit/s
    mirrors = []
    for i in range (1, depth):
        level = pow(fanout, i)
        for j in range(level):
            switchName = 's'+str(switchCount)
            s = net.addSwitch(switchName,
                    cls=OVSKernelSwitch,
                    failMode='secure' if switchName in switches else 'standalone')

            # add a mirror port for logging purpose
            # if mirror:
            #     h = net.addHost('hmirror'+str(switchCount), cls=Host, ip='10.0.0.'+str(255-switchCount), defaultRoute=None)
            #     net.addLink(s, h, cls=TCLink, **hs100)

            if i == 1:
                link=net.addLink(s, net.get('s1'),cls=TCLink, **hs1000)
                link.intf2.setIP('10.0.{0}.1/24'.format(switchCount-1))

            if i > 1:
                prevSwitch = switchCount - j - level/fanout + j/fanout
                l = net.addLink(s, net.get('s'+str(prevSwitch)), cls=TCLink, **hs100)

            switchCount += 1

    for i in range(fanout-1,-1,-1):
        router.intfs[i].rename('s1-eth{0}'.format(i+1))

    info( '*** Add hosts\n')
    numHosts = pow(fanout, depth)
    switchOff = 1+(pow(fanout, depth-1)-1)/(fanout-1)
    division = numHosts/fanout #number of hosts under a distro switch
    for i in range(numHosts):
        h = net.addHost('h'+str(i+1),
                ip='10.0.{0}.{1}/24'.format(int(ceil((i+1.)/division)),str(i+2)),
                defaultRoute=None)
        net.addLink(h, net.get('s'+str(switchOff+i/fanout)), cls=TCLink, **hs100)

    info( '*** Starting network\n')
    net.build()

    topo = printTopoDS(net, switches)

    for host in net.hosts:

        if 'mirror' in str(host) or 's1' in str(host):
            continue
        mac = '00:00:00:00:00:'+hex(int(str(host)[1:]))[2:].zfill(2)
        host.setMAC(mac)
        switch = topo[topo[str(host)][0]][0] # distro switch
        for host2 in net.hosts:
            if 'mirror' in str(host2) or 's1' in str(host2):
                continue
            if str(host) == str(host2):
                continue
            if host.IP()[5] != host2.IP()[5]:
                continue
            if switch in switches:
                mac = '10:00:00:00:00:'+hex(int(str(host2)[1:]))[2:].zfill(2)
            else:
                parent_intf = int(topo[switch][1])
                mac = net.get('s1').intfs[parent_intf-1].MAC()

            if len(switches) != 0:
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

    # add routes
    for host in net.hosts:
        if str(host) == 's1' or 'mirror' in str(host):
            continue
        else:
            i = int(str(host)[1:])
            host.cmd('route add default gw 10.0.{0}.1 h{1}-eth0'.format(int(ceil((i+0.)/division)),i))

    generateFlows(topo,switches,fanout,numHosts)

    return numHosts

def startIperf(net,name):
    hosts = []
    mirrors = []

    for h in net.hosts:
        if 's1' in str(h):
            continue
        if 'mirror' in str(h):
            mirrors += [h]
        else:
            hosts += [h]

    num_hosts = len(hosts)
    res = {}

    for i in range(num_hosts/2):
        h1 = hosts[i]
        h2 = hosts[i+num_hosts/2]
        # h1.cmd('/usr/local/bin/iperf3 -1 -s -f M > ../../../stat/servout'+name+str(h1)+' &')
        h1.cmd('ITGRecv &')

        # Can not record client side data too
        # h2.cmd('sleep 2 && ITGSend -T UDP -a '+h1.IP()+' -t 10000 -C 2560 -c 2048 -l ../../../stat/send{0}.log -x ../../../stat/recv{0}.log &'.format(str(h1)))
        h2.cmd('sleep 2 && cd ../../../pcap1/{1}_ditg_files/ && sudo ITGSend {1}.ditg -l ../../stat/send{0}.log -x ../../../stat/recv{0}.log && cd - &'.format(str(h1),h1.IP()))

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
    parser.add_argument('-t', '--stats', help='Start TCPdump on all switch interfaces for stats collection purpose', action='store_true')

    global mirror
    args = parser.parse_args()
    mirror = args.mirrors

    info('*** building a tree of depth',args.depth[0],'and fanout',args.fanout[0],'\n')

    switchCount = (pow(args.fanout[0],args.depth[0])-1)/(args.fanout[0]-1)

    if args.cli:
        setLogLevel( 'info' )

    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')
    hostCount = treeNet(net, args.depth[0], args.fanout[0], set(args.switches))

    if args.mirrors:
        setMirrors(switchCount, args.fanout[0])

    print args.stats
    if args.stats:
        for switch in net.switches:
            for i in switch.intfs:
                switch.cmd('tcpdump -s 50 -B 65536 -nS -XX -i {0} net 10.0.0.0/16 -w ../../../stat/{0} &'.format(str(switch.intfs[i])))
        router = net.get('s1')

        for i in router.intfs:
            router.cmd('tcpdump -s 50 -B 65536 -nS -XX -i {0} net 10.0.0.0/16 -w ../../../stat/{0} &'.format(str(router.intfs[i])))
        # for host in net.hosts:
        #     host.cmd('tcpdump src {1} or dst {1} and udp -w ../../../stat/{0} &'.format(str(host),host.IP()))

    os.system('sh flow.sh')

    if args.cli:
        CLI(net)
        net.stop()
        exit(0)

    print "Testing",','.join(args.switches)

    print net.get('s1').cmdPrint('ip rule list')

    # net.pingAll()

    setLogLevel( 'warning' )
    k = ','.join([str(a) for a in args.depth]+[str(b) for b in args.fanout]+[] if args.switches == {} else args.switches)
    startIperf(net,k)

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

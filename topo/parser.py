import sys, os, re, pprint, json
from math import ceil

def min(a,b):
    return a if a<b else b

pattern = "([0-9:.]+) IP ([0-9:.]+) > ([0-9:.]+):.*length ([0-9:.]+)"

flag = -1

src = ''
seconds = 0
min_seconds = 86400000
packet = ''
header = sys.argv[1]

d = {}
files = os.popen('ls -1 $HOME/prabodh/stat | grep "s[0-9]\+-"').read()[:-1]
files = files.split('\n')

print >>sys.stderr, files

for tcp_file in files:
    f = open(os.path.expanduser('~')+'/prabodh/stat/'+tcp_file, 'r')
    print >>sys.stderr, tcp_file
    tcp_file = tcp_file[1:]

    for line in f:

        if 'UDP' in line:
            flag = 2
            m = re.search(pattern,line)
            t = re.split('[:.]',m.group(1))
            t = map(float,t)

            src = '.'.join(m.group(2).split('.')[2:4])
            size = int(m.group(4))

            #milli
            seconds = t[0]*60*60*1000 + t[1]*60*1000 + t[2]*1000 + t[3]/1000.0
            min_seconds = min(min_seconds,seconds)
            # print m.group(1),seconds,src
            continue

        if flag:
            flag -= 1
            continue

        if flag == 0:
            flag -= 1
            packet = line[15:19]
            # print line[14:18]

            if packet not in d:
                d[packet] = {src:{tcp_file:[(seconds,size)]}}
            else:
                if src not in d[packet]:
                     d[packet][src] = {tcp_file:[(seconds,size)]}
                else:
                    d[packet][src][tcp_file] = d[packet][src].get(tcp_file,[]) + [(seconds,size)]

for packet in d: # go through every recorded packet
    for host in d[packet]: # for every packet, go through every host
        for intf in d[packet][host]:
            z = []
            for i in d[packet][host][intf]:
                z += [(i[0]-min_seconds,i[1])]
            d[packet][host][intf] = z

# pprint.pprint(d)
TOPO_FILE = 'topo_tree_adj_list'
FLOW_FILE = 'flows'

f = open(TOPO_FILE)
topo = json.load(f)

flows = {}
f = open(FLOW_FILE)
try:
    flows = json.load(f)
except:
    flows = {}

traversal = {}
hosts = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        [17,18,19,20,21,22,23,24,25, 26, 27, 28, 29, 30, 31, 32]]
flag = 0
delay = "Average delay += +([0-9.]+) s"
bitrate = "Average bitrate += +([0-9.]+) Kbit"
host_ee = {}

for i in range(len(hosts[0])):
    flag ^= 1
    cli = hosts[flag^1][i]
    serv = hosts[flag][i]

    k = 'h'+str(cli)
    cli_k = '.'.join(topo[k][2].split('.')[2:])

    #construct traversal
    if cli_k not in traversal:
        traversal[cli_k] = []

    while True:
        if k not in topo:
            break
        traversal[cli_k] += ['{0}-eth{1}'.format(str(topo[k][0]),str(topo[k][1]))]
        if topo[k][0] != 's1':
            traversal[cli_k] += ['{0}-eth1'.format(str(topo[k][0]))]
        k = topo[k][0]

    k = str(topo['h'+str(cli)][2].split('.')[2])+'-'+str(topo['h'+str(serv)][2].split('.')[2])
    if k in flows:
        flow_sw = 's'+flows[k]
        traversal[cli_k] += ['s1-eth{0}'.format(str(topo[flow_sw][1])),'{0}-eth1'.format(flow_sw),'{0}-eth1'.format(flow_sw),'s1-eth{0}'.format(str(topo[flow_sw][1]))]

    k = 'h'+str(serv)
    idx = len(traversal[cli_k])

    while True:
        if k not in topo:
            break
        traversal[cli_k].insert(idx,'{0}-eth{1}'.format(str(topo[k][0]),str(topo[k][1])))
        if topo[k][0] != 's1':
            traversal[cli_k].insert(idx,'{0}-eth1'.format(str(topo[k][0])))
        k = topo[k][0]

    #construct end-to-end latency
    k = 'h'+str(serv)
    ITG = os.popen('ITGDec $HOME/prabodh/stat/recv{0}.log|tail -15|grep -i average'.format(k)).read()
    delay_s = float(re.search(delay, ITG).group(1))*1000
    bitrate_mBps = float(re.search(bitrate, ITG).group(1))/(8*1024)
    host_ee[k] = {'delay':delay_s,'bitrate':bitrate_mBps}

print >> sys.stderr, pprint.pformat(traversal)

drop_file = open(os.path.expanduser('~')+'/prabodh/stat/drop','a')

totalDrop = 0
drop = {'totalDrop':0}
link_speed = {}
link_util  = {}
link_bw = {}
latency = {}

for packet in d: # go through every recorded packet
    for host in d[packet]: # for every packet, go through every host
        for i in range(0,len(traversal[host]),2): # for a host, go through all interfaces in order
            intf = traversal[host][i]
            eth1 = traversal[host][i+1]
            if intf in d[packet][host] and eth1 not in d[packet][host]:
                # print >> drop_file,intf,packet,host
                drop['totalDrop'] += 1
                if eth1.split('-')[0] not in drop:
                    drop[eth1.split('-')[0]] = 1
                else:
                    drop[eth1.split('-')[0]] += 1
                break
            else:
                sw = intf[1:intf.find('-')]

                if sw not in latency:
                    latency[sw] = {'latency':0,'packets':0}

                latency[sw]['packets'] += 1
                if eth1 == intf:
                    try:
                        latency[sw]['latency'] += (d[packet][host][eth1][1][0] - d[packet][host][intf][0][0])
                    except:
                        latency[sw]['packets'] -= 1
                else:
                    latency[sw]['latency'] += (d[packet][host][eth1][0][0] - d[packet][host][intf][0][0])

                if i-1 >= 0:
                    p1 = d[packet][host][intf].pop(0)
                    p2 = d[packet][host][traversal[host][i-1]].pop(0)
                    link = traversal[host][i-1]+":"+intf

                    if link not in link_speed:
                        link_speed[link] = {}
                    second = str(int(ceil(p2[0]/1000)))

                    if second not in link_speed[link]:
                        link_speed[link][second] = []
                    link_speed[link][second] += [(p1[0] - p2[0],p1[1])]

for sw in latency:
    latency[sw] = latency[sw]['latency']/latency[sw]['packets']

for link in link_speed:
    link_util[link] = 0
    link_bw[link] = {}
    bw = 0
    for second in link_speed[link]:
        link_util[link] += (len(link_speed[link][second]))
        link_bw[link][second] = 0
        for t in link_speed[link][second]:
            link_bw[link][second] += t[1]
        link_bw[link][second] /= (1024*1024.)
        bw += link_bw[link][second]
    # link_bw[link] = bw/len(link_speed[link])

for link in link_speed:
    link_speed[link] = (link_util[link],link_bw[link])

stdout = sys.stdout
sys.stdout = drop_file
print header
pprint.pprint(drop)
# pprint.pprint(link_util)
# pprint.pprint(link_bw)
pprint.pprint(link_speed)
pprint.pprint(latency)
pprint.pprint(host_ee)
sys.stdout = stdout

for packet in d: # go through every recorded packet
    for host in d[packet]: # for every packet, go through every host
        for k in d[packet][host]:
            if k not in traversal[host]:
                d[packet][host][k] = 0

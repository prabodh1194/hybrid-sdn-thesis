import sys, os, re, pprint, json
from math import ceil

pattern = "([0-9:.]+) IP ([0-9:.]+) > ([0-9:.]+):"

flag = -1

src = ''
dst = ''
seconds = ''
packet = ''
header = sys.argv[3]

d = {}
files = os.popen('ls -1 ../../../stat | grep "s[0-9]\+-"').read()[:-1]
files = files.split('\n')

print >>sys.stderr, files

for tcp_file in files:
    f = open('../../../stat/'+tcp_file, 'r')
    print >>sys.stderr, tcp_file
    tcp_file = tcp_file[1:]

    for line in f:

        if 'UDP' in line:
            flag = 2
            m = re.search(pattern,line)
            t = re.split('[:.]',m.group(1))
            t = map(float,t)

            src = m.group(2).split('.')[3]
            dst = m.group(3)

            #milli
            seconds = t[0]*60*60*1000 + t[1]*60*1000 + t[2]*1000 + t[3]/1000.0
            # print m.group(1),seconds,src,dst
            continue

        if flag:
            flag -= 1
            continue

        if flag == 0:
            flag -= 1
            packet = line[15:19]
            # print line[14:18]

            if packet not in d:
                d[packet] = {src:{tcp_file:[seconds]}}
            else:
                if src not in d[packet]:
                     d[packet][src] = {tcp_file:[seconds]}
                else:
                    d[packet][src][tcp_file] = d[packet][src].get(tcp_file,[]) + [seconds]


TOPO_FILE = 'topo_tree_adj_list'
FLOW_FILE = 'flows'

f = open(TOPO_FILE)
topo = json.load(f)

f = open(FLOW_FILE)
flows = json.load(f)

depth = int(sys.argv[1])
fanout = int(sys.argv[2])
hosts = pow(fanout, depth)

traversal = {}

for i in range(1+hosts/2,hosts+1):
    if i not in traversal:
        traversal[str(i)] = []

    k = 'h'+str(i)
    while True:
        if k not in topo:
            break
        traversal[str(i)] += ['{0}-eth{1}'.format(str(topo[k][0]),str(topo[k][1]))]
        if topo[k][0] != 's1':
            traversal[str(i)] += ['{0}-eth1'.format(str(topo[k][0]))]
        k = topo[k][0]

    k = 'h'+str(i-hosts/2)+"-"+'h'+str(i)
    if k in flows:
        flow_sw = str(flows[k])
        traversal[str(i)] += ['s1-eth{0}'.format(str(topo[flow_sw][1])),'{0}-eth1'.format(flow_sw),'{0}-eth1'.format(flow_sw),'s1-eth{0}'.format(str(topo[flow_sw][1]))]

    k = 'h'+str(i-hosts/2)
    idx = len(traversal[str(i)])

    while True:
        if k not in topo:
            break
        traversal[str (i)].insert(idx,'{0}-eth{1}'.format(str(topo[k][0]),str(topo[k][1])))
        if topo[k][0] != 's1':
            traversal[str (i)].insert(idx,'{0}-eth1'.format(str(topo[k][0])))
        k = topo[k][0]

print >> sys.stderr, traversal

drop_file = open('../../../stat/drop','a')

totalDrop = 0
drop = {'totalDrop':0}
link_speed = {}
link_latency = {}

for packet in d: # go through every recorded packet
    for host in d[packet]: # for every packet, go through every host
        for i in range(0,len(traversal[str(host)]),2): # for a host, go through all interfaces in order
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
                if i-1 >= 0:
                    link = traversal[host][i-1]+":"+intf

                    if link not in link_speed:
                        link_speed[link] = []
                    link_speed[link] += [d[packet][host][intf].pop(0) - d[packet][host][traversal[host][i-1]].pop(0)]

for link in link_speed:
    latency = sum(link_speed[link])/len(link_speed[link])
    link_latency[link] = (latency,(2./1024)/latency,len(link_speed[link]))

stdout = sys.stdout
sys.stdout = drop_file
print header
pprint.pprint(drop)
pprint.pprint(link_latency)
sys.stdout = stdout

for packet in d: # go through every recorded packet
    for host in d[packet]: # for every packet, go through every host
        for k in d[packet][host]:
            if k not in traversal[host]:
                d[packet][host][k] = 0

pprint.pprint(d)

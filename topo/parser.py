import sys, os, pdb, re, pprint, json
from math import ceil

pattern = "([0-9:.]+) IP ([0-9:.]+) > ([0-9:.]+):"

flag = -1

src = ''
dst = ''
seconds = ''
packet = ''

d = {}
files = os.popen('ls -1 ../../../stat | grep "s[0-9]-"').read()[:-1]
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
                d[packet] = {src:{tcp_file:seconds}}
            else:
                if src not in d[packet]:
                     d[packet][src] = {tcp_file:seconds}
                else:
                    d[packet][src][tcp_file] = seconds

# pprint.pprint(d)

TOPO_FILE = 'topo_tree_adj_list'

f = open(TOPO_FILE)
topo = json.load(f)

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
        k = topo[k][0]

    k = 'h'+str(i-hosts/2)
    idx = len(traversal[str (i)])

    while True:
        if k not in topo:
            break
        traversal[str (i)].insert(idx,'{0}-eth{1}'.format(str(topo[k][0]),str(topo[k][1])))
        k = topo[k][0]

print >> sys.stderr, traversal

drop = {}
link = {}

for packet in d:
    for host in d[packet]:
        for i in range(len(traversal[str(host)])):
            intf = traversal[host][i]
            if intf in d[packet][host]:
                eth1 = re.sub('eth[0-9]','eth1',intf)
                if eth1 not in d[packet][host]:
                    if eth1.split('-')[0] not in drop:
                        drop[eth1.split('-')[0]] = 1
                    else:
                        drop[eth1.split('-')[0]] += 1
            else:
                break

pprint.pprint(drop)

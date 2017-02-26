import sys, os, pdb, re, pprint

tcp_file = sys.argv[1]

f = open(tcp_file, 'r')

pattern = "([0-9:.]+) IP ([0-9:.]+) > ([0-9:.]+):"

flag = -1

d = {}

for line in f:

    if 'UDP' in line:
        flag = 3
        m = re.search(pattern,line)
        t = re.split('[:.]',m.group(1))
        t = map(float,t)

        s = t[0]*60*60*1000 + t[1]*60*1000 + t[2]*1000 + t[3]/1000.0
        # print m.group(1),s,m.group(2),m.group(3)
        continue

    if flag:
        flag -= 1
        continue

    if flag == 0:
        flag -= 1
        # print line[10:14]

        if line[10:14] not in d:
            d[line[10:14]] = [s,m.group(2),m.group(3)]
        else:
            d[line[10:14]] += [s,m.group(2),m.group(3)]

pprint.pprint(d)

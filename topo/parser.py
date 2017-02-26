import sys, os, pdb, re

tcp_file = sys.argv[1]

f = open(tcp_file, 'r')

pattern = "([0-9:.]+) IP ([0-9:.]+) > ([0-9:.]+):"

flag = -1

for line in f:

    if 'UDP' in line:
        flag = 3
        m = re.search(pattern,line)
        print m.group(1),m.group(2),m.group(3)
        continue

    if flag:
        flag -= 1
        continue

    if flag == 0:
        flag -= 1
        print line[10:14]

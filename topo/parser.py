import sys, os, pdb, re, pprint
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

    for line in f:

        if 'UDP' in line:
            flag = 2
            m = re.search(pattern,line)
            t = re.split('[:.]',m.group(1))
            t = map(float,t)

            src = m.group(2)
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

pprint.pprint(d)

# depth  = int(sys.argv[1])
# fanout = int(sys.argv[2])
# 
# hosts = pow(fanout, depth)
# switches = (pow(factor,depth)-1)/(fanout-1)
# 
# traversal = {}
# 
# for i in range(depth):
#     factor = float(pow(fanout,depth-1-i))
#     offset = pow(fanout,depth-i)
#     # pdb.set_trace()
#     for j in range(1+hosts/2,hosts+1):
#         h = j/offset
#         h = h*offset
#         h = j-h
# 
#         ceil(j/offset)
# 
#         if j not in traversal:
#             traversal[j] = []
#         traversal[j] = ['s{0}-eth{1}'.format(i+1,str(int(ceil(h/factor))+1 if i!=0 else 0))]+traversal[j]
# 
#         h = (j-hosts/2)/offset
#         h = h*offset
#         h = j-h-hosts/2
#         traversal[j] += ['s{0}-eth{1}'.format(i+1,str(int(ceil(h/factor))+1 if i!=0 else 0))]
# pprint.pprint(traversal)

traversal = {
 33: [],
 34: [],
 35: [],
 36: [],
 37: [],
 38: [],
 39: [],
 40: [],
 41: [],
 42: [],
 43: [],
 44: [],
 45: [],
 46: [],
 47: [],
 48: [],
 49: [],
 50: [],
 51: [],
 52: [],
 53: [],
 54: [],
 55: [],
 56: [],
 57: [],
 58: [],
 59: [],
 60: [],
 61: [],
 62: [],
 63: [],
 64: []}

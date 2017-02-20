#!/usr/bin/python
import os

f = open("res","w")

for i in range(4):
    for j in range(i,4):
        s = ''
        print i+2,j+2
        for k in range(i,j+1):
            s += 's'+str(k+2)+' '
        print s
        print >> f, os.popen('python tree64-legacy.py -d 3 -f 4 -s {0}'.format(s)).read()

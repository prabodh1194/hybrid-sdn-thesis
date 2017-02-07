#!/usr/bin/python
import os

for i in range(22):
    for j in range(i,21):
        s = ''
        print i,j
        for k in range(i,j+1):
            s += 's'+str(k+1)+' '
        print s
        print(os.popen('python tree64-legacy.py -d 3 -f 4 -s {0}'.format(s)).read())

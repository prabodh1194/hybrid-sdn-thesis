#!/usr/bin/python
import os

os.system('sudo mn -c')
f = open("res","w",buffering=0)

for i in range(4):
    for j in range(i,4):
        s = ''
        print i+2,j+2
        for k in range(i,j+1):
            s += 's'+str(k+2)+' '
        print s
        print >> f, os.popen('python tree64-legacy.py -t -d 3 -f 4 -s {0}'.format(s)).read()
        os.system('cd ../../../stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo tcpdump -qns 0 -X -r $var > s$var; rm $var; done')
        os.system('pwd')
        os.system('python parser.py 3 4 {0} >> ../../../stat/pack_info'.format(s.replace(' ',',')))
        os.system('cd ../../../stat/ && ls -1 | grep "recv" | while read var; do ITGDec $var | grep -i "from\|to\|drop"; echo; done >> drop')
        # os.system('cd ../../../stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo rm $var; done')

#!/usr/bin/python
import os

os.system('sudo mn -c')
f = open("res","w",buffering=0)

# combo = ['s2', 's3', 's4', 's5', 's2 s3', 's2 s4', 's2 s5', 's3 s4', 's3 s5', 's4 s5', 's2 s3 s4', 's2 s3 s5', 's2 s4 s5', 's3 s4 s5',  's2 s3 s4 s5']
s = 's2'
print s
print >> f, os.popen('python tree64-legacy.py -t -d 3 -f 4').read()
# print >> f, os.popen('python tree64-legacy.py -t -d 3 -f 4 -s {0}'.format(s)).read()
os.system('cd ../../../stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo tcpdump -qns 0 -X -r $var > s$var; rm -f $var; done')
os.system('pwd')
os.system('python parser.py 3 4 {0} >> ../../../stat/pack_info'.format(s.replace(' ',',')))
os.system('cd ../../../stat/ && ls -1 | grep "log" | while read var; do ITGDec $var | grep -i "from\|to\|drop"; echo; rm -vf $var; done >> drop')
os.system('cd ../../../stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo rm $var; done')

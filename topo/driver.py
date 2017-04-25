#!/usr/bin/python
import os

os.system('sudo mn -c')
f = open("res","w",buffering=0)

combo = ['s2', 's3', 's4', 's5', 's2 s3', 's2 s4', 's2 s5', 's3 s4', 's3 s5', 's4 s5', 's2 s3 s4', 's2 s3 s5', 's2 s4 s5', 's3 s4 s5',  's2 s3 s4 s5']

print >> f, os.popen('python tree64-legacy.py -t').read()
os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo tcpdump -qns 0 -X -r $var > s$var; rm $var; done')
os.system('pwd')
os.system('python parser.py {0} >> $HOME/prabodh/stat/pack_info'.format(','))
os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "log" | while read var; do sudo rm -vf $var; echo; done')
os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo rm $var; done')

for s in combo:
    os.system('sudo mn -c')
    os.system('sleep 10')
    print s
    os.system('python tree64-legacy.py -t -s {0}'.format(s))
    os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo tcpdump -qns 0 -X -r $var > s$var; rm $var; done')
    os.system('pwd')
    os.system('python parser.py {0} >> $HOME/prabodh/stat/pack_info'.format(s.replace(' ',',')))
    os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "log" | while read var; do sudo rm -vf $var; echo; done')
    os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "s[0-9]\+-" | while read var; do sudo rm $var; done')

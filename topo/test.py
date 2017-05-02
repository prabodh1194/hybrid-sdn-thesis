#!/usr/bin/python
import os

os.system('sudo mn -c')

combo = ['s5 s13']
# combo = [' ']

for s in combo:
    os.system('python tree64-legacy.py -t -s {0}'.format(s))
    os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "vlan\|s[0-9]\+-" | while read var; do sudo tcpdump -eqns 0 -X -r $var > s$var; rm -f $var; done')
    os.system('pwd')
    os.system('python parser.py {0} >> $HOME/prabodh/stat/pack_info'.format(s.replace(' ',',')))
    os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "log" | while read var; do rm -vf $var; done')
    os.system('cd $HOME/prabodh/stat/ && ls -1 | grep "vlan\|s[0-9]\+-" | while read var; do sudo rm $var; done')

#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s17 = net.addSwitch('s17', cls=OVSKernelSwitch, failMode='standalone')
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, failMode='standalone')
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch, failMode='standalone')
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch, failMode='standalone')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, failMode='standalone')
    s18 = net.addSwitch('s18', cls=OVSKernelSwitch, failMode='standalone')
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, failMode='standalone')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch, failMode='standalone')
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, failMode='standalone')
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, failMode='standalone')
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, failMode='standalone')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, failMode='standalone')
    s19 = net.addSwitch('s19', cls=OVSKernelSwitch, failMode='standalone')
    s20 = net.addSwitch('s20', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None)
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s5, s1)
    net.addLink(s6, s1)
    net.addLink(s7, s2)
    net.addLink(s8, s2)
    net.addLink(s5, s6)
    net.addLink(s7, s8)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s9, s3)
    net.addLink(s10, s3)
    net.addLink(s11, s4)
    net.addLink(s12, s4)
    net.addLink(s9, s10)
    net.addLink(s11, s12)
    net.addLink(s13, s5)
    net.addLink(s13, s6)
    net.addLink(s14, s5)
    net.addLink(s14, s6)
    net.addLink(s15, s7)
    net.addLink(s15, s8)
    net.addLink(s16, s7)
    net.addLink(s16, s8)
    net.addLink(s17, s9)
    net.addLink(s17, s10)
    net.addLink(s18, s9)
    net.addLink(s18, s10)
    net.addLink(s19, s11)
    net.addLink(s19, s12)
    net.addLink(s20, s11)
    net.addLink(s20, s12)
    net.addLink(h1, s13)
    net.addLink(h2, s13)
    net.addLink(h3, s14)
    net.addLink(h4, s14)
    net.addLink(h5, s15)
    net.addLink(h6, s15)
    net.addLink(h7, s16)
    net.addLink(h8, s16)
    net.addLink(h9, s17)
    net.addLink(h10, s17)
    net.addLink(h11, s18)
    net.addLink(h12, s18)
    net.addLink(h13, s19)
    net.addLink(h14, s19)
    net.addLink(h15, s20)
    net.addLink(h16, s20)
    net.addLink(s3, s4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s17').start([])
    net.get('s13').start([])
    net.get('s15').start([])
    net.get('s10').start([])
    net.get('s6').start([])
    net.get('s18').start([])
    net.get('s11').start([])
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s4').start([])
    net.get('s9').start([])
    net.get('s14').start([])
    net.get('s12').start([])
    net.get('s16').start([])
    net.get('s3').start([])
    net.get('s7').start([])
    net.get('s5').start([])
    net.get('s8').start([])
    net.get('s19').start([])
    net.get('s20').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


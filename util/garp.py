from socket import *
from sys import *
import pdb

def sendeth(arp_frame, interface = "h5-eth0"):
    """Send raw Ethernet packet on interface."""
    s = socket(AF_PACKET, SOCK_RAW)

    # From the docs: "For raw packet
    # sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])"
    s.bind((interface, 0))
    return s.send(arp_frame)

def pack(byte_sequence):
    """Convert list of bytes to byte string."""
    print byte_sequence
    return b"".join(map(chr, byte_sequence))

if __name__ == "__main__":
    # Formulate a Gratuitous ARP
    # https://en.wikipedia.org/wiki/EtherType
    eth_dst = [0xff,0xff,0xff,0xff,0xff,0xff]
    eth_src = [0x10,0x00,0x00,0x00,0x00,int(argv[1])]
    eth_type = [0x08, 0x06]
    arp_type = [0x00, 0x01, 0x08, 0x00, 0x06, 0x04]
    arp_reply = [0x00, 0x02]
    arp_req = [0x00, 0x01]
    ip_src = ip_dst = [0x0a,0x00,0x00,int(argv[1])]

    # arpframe
        ## ETHERNET
        # destination MAC addr
        # source MAC addr
        # ETHERNET_PROTOCOL_TYPE_ARP,
        ## ARP
        # ARP_PROTOCOL_TYPE_ETHERNET_IP,
        # operation type request/reply
        # sender MAC addr
        # sender IP addr
        # target hardware addr
        # target IP addr

    arp_frame = eth_dst+eth_src+eth_type+arp_type+arp_req+eth_src+ip_src+eth_dst+ip_dst

    # Construct Ethernet packet with an IPv4 ICMP PING request as payload
    r = sendeth(pack(arp_frame))
    print("Sent GARP payload of length %d bytes" % r)

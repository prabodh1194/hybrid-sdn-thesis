import socket as so
import sys

s = so.socket(so.AF_INET, so.SOCK_DGRAM)

s.sendto("Hi",(sys.argv[1],10000))

s.close()

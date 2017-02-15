import socket

HOST = ''
PORT = 162

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))

while 1:
    data,addr = s.recvfrom(1024)
    print addr
    print data
    if not data: 
        break
conn.close()

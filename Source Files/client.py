#!usr/bin/python
from socket import *

#host = 'localhost' # '127.0.0.1' can also be used
#host = '129.107.132.24'
host = 'cse208erbpc5'

port = 52001

sock = socket()
#Connecting to socket
sock.connect((host, port)) #Connect takes tuple of host and port

#Infinite loop to keep client running.
while True:
    data = sock.recv(1024)
    print data
    sock.send('HI! I am client.')

sock.close()
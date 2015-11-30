import time
from socket import *

pings = 1

#Send ping 10 times 
for pings in range(10):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    message = 'this is a test'
    addr = ("127.0.0.1", 12000)

    #Send ping
    startTime = time.time()
    clientSocket.sendto(message, addr)
 
    try:
        data, server = clientSocket.recvfrom(1024)
        elapsed = time.time() - startTime
        print '    data = %s\n    pings = %d\n    elapsed = %s\n' % (data, pings, elapsed)      

    #If data is not received back from server, print it has timed out  
    except timeout:
        print 'REQUEST TIMED OUT'

    pings = 1
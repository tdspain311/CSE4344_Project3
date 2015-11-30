"""
    Ji yeon Jeong
    Nov 27 2015
    CSE 4344
    interface.py 
"""
import random

### Save IP address into list
def getIP(a):
    i = 0
    ipList = [];
    while ( i < a ):
        ip = raw_input("Enter IP %d Address: " %i); 
        ipList.append(ip)
        print "IP %d: %r" %(i, ipList[i])  
        i += 1

### Save Random IP distance into list
def randomDist(a):
    j = 0
    ipDist = [];
    while (j < a):
        dist = random.randint(1, 10);
        ipDist.append(dist)
        print "IP Distance %d: %d" % (j, ipDist[j])
        j += 1

### Main ###
a = int(input("Enter Number of Nodes from 2 to 5: "));

getIP(a);

randomDist(a);

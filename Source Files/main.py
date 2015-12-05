"""
Krishna Bhattarai
Computer Networks, CSE 4345
Project #3
November 16, 2015
Implementation of the Distance Vector Routing Protocol
References: Page 371-379 from the book

"""
import random
import string
import time
from socket import *

#GLOBAL VARS
TABLE = []
CONNECTED = []
DISTANCE = [[0, 1, 2, 999, 999],
            [1, 0, 3, 999, 5],
            [2, 3, 0, 4, 7],
            [999, 999, 4, 0, 6],
            [999, 5, 7, 6, 0]]

def init():
    """
    Initialize by prompting user for # of nodes in set and to set IP addresses
    Then create the initial routing table using the DVR algorithm
    """

    
    nodes = 1
    while nodes not in range(2, 6):
        nodes = int(input("Enter the number of nodes joining Network from 2 to 5: "));
        if nodes not in range(2, 6):
            print "Number must be between 2 and 5"
        

    #Save IP address into list
    addressList = GetIP(nodes)

    #Set the HOST ip by prompting client
    IdentifySelf(addressList)

    print "\n\n================"
    print "::INITIALIZING::"
    print "================\n"
    
    CreateTable(addressList)

    CreateHostTable()

    print "\n\n=================="
    print "::BUILDING TABLE::"
    print "==================\n"
    
    finalTable1 = DVR_init_(addressList[0], 0)
    time.sleep(1)
    finalTable2 = DVR_init_(addressList[1], 1)
    time.sleep(1)
    finalTable3 = DVR_init_(addressList[2], 2)
    time.sleep(1)
    finalTable4 = DVR_init_(addressList[3], 3)
    time.sleep(1)
    finalTable5 = DVR_init_(addressList[4], 4)

        
    result = [finalTable1[1], finalTable2[1], finalTable3[1], finalTable4[1], finalTable5[1]]
    result2 = [finalTable1[0], finalTable2[0], finalTable3[0], finalTable4[0], finalTable5[0]]

    print "\nIndex Table"
    print "====================================="
    PrintFormatedTable(result2)

    print "\nCompleted Table"
    print "====================================="
    PrintFormatedTable(result)

def DVR_init_(addr_, source):
    # auxiliary constants
    DISTANCE
    SIZE = len( DISTANCE )
    EVE = -1; # to indicate no predecessor
    INFINITY = 999

    # declare and initialize pred to EVE and minDist to INFINITY
    pred = [addr_]
    temp = [EVE] * SIZE
    pred.extend(temp)
    minDist = [addr_]
    temp = [INFINITY] * SIZE
    minDist.extend(temp)

    # set minDist[source] = 0 because source is 0 distance from itself.
    minDist[source+1] = 0

    # relax the edge set V-1 times to find all shortest paths
    print("\n\nRouting Table for Node %c" %string.ascii_uppercase[source])
    print("Next Hop \t\t Table   ")
    print("=====================================")
    for i in range( 1, SIZE - 1 ):
      for v in range( SIZE ):
        for x in Adjacency( DISTANCE, v ):
          if minDist[x+1] > minDist[v+1] + DISTANCE[v][x]:
            minDist[x+1] = minDist[v+1] + DISTANCE[v][x]
            pred[x+1] = v
            print "next hop = ", x, "\t", minDist
            time.sleep(2)
            
    # detect cycles if any
    for v in range( SIZE ):
      for x in Adjacency( DISTANCE, v ):
        if minDist[x+1] > minDist[v+1] + DISTANCE[v][x]:
          raise Exception( "Negative cycle found" )

    return [pred, minDist]

def Adjacency(G, v):
    result = []
    for x in range( len( G ) ):
      if G[v][x] is not 'X':
        result.append( x )

    return result

def CreateHostTable():

    pos = 1
    for node in TABLE:
        if HOST[0] == node[0]:
            print "\nSelected Host: ", node[0]

    print "\n"
    
def IdentifySelf(hosts_):
    """
    Prompt User with list to Identify itself in the network
    ex.
    1. 192.168.1.1
    2. 192.168.1.2
    3. 192.168.1.3
    4. 192.168.1.4
    5. 192.168.1.5
    """
    global HOST

    identifiedHost = 0
    while identifiedHost not in range(1, len(hosts_)+1):
        i = 1
        print "\n"
        for host in hosts_:
            print "{hid}. {hip}".format(hid=i, hip=host)
            i += 1
        print "\n"
        identifiedHost = int(input("Select your local host: "));
        if identifiedHost not in range(1, len(hosts_)+1):
            print "Number must be between 1 and 5"
        else:
            HOST = [hosts_[identifiedHost-1]]
    
    

def CreateTable(addr_):
    """
    Create the initial table here with the full list of addresses and distances
    Default configurating for nodes will be implemented by:

    A -2- C -4- D
    |    /|   /
    1  3  7  6
    | /   | /
    B -5- E

    Distances will be static and be an array with the format:

    [IP ADDR, node1, node2, ... , node5]

    ex. [192.168.1.1, 0, 4, 5, 999, 999]
    Where the distances to each node will be placed in the array and:
     0 is represented as itself
     999 is represented as 'infinity'

    Book Psuedocode for init:
    for all destinations y in N:
        Dx(y) = c(x,y)
        #if y is not a neighbor then c(x,y) = ∞ 
        for each neighbor w
            Dw(y) = ? for all destinations y in N
        for each neighbor w
            send distance vector Dx = [Dx(y): y in N] to w

    """
    #init all node data cells to 'inifinity' in table
    for node in addr_:
        nodeData = [node]
        initData = []
        i = 0
        while (i < len(addr_)):
            initData.append(999)
            i += 1
        nodeData.extend(initData)
        TABLE.append(nodeData)

    #Create connected node graph
    ConnectedNodes()

    #Print the Current IP Table and Node Table
    PrintFormatedTable(TABLE)

def ConnectedNodes():
    """
    ex.
    Connected Nodes
    || NODE |  A  |  B  |  C  |  D  |  E  ||
    ||  A   |     |  X  |  X  |     |     ||
    ||  B   |  X  |     |  X  |     |  X  ||
    ||  C   |  X  |  X  |     |  X  |  X  ||
    ||  D   |     |     |  X  |     |  X  ||
    ||  E   |  X  |  X  |  X  |  X  |     ||

    This is a static table that every client is aware of its connected nodes
    """

    print "Connected Table"
    if (len(TABLE) == 2):
        fmtConn = "||{0:^7}|{1:^7}|{2:^7}||"
        print fmtConn.format('Node', 'A', 'B')
        CONNECTED = [[' ', 'X'],
                     ['X', ' ']]
    elif (len(TABLE) == 3):
        fmtConn = "||{0:^7}|{1:^7}|{2:^7}|{3:^7}||"
        print fmtConn.format('Node', 'A', 'B', 'C')
        CONNECTED = [[' ', 'X', 'X'],
                     ['X', ' ', 'X'],
                     ['X', 'X', ' ']]
    elif (len(TABLE) == 4):
        fmtConn = "||{0:^7}|{1:^7}|{2:^7}|{3:^7}|{4:^7}||"
        print fmtConn.format('Node', 'A', 'B', 'C', 'D')
        CONNECTED = [[' ', 'X', 'X', ' '],
                     ['X', ' ', 'X', ' '],
                     ['X', 'X', ' ', 'X'],
                     [' ', ' ', 'X', ' ']]
    elif (len(TABLE) == 5):
        fmtConn = "||{0:^7}|{1:^7}|{2:^7}|{3:^7}|{4:^7}|{5:^7}||"
        print fmtConn.format('Node', 'A', 'B', 'C', 'D', 'E')
        CONNECTED = [[' ', 'X', 'X', ' ', ' '],
                     ['X', ' ', 'X', ' ', 'X'],
                     ['X', 'X', ' ', 'X', 'X'],
                     [' ', ' ', 'X', ' ', 'X'],
                     ['X', 'X', 'X', 'X', ' ']]

    for node in range(len(TABLE)):
        row = [string.ascii_uppercase[node]]
        row.extend(CONNECTED[node])
        print fmtConn.format(*row)

    print "\n"

def PrintFormatedTable(t):
    """
    ex.
    IP Table
    ||  NODE  | IP ADDRESS  ||
    ||   A    | 192.168.1.1 ||
    ||   B    | 192.168.1.2 ||
    ||   C    | 198.168.1.3 ||
    ||   D    | 192.168.1.4 ||
    ||   E    | 192.168.1.5 ||

    Node Table
    ||  NODE  |   A   |   B   |   C   |   D   |   E   ||
    ||   A    |   0   |   1   |   2   |  999  |  999  ||
    ||   B    |   1   |   0   |   3   |  999  |   5   ||
    ||   C    |   2   |   3   |   0   |   4   |   7   ||
    ||   D    |  999  |  999  |   4   |   0   |   6   ||
    ||   E    |  999  |   5   |   7   |   6   |   0   ||

    """
    
    fmtIP = "||{0:^9}|{1:^14}||"
    print "IP Table"
    print fmtIP.format('Node', 'IP ADDRESS')

    for ipData in range(len(t)):
        node = string.ascii_uppercase[ipData]
        ip = t[ipData][0]
        print fmtIP.format(node, ip)

    print "\n"
    print "Node Table"
    if (len(t) == 2):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}||"
        print fmtNode.format('Node', 'A', 'B')
    elif (len(t) == 3):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}|{3:^9}||"
        print fmtNode.format('Node', 'A', 'B', 'C')
    elif (len(t) == 4):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}|{3:^9}|{4:^9}||"
        print fmtNode.format('Node', 'A', 'B', 'C', 'D')
    elif (len(t) == 5):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}|{3:^9}|{4:^9}|{5:^9}||"
        print fmtNode.format('Node', 'A', 'B', 'C', 'D', 'E')

    for node in range(len(t)):
        row = [string.ascii_uppercase[node]]
        row.extend(t[node][1:])
        print fmtNode.format(*row)
    
def GetIP(numNodes_):
    i = 1
    ipList = []
    while ( i <= numNodes_ ):
        ip = raw_input("Enter IP Address of host %d: " %i) 
        ipList.append(ip)
        i += 1

    return ipList

def GetPortNumbers(numNodes_):
    host = HOST[0]
    if host == TABLE[0][0]:
        # If the host is node A, create host socket with ports 12000,12002
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        #serverSocket2 = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((host,12000))
        #serverSocket2.bind((host,12002))
        while True:
            message, address = serverSocket.recvfrom(1024)
            #message, address = serverSocket2.recvfrom(1024)
        serverSocket.close()
        #serverSocket2.close()
        
    if host == TABLE[1][0]:
        # If the host is node B, create host socket with port 12001
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((host, 12001))
        message, address = serverSocket.recvfrom(1024)
        serverSocket.close()
    if host == TABLE[2][0]:
        # If the host is node C, create host socket with port 12003
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((host, 12003))
        message, address = serverSocket.recvfrom(1024)
        serverSocket.close()
def main():
    """
    Main function, should initialize to get user to enter all nodes into table
    then it will transmit its table to its neighbor nodes, neighboring nodes will use
    DVR algorithm to create a complete table
    """
    init()
    PORTS = range(12000,12013)
    
    GetPortNumbers(5)
    pass

# Invoke the main function here
if __name__ == "__main__":
    main()


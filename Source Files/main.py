﻿"""
Krishna Bhattarai
Computer Networks, CSE 4345
Project #3
November 16, 2015
Implementation of the Distance Vector Routing Protocol
References: Page 371-379 from the book

"""
import random
import string

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

    finalTable1 = DVR_init_(0)
    finalTable2 = DVR_init_(1)
    finalTable3 = DVR_init_(2)
    finalTable4 = DVR_init_(3)
    finalTable5 = DVR_init_(4)

    temp = []
    temp = addressList[0]

        
    result = [finalTable1[1], finalTable2[1], finalTable3[1], finalTable4[1], finalTable5[1]]
    result2 = [finalTable1[0], finalTable2[0], finalTable3[0], finalTable4[0], finalTable5[0]]

    
    print result
    print result2

def DVR_init_(source):
    # auxiliary constants
    DISTANCE
    SIZE = len( DISTANCE )
    EVE = -1; # to indicate no predecessor
    INFINITY = 999

    # declare and initialize pred to EVE and minDist to INFINITY
    pred = [EVE] * SIZE
    minDist = [INFINITY] * SIZE

    # set minDist[source] = 0 because source is 0 distance from itself.
    minDist[source] = 0

    # relax the edge set V-1 times to find all shortest paths
    for i in range( 1, SIZE - 1 ):
      for v in range( SIZE ):
        for x in Adjacency( DISTANCE, v ):
          if minDist[x] > minDist[v] + DISTANCE[v][x]:
            minDist[x] = minDist[v] + DISTANCE[v][x]
            #print minDist, v
            pred[x] = v
            


    # detect cycles if any
    for v in range( SIZE ):
      for x in Adjacency( DISTANCE, v ):
        if minDist[x] > minDist[v] + DISTANCE[v][x]:
          raise Exception( "Negative cycle found" )

    
    #return [pred, minDist]
    #print([pred, minDist])
    #return [pred, minDist]
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
    PrintFormatedTable()

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

def PrintFormatedTable():
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

    for ipData in range(len(TABLE)):
        node = string.ascii_uppercase[ipData]
        ip = TABLE[ipData][0]
        print fmtIP.format(node, ip)

    print "\n"
    print "Node Table"
    if (len(TABLE) == 2):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}||"
        print fmtNode.format('Node', 'A', 'B')
    elif (len(TABLE) == 3):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}|{3:^9}||"
        print fmtNode.format('Node', 'A', 'B', 'C')
    elif (len(TABLE) == 4):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}|{3:^9}|{4:^9}||"
        print fmtNode.format('Node', 'A', 'B', 'C', 'D')
    elif (len(TABLE) == 5):
        fmtNode = "||{0:^9}|{1:^9}|{2:^9}|{3:^9}|{4:^9}|{5:^9}||"
        print fmtNode.format('Node', 'A', 'B', 'C', 'D', 'E')

    for node in range(len(TABLE)):
        row = [string.ascii_uppercase[node]]
        row.extend(TABLE[node][1:])
        print fmtNode.format(*row)
    
def GetIP(numNodes_):
    i = 1
    ipList = []
    while ( i <= numNodes_ ):
        ip = raw_input("Enter IP Address of host %d: " %i) 
        ipList.append(ip)
        i += 1

    return ipList

def main():
    """
    Main function, should initialize to get user to enter all nodes into table
    then it will transmit its table to its neighbor nodes, neighboring nodes will use
    DVR algorithm to create a complete table
    """
    init()
    pass

# Invoke the main function here
if __name__ == "__main__":
    main()


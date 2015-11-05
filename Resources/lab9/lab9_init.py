import random,sys,math
from lab9_net import *

"""Skeleton for link-state routing lab in 6.082
"""
# use our own node class derived from the node class of network10.py
# so we can override routing behavior
class MyNode(Node):
    HELLO_INTERVAL = 10   # time between HELLO packets
    LSA_INTERVAL = 50     # time between LSA packets
    INFINITY = sys.maxint
        
    def __init__(self,location,address=None):
        Node.__init__(self, location, address=address)
        # additional instance variables
        self.neighbors = {} # Link -> (timestamp, address)
        self.costs = {}                # Link -> (cost)
        # LSA: address -> (seqnum nbhr1 nbhr2 nbhr3 cost1 cost2 cost3 ...)
        self.LSA = {} 
        self.LSA_seqnum = 0 # uniquely identify each LSA broadcast
        self.routes = {}    # address -> Link

    # return the link corresponding to a given neighbor, nbhr
    def getlink(self, nbhr):
        if self.address == nbhr: return None
        for l in self.links: 
            if l.end2.address == nbhr or l.end1.address == nbhr:
                return l

    # use routing table to forward packet along appropriate outgoing link
    def forward(self,p):
        link = self.routes.get(p.destination, None)
        if link is None:
            print 'No route for ',p,' at node ',self
        else:
            link.send(self, p)   

    def process(self, p, link, time):
        if p.destination == 'HELLO':
            # remember addresses of our neighbors and time of latest update
            self.neighbors[link] = (time, p.source, link.cost)
        elif p.destination == 'LSA':
            # process incoming LSA packet
            # first get sequence number from packet, then see if we have a 
            # previous entry in LSA from the same node
            seq = p.properties['seqnum']
            saved = self.LSA.get(p.source, (-1,))
            if seq > saved[0]:
                # update only if incoming seqnum is larger than saved seqnum
                self.LSA[p.source] = [seq] + p.properties['neighbors']
                # STEP 2(b): Rebroadcast packet to our neighbors here
                # We don't have to rebroadcast to the neighbor we just got
                # the LSA from, but we're going to ignore that obvious
                # optimization here and do it anyway...
		pass

        else:
            Node.process(self, p, link, time)

    def transmit(self, time):
        if (time % self.HELLO_INTERVAL) == 0:
            # STEP 1(a): send HELLO packets along all my links to neighbors
            # These periodic HELLOs tell our neighbors I'm still alive
            # The neighbors will get my address from the source address field
	    pass

            # STEP 1(b) : Code to remove out-of-date entries from self.LSA.
            # Look through neighbors table and eliminate out-of-date entries.
	    pass

        if (time % self.LSA_INTERVAL) == 0:
            # STEP 2(a). Send out LSA packets to all our neighbors.
	    pass

            # After sending out LSA packets, clear out older LSA entries
            for key,value in self.LSA.items():
                if value[0] < self.LSA_seqnum-1:
                    del self.LSA[key]

        if (time % self.LSA_INTERVAL) == self.LSA_INTERVAL/2:
            # We now have all the LSA advertisements.  Let's clear the 
            # current routing table and rebuild it.
            self.routes.clear()
            visited_nodes = [self.address]
            self.spcost = {}        # Node --> shortest path cost to node
            numnodes = 1

            self.LSA[self.address] = [0] # hack; set seqnum for my own lsa

            # Go through my neighbors
            for link, (timestamp, u, c) in self.neighbors.items():
                numnodes = numnodes + 1
                visited_nodes.append(u)
                self.spcost[u] = self.INFINITY
                self.LSA[self.address].append(u)
                self.LSA[self.address].append(link.cost)

            # The snippet below scans each node's LSA to visit all the
            # other non-neighbor nodes emulating a breadth first
            # search (BFS).  The reason we do a BFS traversal rather
            # than simply use len(self.LSA) to calculate the number of
            # nodes and set the spcost to each one to infinity, is
            # because we want the numnodes to be equal to the number
            # of nodes currently reachable from us.  On initialization
            # as well as after a failure, we would have heard a
            # re-broadcast LSA from a node, but have no way of
            # reaching it.
            for u in visited_nodes:
                lsa_info = self.LSA[u][1:]
                for i in range(0, len(lsa_info),2):
                    v = lsa_info[i]
                    if not v in visited_nodes:
                        numnodes = numnodes + 1
                        visited_nodes.append(v)
                        self.spcost[v] = self.INFINITY

            # STEP 3: Code for Dijkstra's shortest-path computation below.
            # In each iteration of the outer loop, add a new node to 
            # nodes_done until all nodes are in nodes_done.  Add nodes in
            # non-decreasing order of shortest path cost.
	    # Make sure you initialize the spcost for node's own address and 
	    # add a dummy route to yourself ("None").  I.e., initialize
	    # self.spcost[self.address], nodes_done, self.routes[self.address]
	    
            return

    def OnClick(self,which):
        if which == 'left':
            print self
            print '  neighbors:',self.neighbors.values()
            print '  LSA:'
            for (key,value) in self.LSA.items():
                print '    ',key,': ',value
            print '  routes:'
            for (key,value) in self.routes.items():
                print '    ',key,': ',value, 'pathcost %.2f' % self.spcost[key]


# a grid network with nodes of type MyNode.
# after reset, there's a single packet that needs to be delivered
class MyNetwork(Network):
    def __init__(self):
        Network.__init__(self)
        # build the test network
        #   A---B   C---D
        #   |   | / | / |
        #   E   F---G---H
        for n,r,c in (('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
                      ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1)):
            self.add_node(r,c,address=n)
        for a1,a2 in (('A','B'),('A','E'),
                      ('B','F'),
                      ('C','D'),('C','F'),('C','G'),
                      ('D','G'),('D','H'),
                      ('F','G'),
                      ('G','H')):
            n1 = self.addresses[a1]
            n2 = self.addresses[a2]
            self.add_link(n1.location[0],n1.location[1],
                          n2.location[0],n2.location[1])
    
    # nodes should be an instance of MyNode (defined above)
    def make_node(self,loc,address=None):
        return MyNode(loc,address=address)

    # reset network to its initial state
    def reset(self):
        # parent class handles the details
        Network.reset(self)
        # insert a single packet into the network with randomly
        # chosen source and destination.  Since we don't have code
        # to deliver the packet this just keeps the simulation alive...
        src = random.choice(self.nlist)
        dest = random.choice(self.nlist)
        src.add_packet(self.make_packet(src.location,dest.location,1))


# Network with link costs.  By default, the cost of a link is the 
# Euclidean distance between the nodes at the ends of the link
class MyCostNetwork(Network):
    def __init__(self):
        Network.__init__(self)
        # build the test network
        #   A---B   C---D
        #   |   | / | / |
        #   E   F---G---H
        for n,r,c in (('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
                      ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1)):
            self.add_node(r,c,address=n)
        for a1,a2 in (('A','B'),('A','E'),
                      ('B','F'),
                      ('C','D'),('C','F'),('C','G'),
                      ('D','G'),('D','H'),
                      ('F','G'),
                      ('G','H')):
            n1 = self.addresses[a1]
            n2 = self.addresses[a2]
            self.add_link(n1.location[0],n1.location[1],
                          n2.location[0],n2.location[1])
    
    # nodes should be an instance of MyNode (defined above)
    def make_node(self,loc,address=None):
        return MyNode(loc,address=address)

    def make_link(self,n1,n2):
        return CostLink(n1,n2)

    def add_cost_link(self,x1,y1,x2,y2):
        n1 = self.find_node(x1,y1)
        n2 = self.find_node(x2,y2)
        if n1 is not None and n2 is not None:
            link = self.make_cost_link(n1,n2)
            link.network = self
            self.links.append(link)


    # reset network to its initial state
    def reset(self):
        # parent class handles the details
        Network.reset(self)
        # insert a single packet into the network with randomly
        # chosen source and destination.  Since we don't have code
        # to deliver the packet this just keeps the simulation alive...
        src = random.choice(self.nlist)
        dest = random.choice(self.nlist)
        src.add_packet(self.make_packet(src.location,dest.location,1))


# make a network
net = MyCostNetwork()

# setup graphical simulation interface
sim = NetSim()
sim.SetNetwork(net)
sim.MainLoop()

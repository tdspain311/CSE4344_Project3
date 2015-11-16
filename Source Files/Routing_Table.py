"""
Krishna Bhattarai
Computer Networks, CSE 4345
Project #3
November 16, 2015
Implementation of the Distance Vector Routing Protocol
"""


class Node:
    def __init__(self):
        # The id by which a Node will be identified
        self.ID = None


class RoutingTable:
    def __init__(self):
        # The Network ID or destination corresponding to the route. The network ID can be
        # subnet or supernet network ID or an IP address for a host route.
        self.NetworkID = None
        # The ip address of the next hop
        self.NextHop = None
        # A number used to indicate the cost of the route so the best route among
        # possible multiple routes to the same destination can be selected.
        self.MetricCost = None
        # An indication of which network interface is used to forward the IP packet.
        self.Interface = None
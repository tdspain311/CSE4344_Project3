"""
Krishna Bhattarai
Computer Networks, CSE 4345
Project #3
November 16, 2015
Implementation of the Distance Vector Routing Protocol
References: Page 371-379 from the book
"""

# Import a bunch of useful stuff here
import os, re, socket, threading, select

# Define a bunch of constants
MessageInterval = 15
MessageTimeout = 35
PathDiscoveryTime = 35
ActiveRouteTimeout = 35


class DVR(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ID = None
        self.TotalNodes = None
        self.PortNumber = None
        self.Status = "Passive"
        self.Timer = None

        # Dictionaries
        self.Neighbours = {}
        self.RoutingTable = {}
        self.MessageBox = {}


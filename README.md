# CSE4344_Project3
Project 3 Assignment for Computer Networks

Implement the distance vector routing protocol

DVR works by having each routing node periodically exchange routing updates with its
neighbors. Each routing update contains the node’s entire routing table. Upon receiving a
routing update, a node updates its routing table with the “best” routes to each destination. In
addition, each routing daemon must remove entries from its routing table when they have not
been updated for a long time.
Your implementation of DVR should have the following features:
  1. Full routing table updates should be exchanged between neighboring nodes every
    advertisement cycle.
  2. In the event of a tie for shortest path, the next hop in the routing table should always
    point to the nodeID with the lowest numerical value.
  3. Set all routes in the routing table through a neighbor to the infinity value if it hasn’t
    given any updates for some period of time.
  4. Set routes in the routing table to the infinity value if they have not been updated for
    some period of time (“expire” them).
  5. Delete routes from the routing table that have been set to infinity for some period of
  time (“garbage collect” them).
  6. If a node or link goes down (e.g., routing daemon crashes, or link between them no
    longer works and drops all messages), your routing tables in the network should reflect
    the new network graph.

Developed by
  Tyler D'Spain
  Krishna Bhattarai
  Zachary Allen
  Ji Yeon Jeong
  David Harvey

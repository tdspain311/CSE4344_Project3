
from sys import maxint
import time
import threading

def bellman_ford(weight, source) :
    # auxiliary constants
    SIZE = len( weight )
    EVE = -1 # to indicate no predecessor
    INFINITY = maxint

    # declare and initialize pred to EVE and minDist to INFINITY
    pred = [EVE] * SIZE
    minDist = [INFINITY] * SIZE
    table1, table2, table3, table4, table5 = [], [], [], [], []

    # set minDist[source] = 0 because source is 0 distance from itself.
    minDist[source] = 0

    # relax the edge set V-1 times to find all shortest paths
    print("\n\nRouting Table for Node %d" % source)
    print("Next Hop \t\t Table   ")
    print("=====================================")
    for i in range( 1, SIZE - 1 ):
      for v in range( SIZE ):
        for x in adjacency( weight, v ):
          if minDist[x] > minDist[v] + weight[v][x]:
            minDist[x] = minDist[v] + weight[v][x]
            pred[x] = v
            print "next hop = ", x, "\t", minDist
            time.sleep(2)

    # detect cycles if any
    for v in range(SIZE):
      for x in adjacency( weight, v ):
        if minDist[x] > minDist[v] + weight[v][x]:
          raise Exception("Negative cycle found" )
    return [pred, minDist]


def adjacency(G, v):
    result = []
    for x in range(len(G)):
        if G[v][x] is not None:
            result.append(x)
    return result

"""
    A -2- C -4- D
    |    /|   /
    1  3  7  6
    | /   | /
    B -5- E
"""
master_table = [[0, 1, 2, None, None],
                [1, 0, 3, None, 5],
                [2, 3, 0, 4, 7],
                [None, None, 4, 0, 6],
                [None, 5, 7, 6, 0]]


result1 = bellman_ford(master_table, 0)
time.sleep(5)
result2 = bellman_ford(master_table, 1)
time.sleep(5)
result3 = bellman_ford(master_table, 2)
time.sleep(5)
result4 = bellman_ford(master_table, 3)
time.sleep(5)
result5 = bellman_ford(master_table, 4)
time.sleep(5)

final_result = [result1[1], result2[1], result3[1], result4[1], result5[1]]

print("\nThe final solution to the problem is:")
for items in final_result:
    print items

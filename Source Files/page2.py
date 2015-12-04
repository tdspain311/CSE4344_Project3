#
#
#   Node Table
#     ||  NODE  |   A   |   B   |   C   |   D   |   E   ||
#     ||   A    |   0   |   1   |   2   |  999  |  999  ||
#     ||   B    |   1   |   0   |   3   |  999  |   5   ||
#     ||   C    |   2   |   3   |   0   |   4   |   7   ||
#     ||   D    |  999  |  999  |   4   |   0   |   6   ||
#     ||   E    |  999  |   5   |   7   |   6   |   0   ||
#
# master_table = [[0, 1, 2, 999, 999],
#                 [1, 0, 3, 999, 5],
#                 [2, 3, 0, 4, 7],
#                 [999, 999, 4, 0, 6],
#                 [999, 5, 7, 6, 0]]
#
# nodes = [A, B, C, D, E]
# # every 30 seconds each node updates the table
#
# for each_node in nodes:


from sys import maxint
class BellmanFord( object ):

  def __init__( self ):
      '''
      Constructor
      '''

  def singleSourceShortestPath( self, weight, source ) :
    # auxiliary constants
    SIZE = len( weight )
    EVE = -1; # to indicate no predecessor
    INFINITY = maxint

    # declare and initialize pred to EVE and minDist to INFINITY
    pred = [EVE] * SIZE
    minDist = [INFINITY] * SIZE

    # set minDist[source] = 0 because source is 0 distance from itself.
    minDist[source] = 0

    # relax the edge set V-1 times to find all shortest paths
    for i in range( 1, SIZE - 1 ):
      for v in range( SIZE ):
        for x in self.adjacency( weight, v ):
          if minDist[x] > minDist[v] + weight[v][x]:
            minDist[x] = minDist[v] + weight[v][x]
            print minDist, v
            pred[x] = v
      print "\n"


    # detect cycles if any
    for v in range( SIZE ):
      for x in self.adjacency( weight, v ):
        if minDist[x] > minDist[v] + weight[v][x]:
          raise Exception( "Negative cycle found" )


    #return [pred, minDist]
    #print([pred, minDist])
    # return [pred, minDist]
    return [pred, minDist]
  #=====================================================================
  # Retrieve all the neighbors of vertex v.
  #=====================================================================
  def adjacency( self, G, v ) :
    result = []
    for x in range( len( G ) ):
      if G[v][x] is not None:
        result.append( x )

    return result


weight = [
      [None, 10, None, None, 3],
      [None, None, 2, None, 1],
      [None, None, None, 7, None],
      [None, None, 9, None, None],
      [None, 4, 8, 2, None]
    ]

master_table = [[0, 1, 2, None, None],
                [1, 0, 3, None, 5],
                [2, 3, 0, 4, 7],
                [None, None, 4, 0, 6],
                [None, 5, 7, 6, 0]]


source = 0
myobject =  BellmanFord()
result0 = myobject.singleSourceShortestPath( master_table,0 )
result1 = myobject.singleSourceShortestPath( master_table, 1 )
result2 = myobject.singleSourceShortestPath( master_table, 2 )
result3 = myobject.singleSourceShortestPath( master_table, 3 )
result4 = myobject.singleSourceShortestPath( master_table, 4 )
#print(result0)
# print(result1)
# print(result2)
# print(result3)
# print(result4)

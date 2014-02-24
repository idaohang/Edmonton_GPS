"""
Dijkstra's algorithm
"""

import digraph
import math

def cost(vtuple):
    """
    This cost function was just used to test the basic functionality
    of the least_cost_path function. It simply assigns '1' to be the
    cost to traverse an edge. More extensive testing is done in the
    server.py module with the costs from the Edmonton road map.
    """

    return 1

def least_cost_path(G, start, dest, cost):
    """
    path = least_cost_path(G, start, dest, cost)

    least_cost_path returns a least cost path in the digraph G from vertex
    start to vertex dest, where costs are defined by the cost function.
    cost should be a function that takes a single edge argument and returns
    a real-valued cost.

    If there is no path, then returns an empty list

    the path from start to start is [start]

    
    Try testing a basic graph to find the minimum path
    >>> G = digraph.Digraph([ (1,2), (2,3), (3,1),(4,3),(3,5),(5,4) ] )
    >>> least_cost_path(G, 1, 5, cost)
    [1, 2, 3, 5]

    Try going to a disconnected component. Should return an empty list
    >>> G = digraph.Digraph([ (1,2), (2,3), (3,1),(4,3),(3,5),(5,4),(6,7)] )
    >>> least_cost_path(G, 1, 7, cost)
    []
    
    Start = dest, should return [1]
    >>> least_cost_path(G, 1, 1, cost)
    [1]

    Try going to a vertex that does not exist. Empty list should return.
    >>> least_cost_path(G, 1, 8, cost)
    []
    
    Try a slightly more complicated graph. Should return [1, 2, 3, 5].
    >>> G = digraph.Digraph( [ (1,2), (2,3), (1,4), (3,7), (3,4), (3,5), (5,4), (4,6), (3,7), (7,5) ] )
    >>> least_cost_path(G, 1, 5, cost)
    [1, 2, 3, 5]

    Try having start = dest where the vertex is not in the graph. Should return [].
    >>> least_cost_path(G, 9, 9, cost)
    []

    """

    # todo[v] is the current best estimate of cost to get from start to v 
    todo = { start: 0}

    # v in visited when the vertex v's least cost from start has been determined
    visited = set()

    # parent[v] is the vertex that just precedes v in the path from start to v
    parent = {}

    # if the start vertex is the destination vertex, and that vertex isn't the graph. Return []
    if start == dest and start not in G.vertices():
        return []

    while todo and (dest not in visited):

        # priority queue operation
        # remove smallest estimated cost vertex from todo list
        # this is not the efficient heap form, but it works
        # because it mins on the cost (2nd) field of the tuple of
        # items from the todo dictionary

        (cur,c) = min(todo.items(), key=lambda x: x[1])
        todo.pop(cur)

        # it is now visited, and will never have a smaller cost
        visited.add(cur)

        # look at vertices which are adjacent to the current vertex
        for n in G.adj_to(cur):
            if n in visited: continue
            # if you haven't looked at something yet, or the cost is lower, assign the new cost
            if n not in todo or ( c + cost((cur,n)) < todo[n] ): 
                todo[n] = c + cost((cur,n)) # sets the tenative cost to current minimum
                parent[n] = cur # set the parent to the current node
                
  
    # now, if there is a path, extract it.  The graph may be disconnected
    # so in that case return []

    # if the start vertex is the destination vertex, and that vertex is in the graph. Return it.
    if start == dest and start in G.vertices():
        return [start]

    # if the destination gets reached we can form a minimum path
    elif dest in visited:
        path = [dest]   # start by putting the destination in the path (we make the path in reverse order)
        
        # start at the destination and continuosly find the parent of the current vertex until
        # you reach the starting vertex.
        vertex_iterator = dest
        while parent[vertex_iterator]!=start:
            path.append(parent[vertex_iterator])
            vertex_iterator = parent[vertex_iterator]

        # place the start vertex in the path
        path.append(start) 
        # reverse the path to get the proper order
        path.reverse()

        return path
    
    # if no path from start to dest exists return an empty list
    else:
        return []

if __name__ == "__main__":
    import doctest
    doctest.testmod()

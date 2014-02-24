"""
python3 readgraph.py [ digraph-file ]

Takes a csv (comma separated values) text file containing the vertices
and edges of a street digraph and converts it into a digraph instance.

If the optional argument digraph-file is supplied, reads that, otherwise
takes input from stdin
"""

import sys
import math
import digraph
import dijkstra
import serial
import argparse

global debug
debug = False

# the file we will use is edmonton-roads.txt
digraph_file = open('edmonton-roads.txt', 'r')

# For testing, just use a simple representation of set of vertices, set of
# edges as ordered pairs, and dctionaries that map
#   vertex to (lat,long)
#   edge to street name

V = set()
E = set()
V_coord = { }
E_name = { }
V_vert = { }

# initialize digraph
graph = digraph.Digraph()

# process each line in the file
for line in digraph_file:

    # strip all trailing whitespace
    line = line.rstrip()

    fields = line.split(",")
    type = fields[0]

    if type == 'V':
        # got a vertex record
        (id,lat,long) = fields[1:]

        # vertex id's should be ints
        id=int(id)

        # lat and long are floats
        lat=float(lat)*100000 # convert to the expected format by multiplyin by 100000
        long=float(long)*100000

        V.add(id)
        V_coord[id] = (lat,long)
        V_vert[ (lat,long) ] = id # reference corresponding vertex given long lat

    elif type == 'E':
        # got an edge record
        (start,stop,name) = fields[1:]

        # vertices are ints
        start=int(start)
        stop=int(stop)
        e = (start,stop)

        # add edges to graph
        graph.add_edge((start, stop))

        # get rid of leading and trailing quote " chars around name
        name = name.strip('"')

        # consistency check, we don't want auto adding of vertices when
        # adding an edge.
        if start not in V or stop not in V:
            raise Exception("Edge {} has an endpoint that is not a vertex".format(e) )

        E.add(e)
        E_name[e] = name
    else:
        # weird input
        raise Exception("Error: weird line |{}|".format(line))

def cost(vtuple):
    """ 
    This computes the edge length to get from one coordinate to another.
    It does this by using the standard Pythagorean Theorem. This implies that 
    we are assuming the points in Edmonton are close enough together that 
    the geometry of the space is approximately Euclidean.

    Try out two vertices which have the same vertex id. The cost should be 0.0
    >>> cost( ( 29577354, 29577354) )
    0.0
    
    Try another few coordinates that are disjoint (I computed the distance by looking at
    the coordinates in the file and conifrming the result by hand).
    >>> cost( ( 29577354, 369898959) )
    19826.76691369523
    """
    
    # read the latitudes and longitudes from the coordinates from the text file
    lon1 = V_coord[vtuple[0]][0] 
    lat1 = V_coord[vtuple[0]][1]
    lon2 = V_coord[vtuple[1]][0]
    lat2 = V_coord[vtuple[1]][1]

    return math.sqrt( (lat2 - lat1)**2 + (lon2 - lon1)**2 )

def server( coords ):
    
    # permission variable to continue operations
    permission = False
        
    # check if input contains four arguments
    if len(coords) != 4:
        pass
            
    else:
        try:
            # extract the coordinates as floating points numbers
            lat1 = float(coords[0])
            lon1 = float(coords[1])
            lat2 = float(coords[2])
            lon2 = float(coords[3])

            permission = True # the input was valid!
        except ValueError:
            permission = False # the input was not valid!
                
            # right here turn the coords into the closest possible match with one in edmonton
            
        distance = float('inf') # set a tenative distance to be as far away as possible
            
            # iterate over all latitudes and longitudes in the graph
        for (x,y) in V_coord.values(): 
            # comput the pythagorean distance to that point
            crow_flies = math.sqrt( (x-lat1)**2 + (y-lon1)**2 )
            
            # if the current point is closer than the previous distance
            # reassign distance and store the points
            if crow_flies < distance:
                distance = crow_flies
                coords_in_file = (x, y)
            
        # save these new closer coordinates        
        lat1 = coords_in_file[0] 
        lon1 = coords_in_file[1]

        # repeat the same procedure for the second set of coordinates
        distance = float('inf')
        for (x,y) in V_coord.values():
            crow_flies = math.sqrt( (x-lat2)**2 + (y-lon2)**2 )
            if crow_flies < distance:
                distance = crow_flies
                coords_in_file = (x, y)

        # save these too!
        lat2 = coords_in_file[0]
        lon2 = coords_in_file[1]        
                    
        # carry out operations with vertices vert1 and vert2 
        # if permission given and they exist in our database
        if permission and ((lat1, lon1) in V_coord.values() and (lat2, lon2) in V_coord.values()):
                
            # below is the code for spitting out the coordinates found by the least_cost
            # path function
            vert1 = V_vert[(lat1, lon1)]
            vert2 = V_vert[(lat2, lon2)]
                
            dijkstra_list = dijkstra.least_cost_path(graph, vert1, vert2, cost)
             
            return dijkstra_list
                      
        else:
            print()

def main():
    args = parse_args()

    # Initialize some stuff...
    if args.serialport:
        print("Opening serial port: %s" % args.serialport)
        serial_out = serial_in =  serial.Serial(args.serialport, 9600)
    else:
        print("No serial port.  Supply one with the -s port option")
        exit()

    if args.verbose:
        debug = True
    else:
        debug = False

    while True:
        msg = receive(serial_in)

        debug and print("GOT:" + msg + ":", file=sys.stderr)

        fields = msg.split(" ");

        if len(fields) == 4:
                  
            # pass the server code the fields and have it
            # return the needed inputs for the client
            inputs = server(fields)

            # send the number of coordinates needed
            send(serial_out, str(len( inputs ))) 
            
            counter = 0
            while counter < len(inputs):
                # send the vertex positions
                send(serial_out, str(V_coord[inputs[counter]][0])+" "+str(V_coord[inputs[counter]][1]) )
                counter+=1

def send(serial_port, message):
    """
    Sends a message back to the client device.
    """
    full_message = ''.join((message, "\n"))

    (debug and
        print("server:" + full_message + ":") )

    reencoded = bytes(full_message, encoding='ascii')
    serial_port.write(reencoded)


def receive(serial_port, timeout=None):
    """
    Listen for a message. Attempt to timeout after a certain number of
    milliseconds.
    """
    raw_message = serial_port.readline()

    debug and print("client:", raw_message, ":")

    message = raw_message.decode('ascii')

    return message.rstrip("\n\r")



def parse_args():
    """
    Parses arguments for this program.
    Returns an object with the following members:
        args.
             serialport -- str
             verbose    -- bool
             graphname  -- str
    """

    parser = argparse.ArgumentParser(
        description='Assignment 1: Map directions.',
        epilog = 'If SERIALPORT is not specified, stdin/stdout are used.')
    parser.add_argument('-s', '--serial',
                        help='path to serial port',
                        dest='serialport',
                        default=None)
    parser.add_argument('-v', dest='verbose',
                        help='verbose',
                        action='store_true')
    parser.add_argument('-g', '--graph',
                        help='path to graph (DEFAULT = " edmonton-roads-2.0.1.txt")',
                        dest='graphname',
                        default=' edmonton-roads-2.0.1.txt')

    return parser.parse_args()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()

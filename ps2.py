# 6.0002 Problem Set 2 Fall 2020
# Graph Optimization
# Name:
# Collaborators:
# Time: 

#
# Finding shortest paths to drive from home to work on a road network
#

from graph import DirectedRoad, Node, RoadMap


# PROBLEM 2: Building the Road Network
#
# PROBLEM 2a: Designing your Graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
#Source and destination of a road represents node; Roads represent as edges. Times are represented as weight in minutes.  
#


# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a road map (graph).

    Parameters:
        map_filename : String
            name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by spaces:
            src_node dest_node travel_time road_type

        Note: mountain road types always are uphill in the source to destination direction and
              downhill in the destination to the source direction. Downhill travel takes
              half as long as uphill travel. The travel_time represents the time to travel 
              from source to destination (uphill).

        e.g.
            N0 N1 10 interstate
        This entry would become two directed roads; one from 'N0' to 'N1' on an interstate highway with 
        a weight of 10, and another road from 'N1' to 'N0' on an interstate using the same weight.

        e.g. 
            N2 N3 7 mountain 
        This entry would become to directed roads; one from 'N2' to 'N3' on a mountain road with 
        a weight of 7, and another road from 'N3' to 'N2' on a mountain road with a weight of 3.5.

    Returns:
        a directed road map representing the inputted map
    """
    file_handle=open(map_filename,'r')
    file_list=[]
    the_road_map=RoadMap()
    for line in file_handle:  #each line in the file is stored in a list
        file_list.append(line)
    for i in range(0,len(file_list)):
        templine=file_list[i]
        templine=templine.strip('\n')
        templine=templine.split(' ')
        if templine[3]=='mountain':  #if the data has mountain type downhil take half the time
            node_src=Node(templine[0])
            node_des=Node(templine[1])
            if not the_road_map.contains_node(node_src): #check if the node is already in the map
                the_road_map.insert_node(node_src)
                
            if not the_road_map.contains_node(node_des): #check if the node is already in the map
                the_road_map.insert_node(node_des)
            
            road_temp=DirectedRoad(node_src,node_des,float(templine[2]),templine[3]) #creating the road
            the_road_map.insert_road(road_temp)
            road_temp=DirectedRoad(node_des,node_src,float(templine[2])/2,templine[3]) #downhil takes half the time
            the_road_map.insert_road(road_temp)
        else:                               # non mountain type road; both way takes same time
            node_src=Node(templine[0])
            node_des=Node(templine[1])
            if not the_road_map.contains_node(node_src):#check if the node is already in the map
                the_road_map.insert_node(node_src)
                
            if not the_road_map.contains_node(node_des):#check if the node is already in the map
                the_road_map.insert_node(node_des)
            
            road_temp=DirectedRoad(node_src,node_des,float(templine[2]),templine[3]) #creating the road
            the_road_map.insert_road(road_temp)
            road_temp=DirectedRoad(node_des,node_src,float(templine[2]),templine[3]) #non mountains road take same time from either node
            the_road_map.insert_road(road_temp)
    
    return the_road_map
        
        

# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out after testing

# road_map = load_map("maps/test_load_map.txt") 



# PROBLEM 3: Finding the Shortest Path using Optimized Search Method



# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer: the sum of the edges of the nodes


# PROBLEM 3b: Implement find_optimal_path
def find_optimal_path(roadmap, start, end, restricted_roads, has_traffic=False):
    """
    Finds the shortest path between nodes subject to constraints.

    Parameters:
    roadmap - RoadMap
        The graph on which to carry out the search
    start - Node
        node at which to start
    end - Node
        node at which to end
    restricted_roads - list[strings]
        Road Types not allowed on path
    has_traffic - boolean
        flag to indicate whether to get shortest path during heavy or normal traffic 

    Returns:
    A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of nodes (Nodes).
        The second item is an number(float), the length (time traveled)
        of the best path.

    If there exists no path that satisfies constraints, then return None.
    """

    if not roadmap.contains_node(start) or not roadmap.contains_node(end):
        return None
    
    elif start==end:
        return ([start],0)
    else:
        # Mark all nodes unvisited and store them.
        # Set the distance to zero for our initial node 
        # and to infinity for other nodes.
        unvisited = roadmap.get_all_nodes()
        distanceTo = {node: float('inf') for node in roadmap.get_all_nodes()}
        distanceTo[start] = 0
        
        # Mark all nodes as not having found a predecessor node on path
        #from start
        predecessor = {node: None for node in roadmap.get_all_nodes()}
        
        while unvisited:
            # Select the unvisited node with the smallest distance from 
            # start, it's current node now.
            current = min(unvisited, key=lambda node: distanceTo[node])
            
             # Stop, if the smallest distance 
             # among the unvisited nodes is infinity.
            if distanceTo[current] == float('inf'):
                break
            
             # Find unvisited neighbors for the current node 
             # and calculate their distances from start through the
             # current node.
            for edge in roadmap.get_roads_starting_at_node(current):
                if edge.get_road_type() not in restricted_roads:
                    alternativePathDist = distanceTo[current] + edge.get_travel_time(has_traffic)
                    neighbour = edge.get_destination_node()
                    
                    # Compare the newly calculated distance to the assigned. 
                     # Save the smaller distance and update predecssor.
                    if alternativePathDist < distanceTo[neighbour]:
                        distanceTo[neighbour] = alternativePathDist
                        predecessor[neighbour] = current
            
            # Remove the current node from the unvisited set.
            unvisited.remove(current)
        
        #Attempt to be build a path working backwards from end
        path = []
        current = end
        while predecessor[current] != None:
            path.insert(0, current)
            current = predecessor[current]
        if path != []:
            path.insert(0, current)
            return (path,distanceTo[end])
        else:
            return None
                  

# PROBLEM 4a: Implement optimal_path_no_traffic
def optimal_path_no_traffic(filename, start, end):
    """
    Finds the shortest path from start to end during ideal traffic conditions.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end
    
    Returns:
    list of Node objects, the shortest path from start to end in normal traffic.
    If there exists no path, then return None.
    """
    road_map=load_map(filename)
    return find_optimal_path(road_map, start, end,[])[0]
    

# PROBLEM 4b: Implement optimal_path_restricted
def optimal_path_restricted(filename, start, end):
    """
    Finds the shortest path from start to end when local roads and mountain roads cannot be used.

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end
    
    Returns:
    list of Node objects, the shortest path from start to end given the aforementioned conditions,
    If there exists no path that satisfies constraints, then return None.
    """
    road_map=load_map(filename)
    return find_optimal_path(road_map, start, end,['local','mountain'])[0]
    

# PROBLEM 4c: Implement optimal_path_heavy_traffic
def optimal_path_heavy_traffic(filename, start, end):
    """
    Finds the shortest path from start to end in heavy traffic,
    i.e. when local roads take twice as long. 

    You must use find_optimal_path and load_map.

    Parameters:
    filename - name of the map file that contains the graph
    start - Node, node object at which to start
    end - Node, node object at which to end; you may assume that start != end
    
    Returns:
    The shortest path from start to end given the aforementioned conditions, 
    represented by a list of nodes (Nodes).

    If there exists no path that satisfies the constraints, then return None.
    """
    road_map=load_map(filename)
    return find_optimal_path(road_map, start, end,[],True)[0]
    
    
if __name__ == '__main__':
    # UNCOMMENT THE FOLLOWING LINES TO DEBUG
    # pass
    # rmap = load_map('maps/road_map.txt')
    rmap=load_map('maps/test_load_map.txt')
    print(rmap)
    
    # start = Node('N0')
    # end = Node('N9')
    # restricted_roads = ['']
    
    # print(find_optimal_path(rmap, start, end, restricted_roads))

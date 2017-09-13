INFINITY = float("inf")


def find_shortest_route(source, destination):
    '''
    Finds the shortest route between a source node and a destination node
    :param source: node to start at
    :param destination: node to finish at
    :return: a string containing the shortest path in the network from source to destination
    '''
    graph = init_graph()
    distances = init_distances()
    costs = init_costs(graph)
    parents = init_parents(graph)
    processed_nodes = []
    # Init the source node distance to itself as 0
    costs[source] = 0
    parents[source] = source
    current_node = get_min_node(costs, distances, processed_nodes, destination)

    while current_node is not None:
        cost_to_current_node = costs[current_node]  # Current cost to this node
        neighbors = graph[current_node]  # Get neighbors of current node
        relax_neighbors(cost_to_current_node, costs, current_node, neighbors, parents)  # Relax neighboring nodes
        processed_nodes.append(current_node)  # Add current node to processed nodes
        current_node = get_min_node(costs, distances, processed_nodes, destination)  # Get next node with shortest distance
    return display_shortest_route(parents, source, destination)


def init_graph():
    '''
    Initializes a graph with nodes and
    the corresponding neighbors.
    :return: graph
    '''
    graph = {}
    graph["A"] = {}
    graph["B"] = {}
    graph["C"] = {}
    graph["D"] = {}
    graph["E"] = {}

    '''
    Initialize neighbors
    '''
    # A
    graph["A"]["C"] = 6
    graph["A"]["B"] = 7
    # B
    graph["B"]["D"] = 2
    graph["B"]["E"] = 4
    # C
    graph["C"]["D"] = 5
    graph["C"]["E"] = 1
    # D
    graph["D"]["E"] = 4
    # E has no neighbors after it

    return graph


def init_costs(graph):
    '''
    Initializes the costs hash table for
    A* Search.
    :param: graph: the graph of the network of nodes
    :return: costs
    '''

    costs = {}
    # Init each value of costs as infinity
    for i in graph.keys():
        costs[i] = INFINITY
    return costs

def init_distances():
    distances = {}
    distances["A"] = {}
    distances["B"] = {}
    distances["C"] = {}
    distances["D"] = {}
    distances["E"] = {}

    # A
    distances["A"]["A"] = 0
    distances["A"]["C"] = 6
    distances["A"]["B"] = 7
    distances["A"]["D"] = 4
    distances["A"]["E"] = 3
    # B
    distances["B"]["B"] = 0
    distances["B"]["D"] = 2
    distances["B"]["E"] = 4
    distances["B"]["A"] = 7
    distances["B"]["C"] = 2
    # C
    distances["C"]["C"] = 0
    distances["C"]["D"] = 5
    distances["C"]["E"] = 1
    distances["C"]["A"] = 6
    distances["C"]["B"] = 4

    # D
    distances["D"]["D"] = 0
    distances["D"]["E"] = 4
    distances["D"]["A"] = 10
    distances["D"]["B"] = 8
    distances["D"]["C"] = 6

    # E
    distances["E"]["E"] = 0
    distances["E"]["A"] = 3
    distances["E"]["B"] = 7
    distances["E"]["C"] = 1
    distances["E"]["D"] = 4

    return distances


def init_parents(graph):
    '''
    Initializes the parent nodes of the shortest
    route, corresponding to the costs table for
    A* Search.
    :param graph:
    :return: parents
    '''
    parents = {}
    for i in graph.keys():
        parents[i] = None
    return parents


def distance_to_destination(distances, source, destination):
    '''
    Gives the heuristic distance from
    a node to the destination node.

    This will be built into PostGIS with real data.
    :return: distance to destination node heuristic
    '''

    return distances[source][destination]

def get_min_node(costs, distances, processed_nodes, destination):
    '''
    Returns the min node so far from costs
    :param costs:
    :param processed_nodes:
    :return: min_node
    '''
    min_node_cost = INFINITY  # Set current min to inf
    min_node = None  # Set current node to null
    for node in costs:  # For every node in costs
        # If the node is smaller than the current smallest AND the node has not yet been processed
        if costs[node] + distance_to_destination(distances, node, destination) < min_node_cost and node not in processed_nodes:
            # New current min node
            min_node_cost = costs[node]
            min_node = node
    return min_node


def relax_neighbors(cost_to_current_node, costs, current_node, neighbors, parents):
    '''
    Relaxing neighbors is the process of checking each neighbor of a node and updating
    our shortest costs if this new route is shorter.
    :param cost_to_current_node:
    :param costs:
    :param current_node:
    :param neighbors:
    :param parents:
    :return:
    '''
    for neighbor in neighbors:  # For each neighbor...
        new_distance_to_neighbor = cost_to_current_node + neighbors[neighbor]  # Get the new distance to this neighbor
        current_distance_to_neighbor = costs[neighbor]  # Get the current distance to this neighbor
        # If it is cheaper to go this way to this neighbor then add that as the shortest cost from the source
        if new_distance_to_neighbor < current_distance_to_neighbor:
            costs[neighbor] = new_distance_to_neighbor
            parents[neighbor] = current_node
            # We have now relaxed all of the current nodes neighbors


def display_shortest_route(parents, source, destination):
    '''
    Creates a shortest route string in easy to read
    language.
    :param parents: parent nodes
    :param source:  source node
    :param destination: destination node
    :return: a string with the shortest path from source to destination
    '''
    path = "->" + destination
    current_node = parents[destination]
    while current_node is not source:
        path = "->" + str(current_node) + path
        current_node = parents[current_node]
    return source + path
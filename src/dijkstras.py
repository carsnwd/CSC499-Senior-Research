import psycopg2

INFINITY = float("inf")


def find_shortest_route(source, destination):
    '''
    Finds the shortest route between a source node and a destination node
    :param source: node to start at
    :param destination: node to finish at
    :return: a string containing the shortest path in the network from source to destination
    '''
    graph = init_graph()
    costs = init_costs(graph)
    parents = init_parents(graph)
    processed_nodes = []
    # Init the source node distance to itself as 0
    costs[source] = 0
    parents[source] = source
    current_node = get_min_node(costs, processed_nodes)

    while current_node is not None:
        cost_to_current_node = costs[current_node]  # Current cost to this node
        neighbors = graph[current_node]  # Get neighbors of current node
        relax_neighbors(cost_to_current_node, costs, current_node, neighbors, parents)  # Relax neighboring nodes
        processed_nodes.append(current_node)  # Add current node to processed nodes
        if current_node == destination:
            break
        current_node = get_min_node(costs, processed_nodes)  # Get next node with shortest distance
    return display_shortest_route(parents, source, destination)


def init_graph():
    '''
    Initializes a graph with nodes and
    the corresponding neighbors.
    :return: graph
    '''
    graph = {}
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT id FROM ways_vertices_pgr')
    row = cur.fetchone()
    while row:
        graph[float(row[0])] = {}
        row = cur.fetchone()

    cur.execute('SELECT source, target, length_m FROM ways')
    row = cur.fetchone()
    while row:
        c1 = float(row[0])
        c2 = float(row[1])
        # print "c1: " + str(c1)
        # print "c2: " + str(c2)
        graph[c1][c2] = float(row[2])
        row = cur.fetchone()

    return graph


def connect_to_database():
    '''
    Establishes connection with database.
    :return: conn
    '''
    # Read password in from config
    with open("../sensitive.config") as f:
        content = f.readlines()
    password = [x.strip() for x in content]

    # Establish connection
    try:
        conn = psycopg2.connect(
            "dbname='connecticut' user='postgres' host='localhost' password='" + password.__getitem__(0) + "'")
        return conn
    except:
        print "I am unable to connect to the database"
        print "dbname='connecticut' user='postgres' host='localhost' password='" + password.__getitem__(0) + "'"


def init_costs(graph):
    '''
    Initializes the costs hash table for
    Dijkstra's algorithm.
    :param: graph: the graph of the network of nodes
    :return: costs
    '''

    costs = {}
    # Init each value of costs as infinity
    for i in graph.keys():
        costs[i] = INFINITY
    return costs


def init_parents(graph):
    '''
    Initializes the parent nodes of the shortest
    route, corresponding to the costs table for
    Dijkstra's Algorithm.
    :param graph:
    :return: parents
    '''
    parents = {}
    for i in graph.keys():
        parents[i] = None
    return parents


def get_min_node(costs, processed_nodes):
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
        if costs[node] < min_node_cost and node not in processed_nodes:
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
    path = str(destination)
    current_node = parents[destination]
    while current_node is not source:
        path = str(current_node) + " -> " + str(path)
        current_node = parents[current_node]
    return str(path)

print find_shortest_route(22029, 37579)
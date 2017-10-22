import psycopg2
import shapely.wkb
from shapely.geometry import LineString
from shapely.ops import linemerge
import datetime
import time

INFINITY = float("inf")


def find_shortest_route(source, destinations):
    '''
    Finds the shortest route between a source node and a destination node
    :param source: node to start at
    :param destination: node to finish at
    :return: a string contai
    ning the shortest path in the network from source to destination
    '''
    id = datetime.datetime.now().strftime("%I%M%S%p%B%d%Y") #Use current exact time as ID
    start = time.time()
    destinations_left = destinations[:]
    shortest_routes = []
    for destination in destinations_left:
        graph = init_graph()
        costs = init_costs(graph)
        parents = init_parents(graph)
        processed_nodes = []
        # Init the source node distance to itself as 0
        costs[source] = 0
        parents[source] = source
        current_node = get_min_node(costs, processed_nodes, destination)

        while current_node is not None:
            cost_to_current_node = costs[current_node]  # Current cost to this node
            neighbors = graph[current_node]  # Get neighbors of current node
            relax_neighbors(cost_to_current_node, costs, current_node, neighbors, parents, destination)  # Relax neighboring nodes
            processed_nodes.append(current_node)  # Add current node to processed nodes
            if current_node == destination:
                break
            current_node = get_min_node(costs, processed_nodes, destination)  # Get next node with shortest distance
        destinations_left.remove(destination)
        shortest_routes.append(display_shortest_route(parents, source, destination))
    end = time.time()
    total_time = end - start
    return generate_results_to_database(shortest_routes, total_time, id)


def init_graph():
    '''
    Initializes a graph with nodes and
    the corresponding neighbors.
    :return: graph
    '''
    graph = {}
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT osm_id FROM ways_vertices_pgr')
    row = cur.fetchone()
    while row:
        graph[float(row[0])] = {}
        row = cur.fetchone()

    cur.execute('SELECT source_osm, target_osm, length FROM ways')
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
    A* Search.
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
    A* Search.
    :param graph:
    :return: parents
    '''
    parents = {}
    for i in graph.keys():
        parents[i] = None
    return parents


def distance_to_destination(source, destination):
    '''
    Gives the heuristic distance from
    a node to the destination node.

    Extracts the lon and lat coordinates from hte point in the ways db
    given the id of the source and destination points. Using PostGIS built
    in ST_Distance, it gets the euclidean distance in meters from the source to destination.
    :return: distance to destination node heuristic
    '''

    source = int(source)
    destination = int(destination)
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute('SELECT lon, lat FROM ways_vertices_pgr WHERE osm_id =' + str(source))
    source_coords = cur.fetchone()
    cur.execute('SELECT lon, lat FROM ways_vertices_pgr WHERE osm_id =' + str(destination))
    destination_coords = cur.fetchone()

    cur.execute("SELECT ST_Distance(ST_GeomFromText('POINT(" + str(source_coords[0]) + " " + str(
        source_coords[1]) + ")', 4326),ST_GeomFromText('POINT(" + str(destination_coords[0]) + " " + str(
        destination_coords[1]) + ")', 4326))")
    distance = cur.fetchone()

    return float(distance[0])


def get_min_node(costs, processed_nodes, destination):
    '''
    Returns the min node so far from costs
    :param costs:
    :param processed_nodes:
    :return: min_node
    '''
    min_node_cost = INFINITY  # Set current min to inf
    min_node = None  # Set current node to null
    destination = float(destination)
    for node in costs:  # For every node in costs
        # print "min_node_cost:   " + str(min_node_cost)
        if costs[node] < min_node_cost and node not in processed_nodes:
            # New current min node
            min_node_cost = costs[node]
            min_node = node
    return min_node


def relax_neighbors(cost_to_current_node, costs, current_node, neighbors, parents, destination):
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
        new_distance_to_neighbor = cost_to_current_node + (neighbors[neighbor] + distance_to_destination(neighbor, destination)) # Get the new distance to this neighbor
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
    :param destinations: destination node
    :return: a string with the shortest path from source to destination
    '''
    shortest_routes = []
    points_of_line = []
    points_of_line.append(destination)
    current_node = parents[destination]
    while current_node is not source:
        points_of_line.append(current_node)
        current_node = parents[current_node]
        shortest_routes.append(points_of_line)
    return create_shortest_route_geom(points_of_line)


def generate_results_to_database(shortest_route_geoms, total_time, id):
    conn = connect_to_database()
    cur = conn.cursor()
    index_of_shortest_geom = 0
    shortest_length = 0
    for index, route_geom in enumerate(shortest_route_geoms):
        if route_geom.length <= shortest_length:
            index_of_shortest_geom = index
    hex_shortest_route_geom = LineString(shortest_route_geoms[index_of_shortest_geom]).wkb_hex
    insert_query = """INSERT INTO public.results_astar_one_to_one(the_geom, total_time, id) VALUES (st_geomfromwkb(%(geom)s::geometry, 4326), %(total_time)s, %(id)s)"""
    cur.execute(insert_query, {'geom': hex_shortest_route_geom, 'total_time': total_time, 'id': id})
    conn.commit()
    return shortest_route_geoms[index_of_shortest_geom], total_time, id

def create_shortest_route_geom(route):
    '''
    Exports the shortest route as a GIS geom to display in QGIS, along with time and id for analysis purposes
    :param shortest_routes:
    :param total_time:
    :param id:
    :return:
    '''
    conn = connect_to_database()
    cur = conn.cursor()
    lines = []
    total_geom = None
    for index, node in enumerate(route):
        try:
            source = str(int(node))
            target = str(int(route[index + 1]))
            query = 'SELECT the_geom FROM public.ways WHERE target_osm = ' + target + ' AND source_osm = ' + source + ' OR target_osm = ' + source + ' AND source_osm = ' + target + ';'
            cur.execute(query)
            hex_geom = cur.fetchone()
            geom = shapely.wkb.loads(hex_geom[0], hex=True)
            lines.append(geom)
        except IndexError:
            print "Last element"
        total_geom = linemerge(lines)
    return total_geom

print(find_shortest_route(83917069, [83958535]))
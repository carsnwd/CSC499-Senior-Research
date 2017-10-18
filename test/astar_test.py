import unittest
import src.astar as astar


class TestGraphAStar(unittest.TestCase):
    def test_graph_initialization(self):
        graph = astar.init_graph()
        self.assertIsNotNone(graph)
        self.assertEquals(graph[60642422][60642896], 0.000192337879785143)
        self.assertEquals(graph.__len__(), 240188)

    def test_database_connection(self):
        conn = astar.connect_to_database()
        self.assertIsNotNone(conn)
        cur = conn.cursor()
        cur.execute('SELECT x1,y1 FROM ways')
        row = cur.fetchone()
        print str(float(row[0])) + str(",") + str(float(row[1]))
        self.assertEquals(float(row[0]), -73.4418006)
        self.assertEquals(float(row[1]), 41.0593617)

    def test_costs_initialization(self):
        graph = astar.init_graph()
        costs = astar.init_costs(graph)
        infinity = float("inf")
        # Test all are init to infinity
        for i in costs:
            self.assertEquals(costs[i], infinity)
        self.assertEquals(graph[60642422], {1900216568: 0.000596244412977484, 60642896: 0.000192337879785143})
        # Test getting neighbor label works
        self.assertEquals(graph[60642422].keys(), [1900216568.0, 60642896.0])
        # Test getting edge to neighbor weight is valid
        self.assertEquals(graph[60642422][graph[60642422].keys()[0]], 0.000596244412977484)

    def test_get_distance(self):
        self.assertEquals(astar.distance_to_destination(60642422, 83997901), 0.0658882536679388)

    def test_astar(self):
        self.assertEquals(astar.find_shortest_route(60642422, [60642896]), [[60642896, 60642422.0]])
        self.assertEquals(astar.find_shortest_route(60642422, [60642900]), [[60642900, 60642896.0, 60642422.0]])

if __name__ == '__main__':
    unittest.main()

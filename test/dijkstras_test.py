import unittest
import src.dijkstras as dijkstra


class TestGraphDijkstras(unittest.TestCase):
    def test_graph_initialization(self):
        graph = dijkstra.init_graph()
        self.assertIsNotNone(graph)
        self.assertEquals(graph[60642422][60642896], 0.000192337879785143)
        self.assertEquals(graph.__len__(), 240188)

    def test_database_connection(self):
        conn = dijkstra.connect_to_database()
        self.assertIsNotNone(conn)
        cur = conn.cursor()
        cur.execute('SELECT x1,y1 FROM ways')
        row = cur.fetchone()
        print str(float(row[0])) + str(",") + str(float(row[1]))
        self.assertEquals(float(row[0]), -73.5419236)
        self.assertEquals(float(row[1]), 41.3891845)

    def test_costs_initialization(self):
        graph = dijkstra.init_graph()
        costs = dijkstra.init_costs(graph)
        infinity = float("inf")
        # Test all are init to infinity
        for i in costs:
            self.assertEquals(costs[i], infinity)
        self.assertEquals(graph[60642422], {60642896: 0.000192337879785143, 1900216568: 0.000596244412977484})
        # Test getting neighbor label works
        self.assertEquals(graph[60642422].keys(), [60642896.0, 1900216568.0])
        # Test getting edge to neighbor weight is valid
        self.assertEquals(graph[60642422][graph[60642422].keys()[0]], 0.000192337879785143)

    def test_dijkstras(self):
        self.assertEquals(dijkstra.find_shortest_route(60642422, [60642896]), [[60642896, 60642422.0]])
        self.assertEquals(dijkstra.find_shortest_route(60642422, [60642900]), [[60642900, 60642896.0, 60642422.0]])

if __name__ == '__main__':
    unittest.main()
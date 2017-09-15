import unittest
import src.dijkstras as dijkstra


class TestGraphDijkstras(unittest.TestCase):
    def test_graph_initialization(self):
        graph = dijkstra.init_graph()
        self.assertIsNotNone(graph)
        self.assertEquals(graph[22029][35820], 20.86742605803)
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

    # def test_costs_initialization(self):
    #     graph = dijkstra.init_graph()
    #     costs = dijkstra.init_costs(graph)
    #     infinity = float("inf")
    #     # Test all are init to infinity
    #     for i in costs:
    #         self.assertEquals(costs[i], infinity)
    #     self.assertEquals(graph["A"], {'C': 6, 'B': 7})
    #     # Test getting neighbor label works
    #     self.assertEquals(graph["A"].keys(), ['C', 'B'])
    #     # Test getting edge to neighbor weight is valid
    #     self.assertEquals(graph["A"][graph["A"].keys()[0]], 6)

    # def test_dijkstras(self):
    #     self.assertEquals(dijkstra.find_shortest_route("A","B"), "A->B")
    #     self.assertEquals(dijkstra.find_shortest_route("A","C"), "A->C")
    #     self.assertEquals(dijkstra.find_shortest_route("A","D"), "A->B->D")
    #     self.assertEquals(dijkstra.find_shortest_route("A","E"), "A->C->E")

if __name__ == '__main__':
    unittest.main()

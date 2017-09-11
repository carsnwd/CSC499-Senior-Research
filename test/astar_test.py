import unittest
import src.astar as astar


class TestGraphAStar(unittest.TestCase):
    def test_graph_initialization(self):
        graph = astar.init_graph()
        self.assertEquals(graph["A"]["C"], 6)
        self.assertEquals(graph["A"]["B"], 7)
        self.assertEquals(graph["C"]["D"], 5)
        self.assertNotEqual(graph["B"]["E"], 2)
        self.assertEquals(graph.__len__(), 5)

    def test_costs_initialization(self):
        graph = astar.init_graph()
        costs = astar.init_costs(graph)
        infinity = float("inf")
        # Test all are init to infinity
        for i in costs:
            self.assertEquals(costs[i], infinity)
        self.assertEquals(graph["A"], {'C': 6, 'B': 7})
        # Test getting neighbor label works
        self.assertEquals(graph["A"].keys(), ['C', 'B'])
        # Test getting edge to neighbor weight is valid
        self.assertEquals(graph["A"][graph["A"].keys()[0]], 6)

    def test_init_distances(self):
        graph = astar.init_graph()
        costs = astar.init_costs(graph)
        infinity = float("inf")
        distances = astar.init_distances()
        # Test all are init to infinity
        self.assertEquals(distances["B"]["A"], 7)

    def test_dijkstras(self):
        self.assertEquals(astar.find_shortest_route("A", "B"), "A->B")
        self.assertEquals(astar.find_shortest_route("A", "C"), "A->C")
        self.assertEquals(astar.find_shortest_route("A", "D"), "A->B->D")
        self.assertEquals(astar.find_shortest_route("A", "E"), "A->C->E")

if __name__ == '__main__':
    unittest.main()

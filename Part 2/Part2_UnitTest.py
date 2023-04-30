import unittest
from Part2_Graph import Graph

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_node('A')
        self.graph.add_node('B')
        self.graph.add_node('C')
        self.graph.add_node('D')
        self.graph.add_node('E')
        self.graph.add_edge('A', 'B', 1)
        self.graph.add_edge('A', 'C', 1)
        self.graph.add_edge('A', 'E', 1)
        self.graph.add_edge('B', 'C', 1)
        self.graph.add_edge('B', 'E', 1)
        self.empty_graph = Graph()

    def test_is_empty(self):
        self.assertTrue(self.empty_graph.is_empty)
        self.assertFalse(self.graph.is_empty)

    def test_num_nodes(self):
        self.assertEqual(self.empty_graph.num_nodes, 0)
        self.assertEqual(self.graph.num_nodes, 5)

    def test_num_edges(self):
        self.assertEqual(self.empty_graph.num_edges, 0)
        self.assertEqual(self.graph.num_edges, 5)

    def test_nodes(self):
        self.assertCountEqual(self.empty_graph.nodes, [])
        self.assertCountEqual(self.graph.nodes, ['A', 'B', 'C', 'D', 'E'])

    def test_edges(self):
        self.assertCountEqual(self.empty_graph.edges, [])
        edge_strings = [str(edge) for edge in self.graph.edges]
        self.assertCountEqual(edge_strings, ['A - B: 1', 'A - C: 1', 'A - E: 1', 'B - C: 1', 'B - E: 1'])

    def test_neighbors(self):
        self.assertCountEqual(self.graph.neighbors('A'), ['B', 'C', 'E'])
        self.assertCountEqual(self.graph.neighbors('D'), [])

    def test_adjacent(self):
        self.assertTrue(self.graph.adjacent('A', 'B'))
        self.assertFalse(self.graph.adjacent('A', 'D'))

if __name__ == '__main__':
    unittest.main()

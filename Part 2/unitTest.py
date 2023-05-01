import unittest
from graph import Graph
from shortest_path import ShortestPathBase, Dijkstra, A_Star

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_node('A')
        self.graph.add_node('B')
        self.graph.add_node('C')
        self.graph.add_node('D')
        self.graph.add_node('E')
        self.graph.add_edge('A', 'B', 1)
        self.graph.add_edge('A', 'C', 2)
        self.graph.add_edge('A', 'E', 3)
        self.graph.add_edge('B', 'C', 4)
        self.graph.add_edge('B', 'E', 5)
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
        self.assertCountEqual(edge_strings, ['A - B: 1', 'A - C: 2', 'A - E: 3', 'B - C: 4', 'B - E: 5'])

    def test_neighbors(self):
        self.assertCountEqual(self.graph.neighbors('A'), ['B', 'C', 'E'])
        self.assertCountEqual(self.graph.neighbors('D'), [])

    def test_adjacent(self):
        self.assertTrue(self.graph.adjacent('A', 'B'))
        self.assertFalse(self.graph.adjacent('A', 'D'))


class TestShortestPathAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.graph = Graph()
        self.graph.add_node('A')
        self.graph.add_node('B')
        self.graph.add_node('C')
        self.graph.add_node('D')
        self.graph.add_node('E')
        self.graph.add_edge('A', 'B', 5)
        self.graph.add_edge('B', 'C', 3)
        self.graph.add_edge('A', 'C', 9)
        self.graph.add_edge('C', 'D', 2)
        self.graph.add_edge('D', 'E', 4)
        self.graph.add_edge('E', 'A', 7)
        self.graph.get_node('A').add_data('pos', (0, 0))
        self.graph.get_node('B').add_data('pos', (3, 4))
        self.graph.get_node('C').add_data('pos', (6, 0))
        self.graph.get_node('D').add_data('pos', (9, 4))
        self.graph.get_node('E').add_data('pos', (12, 0))

    def test_initialization(self):
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        a_star = A_Star(self.graph, 'A', 'E')

        self.assertIsInstance(dijkstra, Dijkstra)
        self.assertIsInstance(dijkstra, ShortestPathBase)
        self.assertIsInstance(a_star, A_Star)
        self.assertIsInstance(a_star, ShortestPathBase)

    def test_graph_input_validation(self):
        with self.assertRaises(AssertionError):
            Dijkstra(self.graph, 'Z', 'E')
        with self.assertRaises(AssertionError):
            A_Star(self.graph, 'A', 'Z')

    def test_shortest_path_calculation(self):
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        a_star = A_Star(self.graph, 'A', 'E')

        self.assertEqual(dijkstra.shortest_path, ['A', 'E'])
        self.assertEqual(a_star.shortest_path, ['A', 'E'])
        self.assertEqual(dijkstra.shortest_distance, 7)
        self.assertEqual(a_star.shortest_distance, 7)

    def test_heuristic_calculation(self):
        a_star = A_Star(self.graph, 'A', 'E')
        distance = a_star._distance_to_target(self.graph.get_node('A'))
        self.assertEqual(distance, 12)

    def test_initialize_priority_queue(self):
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        a_star = A_Star(self.graph, 'A', 'E')

        self.assertEqual(len(dijkstra._priority_queue), len(self.graph.nodes))
        self.assertEqual(len(a_star._priority_queue), len(self.graph.nodes))

    def test_update_priority_queue(self):
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        a_star = A_Star(self.graph, 'A', 'E')

        dijkstra._update_priority_queue(10, self.graph.get_node('B'), self.graph.get_node('A'))
        a_star._update_priority_queue(10, self.graph.get_node('B'), self.graph.get_node('A'))

        self.assertEqual(dijkstra.priority_queue[1][1], 10)
        self.assertEqual(a_star.priority_queue[1][1], 10)

    def test_get_unvisited_neighbors(self):
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        neighbors = dijkstra._get_unvisited_neighbors(self.graph.get_node('A'))
        self.assertEqual(neighbors, {'B', 'C', 'E'})


if __name__ == '__main__':
    unittest.main()

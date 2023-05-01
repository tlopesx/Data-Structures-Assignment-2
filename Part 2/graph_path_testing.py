import unittest
from graph import Graph
from shortest_path import Dijkstra, A_Star

class TestGraph(unittest.TestCase):
    def setUp(self):
        # Construct a test graph
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
        # Construct an empty graph
        self.empty_graph = Graph()

    def test_is_empty(self):
        # Checks that is_empty returns true for the empty graph and false for the other graph
        self.assertTrue(self.empty_graph.is_empty)
        self.assertFalse(self.graph.is_empty)

    def test_num_nodes(self):
        # Checks that num_nodes returns 0 for the empty graph and 5 for the other graph
        self.assertEqual(self.empty_graph.num_nodes, 0)
        self.assertEqual(self.graph.num_nodes, 5)

    def test_num_edges(self):
        # checks that num_edges returns 0 for the empty graph and 5 for the other graph
        self.assertEqual(self.empty_graph.num_edges, 0)
        self.assertEqual(self.graph.num_edges, 5)

    def test_nodes(self):
        # Check that nodes returns an empty list for the empty graph, and the list of nodes for the other graph
        self.assertCountEqual(self.empty_graph.nodes, [])
        self.assertCountEqual(self.graph.nodes, ['A', 'B', 'C', 'D', 'E'])

    def test_edges(self):
        # Check that the edges function returns an empty list for the empty graph and the list of edges we constructed for the other graph
        self.assertCountEqual(self.empty_graph.edges, [])
        edge_strings = [str(edge) for edge in self.graph.edges]
        self.assertCountEqual(edge_strings, ['A - B: 1', 'A - C: 1', 'A - E: 1', 'B - C: 1', 'B - E: 1'])

    def test_neighbors(self):
        # Check that neighbors function for A returns B, C, and E, and that it returns an empty list for D
        self.assertCountEqual(self.graph.neighbors('A'), ['B', 'C', 'E'])
        self.assertCountEqual(self.graph.neighbors('D'), [])

    def test_adjacent(self):
        # Check that the adjacent function returns true for A -> B and False for A -> D
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

    def test_graph_input_validation(self):
        # Check that an assertion error is raised if we try to find the shortest path between edges that don't exist
        with self.assertRaises(AssertionError):
            Dijkstra(self.graph, 'Z', 'E')
        with self.assertRaises(AssertionError):
            A_Star(self.graph, 'A', 'Z')

    def test_shortest_path_calculation(self):
        # Checks that the shortest path in the graph is A -> E, and the distance is 7
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        a_star = A_Star(self.graph, 'A', 'E')
        self.assertEqual(dijkstra.shortest_path, ['A', 'E'])
        self.assertEqual(a_star.shortest_path, ['A', 'E'])
        self.assertEqual(dijkstra.shortest_distance, 7)
        self.assertEqual(a_star.shortest_distance, 7)

    def test_heuristic_calculation(self):
        # Checks that the heuristic distance calculated between A and E is 12 
        a_star = A_Star(self.graph, 'A', 'E')
        distance = a_star._distance_to_target(self.graph.get_node('A'))
        self.assertEqual(distance, 12)

    def test_initialize_priority_queue(self):
        # Checks that the length of the priority queue is equal to the length of the list of nodes.
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        a_star = A_Star(self.graph, 'A', 'E')
        self.assertEqual(len(dijkstra._priority_queue), len(self.graph.nodes))
        self.assertEqual(len(a_star._priority_queue), len(self.graph.nodes))

    def test_get_unvisited_neighbors(self):
        # Checks that the list of unvisited neighbors of A is B, C, and D.
        dijkstra = Dijkstra(self.graph, 'A', 'E')
        neighbors = dijkstra._get_unvisited_neighbors(self.graph.get_node('A'))
        self.assertEqual(neighbors, {'B', 'C', 'E'})
class Graph:
    '''Class that contains an adjacency map representation of a Graph'''

    class Node:
        def __init__(self, name):
            '''Initialize a new node'''
            self.name = name
            self._edges = {}
            # Data property for storing additional information on the node
            # For example, position
            self.data = {}

        def __eq__(self, other):
            '''Two nodes are considered equal if they have the same name'''
            if self.name == other.name:
                return True
            else:
                return False
                       
        def __repr__(self):
            '''Print the name of the node'''
            return str(self.name)
            
        def _add_edge(self, edge):
            '''Add an edge to the node's list of edges'''
            if edge.node1 == self:
                self._edges[edge.node2.name] = edge
            elif edge.node2 == self:
                self._edges[edge.node1.name] = edge

        def _remove_edge(self, edge):
            '''Remove an edge from the node's list of edges'''
            if edge.node1 == self:
                del self._edges[edge.node2.name]
            elif edge.node2 == self:
                del self._edges[edge.node1.name]

        def get_edges(self):
            '''Return all edges connected to the node'''
            return list(self._edges.values())
        
        def get_adjacent_nodes(self):
            '''Return the names of all nodes connected to the edge'''
            return list(self._edges.keys()) 

        def add_data(self, key, value):
            '''Adds a custom additional property to the node'''
            self.data[key] = value

        def get_data(self, key):
            '''Access a custom additional property of the node'''
            return self.data[key]





    class Edge:
        def __init__(self, node1, node2, weight):
            '''Initialize a new edge'''
            assert node1 != node2, "Edge cannot have the same start and end node"
            self.node1 = node1
            self.node2 = node2
            self.weight = weight

        def __eq__(self, other):
            '''Two edges are considered equal if they have the same two nodes'''
            if (self.node1 == other.node1 and self.node2 == other.node2):
                return True
            elif (self.node1 == other.node2 and self.node2 == other.node1):
                return True
            else:
                return False
            
        def __hash__(self):
            '''Use a frozenset (order does not matter) to hash the edge'''
            nodes = frozenset([self.node1.name, self.node2.name])
            return hash(nodes)
        
        def __repr__(self):
            '''Print the nodes and weight of the edge'''
            return f'{self.node1} - {self.node2}: {self.weight}'
            
          
    def __init__(self):
        '''Initialize a new graph with a list of nodes and edges'''
        self._nodes = {}
        self._edges = {}

    @property
    def is_empty(self):
        '''Returns true if a graph has no edges'''
        return len(self._nodes) == 0
        
    @property
    def num_nodes(self):
        '''Returns the number of nodes associated with the graph'''
        return len(self._nodes)
    
    @property
    def num_edges(self):
        '''Returns the number of edges associated with the graph'''
        return len(self._edges)

    @property
    def nodes(self):
        '''Returns the list of nodes in the graph'''
        return list(self._nodes.keys())
    
    @property
    def edges(self):
        '''Returns the list of nodes in the graph'''
        return list(self._edges.values())
    
    @property
    def adjacency_map(self):
        '''Returns the adjacency map of the graph'''
        # Create an empty list for the adjacency map
        adjacency_map = []
        # Loop through all of the nodes and add their adjacent nodes to the list
        for node in list(self._nodes.values()):
            adjacency_map.append(node.get_adjacent_nodes())
        # Return the list of adjacencies
        return adjacency_map

    def add_node(self, nodeName):
        '''Creates a new node if it does not already exist and adds it to the graph'''
        # Check if the node is not in the list of nodes
        if nodeName not in self._nodes.keys():
            self._nodes[nodeName] = self.Node(nodeName)
        return self._nodes[nodeName]

    def get_node(self, nodeName):
        '''Retrieves the node object with a specified name in a graph'''
        assert nodeName in self._nodes.keys(), "Node does not exist in graph"
        return self._nodes[nodeName]

    def add_edge(self, node1, node2, weight):
        '''Creates a new edge if it does not already exist and adds it to the graph.
         Creates either of the nodes and adds them to the graph if they do not already exist. '''
        # Adds nodes to node list if not already there
        node1 = self.add_node(node1)
        node2 = self.add_node(node2)
        # Creates an Edge between the two nodes with the weight
        new_edge = self.Edge(node1, node2, weight)
        
        # Check that there's an already an edge between the two nodes
        if new_edge not in self._edges:
            # Add the edge to the list of edges and add the edge to the list of edges for each node
            self._edges[new_edge] = new_edge
            self._nodes[node1.name]._add_edge(new_edge)
            self._nodes[node2.name]._add_edge(new_edge)
        
        else:
            # If there is already an edge, update the weight
            self._edges[new_edge].weight = new_edge.weight
            self._nodes[node1.name]._edges[node2] = new_edge.weight
            self._nodes[node2.name]._edges[node1] = new_edge.weight

    def get_edge(self, node1, node2):
        '''Retrieves the edge object with a specified nodes in a graph'''
        lookup_edge = self.Edge(node1, node2, 1)
        assert lookup_edge in self._edges.keys(), "Edge does not exist in graph"
        return self._edges[lookup_edge]

    def adjacent(self, node1, node2):
        '''Checks whether two nodes share an edge'''
        return node2 in self._nodes[node1].get_adjacent_nodes()
    
    def neighbors(self, node):
        '''Returns a list of all nodes that are adjacent to a node'''
        return self._nodes[node].get_adjacent_nodes()
    
    def remove_node(self, nodeToRemove):
        '''Removes a node and all edges associated with it'''
        # Get the edges connected to the node to be removed
        edges_to_remove = self._nodes[nodeToRemove].get_edges()

        # Remove the node from the list of nodes
        del self._nodes[nodeToRemove]
        
        # Remove the edges from the list of edges and from the adjacency lists of adjacent nodes
        for edge in edges_to_remove:
            # Remove the edge from the graph's list of edges
            del self._edges[edge]
            # Check which node of the edge is being removed
            if edge.node1 != nodeToRemove:
                # Remove the edge from the first node's list of edges if it's the second
                del self._nodes[edge.node1.name]._edges[edge.node2.name]
            if edge.node2.name != nodeToRemove:
                # Remove the edge from the first node's list of edges if it's the second
                del self._nodes[edge.node2.name]._edges[edge.node1.name]
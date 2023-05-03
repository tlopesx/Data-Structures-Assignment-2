from graph import Graph
import math
from tabulate import tabulate

class ShortestPathBase():
    def __init__(self, graph, start_node, end_node, log=False):
        assert start_node in graph.nodes, "Start node must be a node in the Graph"
        self.graph = graph
        self.start_node = self.graph.get_node(start_node)
        self.end_node = self.graph.get_node(end_node)
        self._current_node = self.graph.get_node(start_node)
        self._priority_queue = self._initialize_priority_queue()
        self._visited = {}
        self.__log = log

    # Define an "abstract" method to define the priority queue to be used in the path finding algorithm
    def _initialize_priority_queue(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    # Define an "abstract" method to define an update function for the priority queue based on the algorithm
    def _update_priority_queue(self):
        raise NotImplementedError("Subclasses must implement this method")

    @property
    def priority_queue(self):
        '''Returns a version of the priority queue sorted by distance'''
        # Sort the entries of the priority queue by their total distance
        self._priority_queue.sort(key=lambda queue_object: queue_object[self._queue_sort_by_index])
        return self._priority_queue
    
    @property
    def __visited(self):
        '''Returns the names of the already visited elements as a set'''
        # Get the keys of all entries in the priority queue
        return set(self._visited.keys())
    
    
    def dequeue(self):
        '''Removes the top entry from the priority queue and adds it to the dictionary of visited elements'''
        # Pop the element off the queue and an entry in the visited dictionary
        element = self.priority_queue.pop(0)
        self._visited[element[0].name] = element
        
        return element
    
    def _get_unvisited_neighbors(self, node):
        '''Gets the set of unvisited neighbors of the current element'''
        # Get unvisited neighbors by subtracting the set of visited nodes from the set of neighbors
        current_neighbors = set(node.get_adjacent_nodes())
        unvisited_neighbors = current_neighbors - self.__visited
        
        return unvisited_neighbors
    
    def _shortest_paths(self):
        '''Calculates the shortest path between the start node and every other node'''
        counter = 1
        # While there are nodes in the priority queue
        while self.priority_queue:

            if self.__log == True:
                # Print the queues
                self._print_queues(counter)
                # Increment the counter
                counter += 1

            # Grab the first element
            current_element = self.dequeue()
            current_node = current_element[0]
            current_distance = current_element[1]
    
            # Get the previously unvisited neighbors of the element being visited
            unvisited_neighbors = self._get_unvisited_neighbors(current_node)
            
            # Update the priority queue to reflect the distances 
            for neighbor in unvisited_neighbors:
                neighbor = self.graph.get_node(neighbor)
                distance = self.graph.get_edge(current_node, neighbor).weight + current_distance
                self._update_priority_queue(distance, neighbor, current_node)
            
    def _print_queues(self, counter):
       
        # Get the visited key list
        visited_key_list = list(self._visited.keys())

        priority_queue_len = len(self._priority_queue)
        visited_len = len(visited_key_list)

        print_length = max(priority_queue_len, visited_len)

        # Check if there are any elements in the u
        if print_length > 0:
            # Print headers
            print("Step", counter)
            table_data = []
           
            # Loop through the elements of the priority queue
            for i in range(print_length):
                # Print nothing if there is nothing in the visited list
                if i >= visited_len:
                    visited = ""
                else:
                    visited = self._visited[visited_key_list[i]]

                if i >= priority_queue_len:
                    queue = "\t\t"
                else:
                    queue = self._priority_queue[i]

                table_data.append((queue, visited))

            print(tabulate(table_data, headers=['Priority Queue', 'Visited List'], tablefmt="grid"))
                
            print()

    @property     
    def shortest_path(self):
        '''Displays the shortest path between the start node and the end node'''
        # Initialize a path list to store the path taken to the end_node
        path = [self.end_node.name]
        # Call the shortest path method which performs the algorithm to find the shortest paths
        self._shortest_paths()
        # Start at the end
        current_node = self.end_node
        
        # Loop through the nodes until we get back to the beginning,
        # adding the names of the elements to the path as we go
        while current_node != self.start_node:
            previous_node = self._visited[current_node.name][2]
            path.append(previous_node.name)
            current_node = previous_node
        
        # Reverse the list so that it displays the start at the start and the end at the end
        path.reverse()
        
        return path
    
    @property
    def shortest_distance(self):
        '''Gets the total distance from the start node to the end node'''
        self._shortest_paths()
        
        return self._visited[self.end_node.name][1]
    
class Dijkstra(ShortestPathBase):
    def __init__(self, graph, start_node, end_node, log=False):
        # Call the ShortestPathBase class constructor
        super().__init__(graph, start_node, end_node, log)


    def _initialize_priority_queue(self):
        '''Initializes the priority queue. 
        Adds an entry for the start node with distance 0, and each other node with the distance infinity '''
        priority_queue = []
        self._queue_sort_by_index = 1
        # Loop through all nodes in the graph
        for node in self.graph.nodes:
            # Get the node element by its name from the graph
            node = self.graph.get_node(node)
            # If the current node is not the start node, make the initial distance infinity
            if node != self.start_node:
                priority_queue.append((node, float('inf'), None))
            # If the current node is the start node, make the distance 0
            else:
                priority_queue.append((node, 0, node))
        return priority_queue


    def _update_priority_queue(self, current_distance, node_to_update, current_node):
        '''Updates a node's entry in the priority queue if the total distance to this node is less than the previous total distance'''
        # Look for the entry in the priority queue that matches the node we are updating
        for i, (node, distance, previous_node) in enumerate(self._priority_queue):
            if node == node_to_update:
                # If the current distance to the node is shorter than the distance previously entered for the node, update it
                if current_distance < distance:
                    self._priority_queue[i] = (node, current_distance, current_node)
                break

class A_Star(ShortestPathBase):
    def __init__(self, graph, start_node, end_node, log=False):
        # Call the ShortestPathBase class constructor
        super().__init__(graph, start_node, end_node, log)

    def _initialize_priority_queue(self):
        '''Initializes the priority queue. 
        Adds an entry for the start node with distance 0, and each other node with the distance infinity'''
        priority_queue = []
        self._queue_sort_by_index = 3
        # Loop through all nodes in the graph
        for node in self.graph.nodes:
            # Get the node element by its name from the graph
            node = self.graph.get_node(node)
            # If the current node is not the start node, make the initial distance infinity
            if node != self.start_node:
                # Each entry in the priority queue has the node, the path length, the previous node on the path, and a combined heuristic
                priority_queue.append((node, float('inf'), None, float('inf')))
            # If the current node is the start node, make the distance 0
            else:
                heuristic_distance = self._distance_to_target(node)
                priority_queue.append((node, 0, node, heuristic_distance))
        return priority_queue
  
    def _distance_to_target(self, node):
        '''Gets the distance between the target node and the current node'''
        target_pos = self.end_node.get_data('pos')
        current_pos = node.get_data('pos')
        distance = round(math.sqrt((target_pos[0]-current_pos[0])**2 + (target_pos[1]-current_pos[1])**2),0)
        return distance

    def _update_priority_queue(self, current_distance, node_to_update, current_node):
        '''Updates a node's entry in the priority queue if the total distance to this node is less than the previous total distance'''
        # Get the current heuristic, which is equal to the length of the path plus the distance to the target
        current_heuristic = current_distance + self._distance_to_target(node_to_update)
        # Look for the entry in the priority queue that matches the node we are updating
        for i, (node, distance, previous_node, heuristic_distance) in enumerate(self._priority_queue):
            if node == node_to_update:
                # If the current distance to the node is shorter than the distance previously entered for the node, update it
                if current_heuristic < heuristic_distance:
                    self._priority_queue[i] = (node, current_distance, current_node, current_heuristic)
                break
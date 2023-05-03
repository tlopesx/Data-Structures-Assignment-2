import networkx as nx
import matplotlib as plt

def get_edges_from_shortest_path( shortest_path):
    '''Uses the list of nodes on the shortest path to extract the list of edges on the shortest path'''
    # Create an array for the edges on the path
    edges = []
    
    # Loop through the nodes on the path, add the edges between them to the path
    for node in range(len(shortest_path)- 1):
        edges.append((shortest_path[node], shortest_path[node+1]))
    
    # Return the list of edges
    return edges

def get_edges_not_in_subgraph( graph, subgraph):
    '''Uses the subgraph created from the list of edges on the path to get the list of edges not on the path'''
    # Create an array for every edge not on the path
    edges_not_in_subgraph = []
    
    # Loop through the edges in the graph
    for u, v, d in graph.edges(data=True):
    
        # If the edge is not in the subgraph add it to the array
        if (u, v) not in subgraph.edges():
            edges_not_in_subgraph.append((u, v))
    
    # Return the list of edges
    return edges_not_in_subgraph

def draw_shortest_path(graph, pos, shortest_path):
    '''Uses the original graph and the list of nodes on the shortest path to draw the '''
    # Create the subgraph with the subnodes
    shortest_path_edges = get_edges_from_shortest_path(shortest_path)
    subgraph = graph.edge_subgraph(shortest_path_edges)

    # Draw the nodes not in the subgraph with 75% transparency
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color='#465368', alpha=0.25)

    # Draw the nodes in the subgraph
    nx.draw_networkx_nodes(subgraph, pos, node_size=700, node_color='#465368')

    # Draw the labels for all nodes
    node_labels = {}
    for node in graph.nodes():
        node_labels[node] = node
    nx.draw_networkx_labels(graph, pos, labels=node_labels, font_color='white', font_size=10, font_family="sans-serif")

    # Get the edges not in the subgraph
    edges_not_in_subgraph = get_edges_not_in_subgraph(graph, subgraph)

    # Draw the edges not in the subgraph with 75% transparency
    nx.draw_networkx_edges(graph, pos, edgelist=edges_not_in_subgraph, alpha=0.25, edge_color="gray")

    # Draw the edges in the subgraph
    nx.draw_networkx_edges(subgraph, pos, alpha=1, edge_color="gray")

    # Draw edge labels for all edges
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, rotate=False)



def print_shortest_path_info( source, target, path, length):
    '''Displays the order of nodes on the shortest path, and the total distance.'''
    # Print the list of nodes on the shortest path
    print("\nShortest path between", source, "and", target, ":", path)
    # Print the total distance
    print("Distance: ", length)
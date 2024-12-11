import matplotlib.pyplot as plt
import networkx as nx

def visualize_taxonomy(G):
    """
    Visualizes the taxonomy graph, differentiating between direct and transitive edges.
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5)

    # Separate edges based on type
    direct_edges = [(u, v) for u, v, d in G.edges(data=True) if d['relation'] != "transitive"]
    transitive_edges = [(u, v) for u, v, d in G.edges(data=True) if d['relation'] == "transitive"]

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightgreen')

    # Draw direct edges
    nx.draw_networkx_edges(G, pos, edgelist=direct_edges, node_size=2000, edge_color='black', arrows=True)

    # Draw transitive edges
    nx.draw_networkx_edges(G, pos, edgelist=transitive_edges, node_size=2000, edge_color='red', style='dashed', arrows=True)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title('Taxonomy Visualization with Lexical and Transitive Links')
    plt.show()
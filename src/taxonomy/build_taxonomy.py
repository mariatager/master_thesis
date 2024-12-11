import networkx as nx

def build_taxonomy(hyponym_relations):
    """
    Builds a taxonomy graph and computes its transitive closure.
    """
    # Step 1: Create the directed graph
    G = nx.DiGraph()
    for hyponym, hypernym, relation_rule in hyponym_relations:
        G.add_edge(hypernym, hyponym, relation=relation_rule)

    # Step 2: Compute transitive closure
    G_transitive = nx.transitive_closure(G)

    # Step 3: Add transitive edges with a distinct label
    for edge in G_transitive.edges:
        if not G.has_edge(*edge):  # Avoid overwriting existing edges
            G.add_edge(edge[0], edge[1], relation="transitive")

    return G
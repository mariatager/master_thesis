from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
import re

def sanitize_node_name(node_name):
    """
    Sanitizes node names to ensure they are valid in URIs.
    """
    # Replace spaces with underscores, remove newlines, and keep only valid characters
    sanitized = re.sub(r'\s+', '_', node_name)  # Replace spaces/newlines with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '', sanitized)  # Remove invalid characters
    return sanitized

def export_to_rdf(G, output_file="taxonomy_sanitized.rdf"):
    """
    Converts a taxonomy graph to RDF format with sanitized URIs to prevent errors in Protege.
    """
    # Create an RDF graph
    rdf_graph = Graph()

    # Define a namespace for your taxonomy
    TAXO = Namespace("http://example.org/taxonomy#")
    rdf_graph.bind("taxo", TAXO)

    # Add nodes and edges to the RDF graph
    for hypernym, hyponym, data in G.edges(data=True):
        # Sanitize node names
        sanitized_hyponym = sanitize_node_name(hyponym)
        sanitized_hypernym = sanitize_node_name(hypernym)

        hyponym_uri = TAXO[sanitized_hyponym]
        hypernym_uri = TAXO[sanitized_hypernym]
        relation = data.get("relation", "relatedTo")

        # Add the rdfs:subClassOf relationship
        rdf_graph.add((hyponym_uri, RDFS.subClassOf, hypernym_uri))  # Hyponym is a subclass of Hypernym

        # Add type declarations for the nodes
        rdf_graph.add((hyponym_uri, RDF.type, TAXO.Concept))
        rdf_graph.add((hypernym_uri, RDF.type, TAXO.Concept))

        # Optionally, add the relation label as a literal
        rdf_graph.add((hyponym_uri, TAXO.relation, Literal(relation)))

    # Serialize to an RDF file
    rdf_graph.serialize(destination=output_file, format="xml")
    print(f"RDF file with sanitized URIs saved to {output_file}")

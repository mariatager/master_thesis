from .utils import LSP_PATTERNS, EXCLUDED_TYPES


def filter_relations(hyponym_relations):
    # First, filter hyponyms as before
    # Organize hyponyms by hypernym
    hypernym_to_hyponyms = {}
    relation_dict = {}
    for hyponym, hypernym, relation in hyponym_relations:
        if hypernym not in hypernym_to_hyponyms:
            hypernym_to_hyponyms[hypernym] = set()
            relation_dict[hypernym] = {}
        hypernym_to_hyponyms[hypernym].add(hyponym)
        relation_dict[hypernym][hyponym] = relation

    # Filter hyponyms for each hypernym
    filtered_hyponym_relations = []
    for hypernym, hyponyms in hypernym_to_hyponyms.items():
        hyponym_list = list(hyponyms)
        hyponyms_to_remove = set()
        for i, hyponym_i in enumerate(hyponym_list):
            for j, hyponym_j in enumerate(hyponym_list):
                if i != j and hyponym_i.lower() in hyponym_j.lower():
                    if len(hyponym_i) < len(hyponym_j):
                        hyponyms_to_remove.add(hyponym_i)
        filtered_hyponyms = [h for h in hyponym_list if h not in hyponyms_to_remove]
        for hyponym in filtered_hyponyms:
            relation = relation_dict[hypernym][hyponym]
            filtered_hyponym_relations.append((hyponym, hypernym, relation))

    # Now, filter hypernyms for each hyponym
    # Organize hypernyms by hyponym
    hyponym_to_hypernyms = {}
    relation_dict_hypernyms = {}
    for hyponym, hypernym, relation in filtered_hyponym_relations:
        if hyponym not in hyponym_to_hypernyms:
            hyponym_to_hypernyms[hyponym] = set()
            relation_dict_hypernyms[hyponym] = {}
        hyponym_to_hypernyms[hyponym].add(hypernym)
        relation_dict_hypernyms[hyponym][hypernym] = relation

    # Filter hypernyms for each hyponym
    final_relations = []
    for hyponym, hypernyms in hyponym_to_hypernyms.items():
        hypernym_list = list(hypernyms)
        hypernyms_to_remove = set()
        for i, hypernym_i in enumerate(hypernym_list):
            for j, hypernym_j in enumerate(hypernym_list):
                if i != j and hypernym_i.lower() in hypernym_j.lower():
                    if len(hypernym_i) < len(hypernym_j):
                        hypernyms_to_remove.add(hypernym_i)
        filtered_hypernyms = [h for h in hypernym_list if h not in hypernyms_to_remove]
        for hypernym in filtered_hypernyms:
            relation = relation_dict_hypernyms[hyponym][hypernym]
            final_relations.append((hyponym, hypernym, relation))

    return final_relations


def filter_relations_by_umls_medical(hyponym_relations, nlp):
    """
    Filters hyponym relations to keep only those where both the hyponym and the hypernym
    are linked to UMLS and do not belong to excluded semantic types.

    Args:
        hyponym_relations (list): A list of (hyponym, hypernym, relation_label) tuples.
        nlp (spacy.Language): The spaCy pipeline with the scispacy linker.
    
    Returns:
        list: A filtered list of hyponym-hypernym relations.
    """

    # Retrieve the linker component from the pipeline
    linker = nlp.get_pipe("scispacy_linker")

    filtered_relations = []
    for hyponym, hypernym, relation_label in hyponym_relations:
        hyponym_doc = nlp(hyponym)
        hypernym_doc = nlp(hypernym)

        def is_valid_entity(doc):
            for ent in doc.ents:
                if ent._.kb_ents:
                    for cui, _ in ent._.kb_ents:
                        entity = linker.kb.cui_to_entity[cui]
                        if not any(tui in EXCLUDED_TYPES for tui in entity.types):
                            return True
            return False

        # Check if both hyponym and hypernym are valid
        if is_valid_entity(hyponym_doc) and is_valid_entity(hypernym_doc):
            filtered_relations.append((hyponym, hypernym, relation_label))

    return filtered_relations

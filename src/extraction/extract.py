import spacy
from spacy.matcher import Matcher
from .utils import LSP_PATTERNS, EXCLUDED_TYPES

def extract_hyponyms(text, nlp):
    """
    Extracts hyponym-hypernym relations from text using predefined patterns
    and additional rules for terms that end with a potential hypernym.
    """
    hyponym_relations = []

    # Convert text to lowercase for consistency
    text = text.lower()

    # Process the text with spaCy
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    # Add predefined patterns to the matcher
    for pat in LSP_PATTERNS:
        matcher.add(pat["label"], [pat["pattern"]])

    # Match patterns in the document
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        label = nlp.vocab.strings[match_id]

        # Identify the cue word and its position
        cue_index = next((i for i, token in enumerate(span) if token.text.lower() in ["such", "including", "especially", "like"]), None)
        if cue_index is None or cue_index + 1 >= len(span):
            continue  # Skip if cue word not found or invalid

        # Handle specific cases for cue words
        if label == "such_as":
            # Skip both "such" and "as" from the hypernym span
            hypernym_tokens = span[:cue_index]
            if span[cue_index + 1].text.lower() == "as":
                cue_index += 1  # Skip "as"
        else:
            # General case: exclude the cue word itself
            hypernym_tokens = span[:cue_index]

        # Extract the remaining tokens as the hyponym span
        hyponym_tokens = span[cue_index + 1:]

        # Extract and clean hypernym
        hypernym = " ".join([token.text for token in hypernym_tokens if not token.is_punct]).strip()

        # Split and clean hyponyms
        hyponyms = split_hyponyms(hyponym_tokens)

        # Append hyponym-hypernym relations
        for hyponym in hyponyms:
            hyponym_relations.append((hyponym, hypernym, label))

    # Add additional relations based on ending matches
    hyponym_relations += detect_ending_match_hyponyms(doc)

    # Remove duplicate relations
    hyponym_relations = list(set(hyponym_relations))
    return hyponym_relations

def detect_ending_match_hyponyms(doc):
    """
    Detects hyponym-hypernym relations based on terms that end with a potential hypernym,
    while ignoring cases with prefixes like 'non-'. e.g.
    hyponym('non-hodgkin lymphoma', 'hodgkin lymphoma') - relation: 'ends_with'


    """
    ending_relations = []
    terms = [ent.text for ent in doc.ents]  # Identify named entities in the text
    for term in terms:
        for potential_hypernym in terms:
            if (
                term != potential_hypernym  # Ensure the term and hypernym are different
                and term.endswith(potential_hypernym)  # Check for ending match
                and not term.startswith("non-")  # Exclude terms with "non-" prefix
            ):
                # If term ends with the potential hypernym and is valid, consider it a relation
                ending_relations.append((term, potential_hypernym, "ends_with"))
    return ending_relations



def split_hyponyms(tokens):
    """
    Splits a sequence of tokens into individual hyponyms using punctuation and conjunctions.
    """
    hyponyms = []
    current_hyponym = []

    for token in tokens:
        if token.text.lower() in [",", "and", "or"]:  # Split on commas and conjunctions
            if current_hyponym:
                hyponyms.append(" ".join([t.text for t in current_hyponym]).strip())
                current_hyponym = []
        else:
            current_hyponym.append(token)

    # Append the last hyponym, if any
    if current_hyponym:
        hyponyms.append(" ".join([t.text for t in current_hyponym]).strip())

    return hyponyms
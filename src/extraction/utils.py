# Define patterns for various lexico-syntactic cues with optional punctuation
LSP_PATTERNS = [
    {"label": "is_a", "pattern": [
    {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},  # Hyponym
    {"LEMMA": "be"},                                       # "is," "are," "was," etc.
    {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},  # Hypernym
    ]},

    # Pattern for "NOUN such as NOUN (, NOUN)* (,)? (and|or)? NOUN"
    {"label": "such_as", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"IS_PUNCT": True, "OP": "?"},                           # Optional punctuation
        {"LOWER": "such"},
        {"LOWER": "as"},
        {"IS_PUNCT": True, "OP": "?"},                           # Optional punctuation
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
        {"LOWER": {"IN": ["and", "or"]}, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "*"},
    ]},

    # Pattern for "including"
    {"label": "including", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},    # Hypernym
        {"IS_PUNCT": True, "OP": "?"},
        {"LOWER": "including"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},    # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
        {"LOWER": {"IN": ["and", "or"]}, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "*"},
    ]},

    # Pattern for "especially"
    {"label": "especially", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},    # Hypernym
        {"IS_PUNCT": True, "OP": "?"},
        {"LOWER": "especially"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},    # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
        {"LOWER": {"IN": ["and", "or"]}, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "*"},
    ]},

    # Pattern for "like"
    {"label": "like", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"IS_PUNCT": True, "OP": "?"},
        {"LOWER": "like"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
        {"LOWER": {"IN": ["and", "or"]}, "OP": "*"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "*"},
    ]},

    # Pattern for "such NP as"
    {"label": "such_NP_as", "pattern": [
        {"LOWER": "such"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"LOWER": "as"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "consist(s) of"
    {"label": "consists_of", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"LEMMA": "consist"},
        {"LOWER": "of"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "comprise(s)"
    {"label": "comprises", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"LEMMA": "comprise"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ", "CCONJ", "PUNCT"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "for example"
    {"label": "for_example", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"IS_PUNCT": True, "OP": "?"},
        {"LOWER": "for"},
        {"LOWER": "example"},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["PUNCT", "CCONJ", "NOUN", "PROPN", "ADJ"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "e.g."
    {"label": "eg", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"IS_PUNCT": True, "OP": "*"},
        {"TEXT": {"REGEX": r"e\.?g\.?"}},
        {"IS_PUNCT": True, "OP": "*"},
        {"ORTH": "(", "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["PUNCT", "CCONJ", "NOUN", "PROPN", "ADJ"]}, "OP": "*"},  # Additional Hyponyms
        {"ORTH": ")", "OP": "?"},
    ]},

    # Pattern for "i.e."
    {"label": "ie", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"IS_PUNCT": True, "OP": "*"},
        {"TEXT": {"REGEX": r"i\.?e\.?"}},
        {"IS_PUNCT": True, "OP": "*"},
        {"ORTH": "(", "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["PUNCT", "CCONJ", "NOUN", "PROPN", "ADJ"]}, "OP": "*"},  # Additional Hyponyms
        {"ORTH": ")", "OP": "?"},
    ]},

    # Pattern for "notably"
    {"label": "notably", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"IS_PUNCT": True, "OP": "?"},
        {"LOWER": "notably"},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["PUNCT", "CCONJ", "NOUN", "PROPN", "ADJ"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "includes"
    {"label": "includes", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"LEMMA": "include"},                                    # "include" or "includes"
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"POS": {"IN": ["PUNCT", "CCONJ", "NOUN", "PROPN", "ADJ"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "such NP as"
    {"label": "NP_such_NP_as", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Possibly Hyponyms before "such"
        {"POS": {"IN": ["PUNCT", "CCONJ"]}, "OP": "*"},
        {"LOWER": "such"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
        {"LOWER": "as"},
        {"IS_PUNCT": True, "OP": "?"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hyponym(s)
        {"POS": {"IN": ["PUNCT", "CCONJ", "NOUN", "PROPN", "ADJ"]}, "OP": "*"},  # Additional Hyponyms
    ]},

    # Pattern for "and other"
    {"label": "and_other", "pattern": [
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # First Hyponym
        {"IS_PUNCT": True, "OP": "*"},
        {"LOWER": {"IN": ["and", "or"]}},
        {"LOWER": "other"},
        {"POS": {"IN": ["NOUN", "PROPN", "ADJ"]}, "OP": "+"},   # Hypernym
    ]},
]


EXCLUDED_TYPES = {
    "T066",  # Machine Activity
    "T065",  # Educational Activity
    "T090",  # Occupation or Discipline
    "T091",  # Biomedical Occupation or Discipline
    "T041",  # Mental Process
    "T080",  # Qualitative Concept
    "T081",  # Quantitative Concept
    "T082",  # Spatial Concept
    "T083",  # Geographic Area
    "T073",  # Manufactured Object
    "T089",  # Regulation or Law
    "T078",  # Idea or Concept
    "T072",  # Physical Object
}
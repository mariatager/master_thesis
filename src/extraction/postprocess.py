import openai
import ast  # Safely parse Python-like structures


def preprocess_llm_response(response_text):
    """
    Cleans the LLM response by removing code fences or other formatting artifacts.
    Ensures that what remains is a clean Python list literal for parsing.
    """
    # Remove code fence markers if present
    response_text = response_text.replace("```python", "").replace("```", "").strip()
    return response_text

def rearrange_taxonomy_pairs(filtered_hyponym_relations):
    """
    Uses an LLM to rearrange, normalize, and refine hyponym-hypernym pairs to create
    a consistent hierarchical taxonomy under the top-level class "cancer."

    Steps performed by the LLM:
      - Ensure all classes related to cancer types descend from "cancer."
      - Merge plural/similar class names (e.g., "cancers" -> "cancer").
      - Remove unrelated or incorrect pairs.
      - Add missing relationships to maintain a coherent hierarchy.

    The function returns a Python list of tuples in the format:
      (hyponym, hypernym, relation)

    Example output structure:
      [
        ('leukemia', 'cancer', 'ends_with'),
        ('lung cancer', 'cancer', 'ends_with'),
        ('small-cell lung cancer', 'lung cancer', 'such_as')
      ]
    """
    with open('../../open_ai_secret_key.txt', 'r') as file:
      openai.api_key = file.read().strip()

    # Convert the input pairs into a string for the prompt
    input_pairs_str = "\n".join(str(pair) for pair in filtered_hyponym_relations)

    # Prompt for the LLM
    prompt = f"""
    You are given a list of hyponym-hypernym relationships extracted from a cancer taxonomy.
    Each relationship is represented as a tuple (hyponym, hypernym, relation).

    Your task:
    1. Ensure every cancer-related class (e.g., leukemia, sarcoma, lung cancer, skin cancer)
       directly or indirectly descends from "cancer". If not, add or adjust relationships.
    2. Normalize classes: merge plurals and variants into a single canonical form ("cancers" → "cancer").
    3. Remove or fix unrelated or incorrect pairs.
    4. Add missing relationships as needed to maintain a coherent hierarchy.
    5. Return the final list as a valid Python list of tuples.

    ### Input Pairs:
    {input_pairs_str}

    ### Output Pairs:
    Return the updated pairs as a Python list of tuples:
    """

    try:
        # Query the LLM
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in taxonomy and medical classification."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )

        # Extract the raw LLM response
        raw_response = response.choices[0].message.content

        # Preprocess the LLM response to remove code fences and ensure clean parsing
        cleaned_response = preprocess_llm_response(raw_response)

        # Safely parse the LLM output as a Python literal
        output_pairs = ast.literal_eval(cleaned_response)
        return output_pairs

    except SyntaxError as e:
        # If there's a syntax error, print debugging info
        print("Syntax Error in LLM Response:", e)
        print("Raw LLM Response:", raw_response)
        return None
    except Exception as e:
        print("Error querying the LLM:", e)
        return None
import openai
import tiktoken

def chunk_text(text, max_tokens=3000):
    """
    Splits a large text into chunks within a specified token limit.
    """
    # Load the tokenizer for the OpenAI model
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # Tokenize the text
    tokens = tokenizer.encode(text)

    # Split tokens into chunks
    for i in range(0, len(tokens), max_tokens):
        yield tokenizer.decode(tokens[i:i + max_tokens])

def format_large_text(raw_text):
    """
    Processes large text in chunks using GPT-3.5-turbo and your custom prompt.
    """
    with open('../../open_ai_secret_key.txt', 'r') as file:
      openai.api_key = file.read().strip()

    formatted_chunks = []
    for chunk in chunk_text(raw_text, max_tokens=3000):  # Adjust chunk size as needed
        # Create a formatted prompt for the current chunk
        prompt = f"""
        The following text discusses cancer-related topics. Your task is to extract and rewrite sentences that describe taxonomic relationships involving cancer types and their subclasses. Specifically:

        1. Extract sentences that describe taxonomic relationships explicitly between:
          - Cancer types and the superclass "cancer" (e.g., "Lung cancer is a type of cancer").
          - Subclasses of specific cancer types (e.g., "Small-cell lung cancer and non-small cell lung cancer are types of lung cancer").

        2. Rewrite each relevant sentence to align with one of the following lexicosyntactic patterns (LSPs):
          - "X such as Y"
          - "Y including X"
          - "Y consists of X"
          - "Y comprises X"
          - "Y, for example, X"
          - "Y, notably, X"
          - "X and other Y"

        3. Ignore any unrelated information (e.g., prognosis, treatments, risk factors, genetic causes) or sentences that do not fit the specified LSPs.

        4. Ensure that each rewritten sentence:
          - Clearly describes a taxonomic relationship.
          - Matches one of the specified LSPs.
          - Is short, concise, and focused only on taxonomy.

        ### Example:
        - Input: "Lung cancer, such as small-cell lung cancer and non-small cell lung cancer, is a significant health concern. Genetic mutations are common in tumors."
        - Output:
          - "Lung cancer, such as small-cell lung cancer and non-small cell lung cancer."
          - "Leukemia includes acute myeloid leukemia and chronic lymphocytic leukemia."

        Text:
        {chunk}

        Rewritten sentences:
        """


        # Query the OpenAI API for the current chunk
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,  # Limit the response length
                temperature=0.5
            )
            formatted_text = response.choices[0].message.content.strip()
            formatted_chunks.append(formatted_text)
        except Exception as e:
            print("Error querying the API:", e)
            formatted_chunks.append(f"Error processing chunk: {e}")

    # Combine all the processed chunks into one text
    return "\n".join(formatted_chunks)
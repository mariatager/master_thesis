import wikipediaapi

def extract_cancer_articles():
    """
    Extracts articles on specified cancer topics from Wikipedia.

    Returns:
        dict: A dictionary where the keys are cancer topic titles, and the values are the corresponding article texts.
    """
    # Define a valid User-Agent
    user_agent = "MyCancerCorpusBot/1.0 (https://yourdomain.com; your_email@example.com)"
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent)  # English Wikipedia

    # List of cancer topics to extract
    cancer_topics = [
        "Cancer", "Carcinoma", "Lymphoma", "Sarcoma", "Leukemia",
        "Breast cancer", "Lung cancer", "Prostate cancer", "Skin cancer",
        "Oncology", "Tumor", "Cancer treatment", "Metastasis"
    ]
    articles = {}

    # Iterate over topics and fetch their content
    for topic in cancer_topics:
        page = wiki_wiki.page(topic)
        if page.exists():
            articles[topic] = page.text

    return articles


def save_corpus(articles, file_path="cancer_corpus.txt"):
    """
    Saves a dictionary of articles to a text file.

    Args:
        articles (dict): A dictionary where the keys are article titles and the values are article contents.
        file_path (str): The file path to save the corpus. Defaults to 'cancer_corpus.txt'.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for title, content in articles.items():
            f.write(f"== {title} ==\n")
            f.write(content + "\n\n")
    print(f"Corpus saved to {file_path}")


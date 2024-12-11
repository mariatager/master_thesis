# README

## **Introduction**
This project implements an automated pipeline to extract and build a taxonomy of cancer-related terms using the Hearst Method. Inspired by Marti A. Hearst's paper, *"Automatic Acquisition of Hyponyms from Large Text Corpora"*, the pipeline identifies hyponym-hypernym relationships (e.g., "lung cancer is a type of cancer") using Lexico-Syntactic Patterns (LSPs). These symbolic methods are robust and domain-independent, relying on predefined patterns in natural language to identify hierarchical relationships.

While the core of the method relies purely on symbolic processing (LSPs), prompting to a large language model (LLM) is used in a minimal capacity for post-processing. This step ensures the taxonomy is refined, normalized, and consistent, avoiding the need for manual intervention in reorganizing the extracted relationships.

---

## **File Structure**
THESIS/ 
├── data/ # Raw and processed data │ 
   ├── cancer_corpus.txt # Raw extracted Wikipedia corpus │
   ├── formatted_cancer_corpus.txt # Processed and formatted corpus 
├── evaluation/ # Files for evaluation │ 
   ├── inferred.owl # Inferred ontology │ 
   ├── tumor_types.owl # Tumor types ontology 
├── notebooks/ # Jupyter notebooks │
   ├── symbolic_method.ipynb # Notebook to run the pipeline 
├── results/ # Results of the pipeline │ 
   ├── symbolic_taxonomy.rdf # Final exported taxonomy in RDF 
├── src/ # Source code │ 
   ├── corpus/ # Corpus-related functions │ │ 
      ├── extract_wiki_corpus.py # Functions for corpus extraction │ 
      ├── format_text.py # Functions to format text │ 
   ├── extraction/ # Extraction-related functions │ │ 
      ├── extract.py # Extract hyponym-hypernym pairs │ │ 
      ├── filter.py # Filter and refine extracted relationships │ │ 
      ├── postprocess.py # Post-process relationships │ │ └── init.py # Module initialization │ ├── taxonomy/ # Taxonomy-related functions │ │ ├── build.py # Build the taxonomy graph │ │ ├── visualize.py # Visualize the taxonomy │ │ ├── export.py # Export taxonomy to RDF │ │ └── init.py # Module initialization │ └── pycache/ # Python cache files ├── Dockerfile # Docker configuration └── README.md # Project documentation

---

## **Pipeline Overview**

### 1. **Corpus Extraction**
   - Extract articles on cancer-related topics (e.g., "leukemia", "tumors") from Wikipedia using `extract_wiki_corpus.py`.
   - Save the raw text corpus in the `data/` directory as `cancer_corpus.txt`.

### 2. **Text Formatting**
   - Process and rewrite the raw text into a structured format that emphasizes taxonomic relationships using predefined LSPs (e.g., "such as," "including").
   - Save the output as `formatted_corpus.txt`.

### 3. **Relation Extraction**
   - Apply the Hearst Method to identify hyponym-hypernym pairs from the formatted text based on predefined LSPs using `extract.py`.

### 4. **Filtering**
   - Refine extracted relationships:
     - Remove redundant or overly generic terms.
     - Validate terms using a UMLS-based symbolic filter to ensure biomedical relevance.

### 5. **Post-Processing**
   - Use prompting to an LLM (GPT-3.5-turbo) for post-processing:
     - Normalize terms, resolve abbreviations, and consolidate variants (e.g., plurals).
     - Reorganize relationships into a hierarchical structure, ensuring all terms descend from "cancer."

### 6. **Taxonomy Construction**
   - Build the taxonomy as a directed graph using `build.py`, compute transitive relationships, and visualize it.

### 7. **Export**
   - Save the final taxonomy in RDF format using `export.py` for further analysis or integration.

---

## **Lexico-Syntactic Patterns (LSPs)**
The following LSPs are used to extract hyponym-hypernym relationships:

| **Pattern Label**   | **Example**                                      |
|----------------------|-------------------------------------------------|
| **is_a**            | "Leukemia is a cancer."                         |
| **such_as**         | "Cancers such as leukemia and lymphoma."        |
| **including**       | "Cancer types including lung cancer."           |
| **especially**      | "Lung cancer, especially small-cell lung cancer."|
| **like**            | "Cancers like leukemia and lymphoma."           |
| **such_NP_as**      | "Such cancers as breast cancer."                |
| **consists_of**     | "The category consists of leukemia and lymphoma."|
| **comprises**       | "The group comprises lung cancer and sarcoma."  |
| **for_example**     | "Cancers, for example, leukemia and sarcoma."   |
| **eg**              | "Cancers (e.g., leukemia, sarcoma)."            |
| **ie**              | "Lymphoma (i.e., a type of blood cancer)."      |
| **notably**         | "Cancers, notably leukemia and sarcoma."        |
| **includes**        | "The group includes leukemia and sarcoma."      |
| **and_other**       | "Lung cancer and other respiratory cancers."    |

---

## **How to Use**

1. **Install Dependencies**:
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt


## **How to Use**
1. **Run the Pipeline:**
Open the notebooks/main.ipynb notebook and execute the steps sequentially.

2. **Outputs:**
- Raw corpus: data/cancer_corpus.txt
- Formatted corpus: data/formatted_corpus.txt
- Final taxonomy: data/taxonomy.rdf
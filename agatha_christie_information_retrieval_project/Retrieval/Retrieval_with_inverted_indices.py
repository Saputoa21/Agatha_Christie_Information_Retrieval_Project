import pickle
from pathlib import Path

import nltk
import string
from nltk.corpus import stopwords

import spacy
nlp = spacy.load("en_core_web_sm")
print(spacy.info())  # Lists installed models

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
new_signs = ['“', '‘', '’', '”', '—']  #specific signs that are not processed with just a punctuation list

import matplotlib.pyplot as plt


# Tokenization function
def tokenize_query(query, stop_words, punctuation, lemmatisation=False):
    clean_book_tokens = []
    processed_book = nlp(query)
    for token in processed_book:
        if token.text in punctuation or token.text in stop_words or token.text in new_signs:
            continue
        if lemmatisation:
            clean_book_tokens.append(token.lemma_)
        else:
            clean_book_tokens.append(token.text)
    return clean_book_tokens

# Load inverted indices from pickle files
input_dir = Path("agatha_christie_information_retrieval_project/Index/Inverted indices")
inverted_indices_as_pickle = sorted(input_dir.glob("*.pkl"))

indices_dict = {}

# Loading the indices from pickle files
for index_file in inverted_indices_as_pickle:
    with open(index_file, 'rb') as f:
        loaded_inverted_index = pickle.load(f)
        print(f"{index_file.name} loaded from the pickle file:")
        print(f"Type of the index: {type(loaded_inverted_index)}")
        print(f"Number of terms in index: {len(loaded_inverted_index)}")
        total_postings = sum(len(postings) for postings in loaded_inverted_index.values())
        print(f"Total postings across all terms: {total_postings}")
        print('\n')
        indices_dict[index_file.name] = loaded_inverted_index

print(len(indices_dict))
print(indices_dict.keys())

# Query function
def query_inverted_index(query, inverted_index, stop_words, punctuation, lemmatisation=False):
    query_terms = tokenize_query(query, stop_words, punctuation, lemmatisation)
    if not query_terms:
        return []
    result = set(inverted_index.get(query_terms[0], []))
    for term in query_terms[1:]:
        postings = set(inverted_index.get(term, []))
        result &= postings
    return sorted(result)

# Example usage with one index
query = "Hercule Poirot"
loaded_index = next(iter(indices_dict.values()))  # Get the first index's data, not the filename

# Query without lemmatization
results = query_inverted_index(query, loaded_index, stop_words, punctuation)
print(f"Documents matching '{query}': {results}")
print(f"Number of Documents matching: {len(results)}\n")

# Query with lemmatization
results_lemmatized = query_inverted_index(query, loaded_index, stop_words, punctuation, lemmatisation=True)
print(f"Documents matching '{query}' with lemmatization: {results_lemmatized}")
print(f"Number of Documents matching (lemmatized): {len(results_lemmatized)}\n")

# Analyzing all indices with tokenization and lemmatization
results_dict_tokenization = {}
results_dict_lemmatization = {}

for index_name, inverted_index in indices_dict.items():
    results_tokenization = query_inverted_index(query, inverted_index, stop_words, punctuation)
    results_dict_tokenization[index_name] = len(results_tokenization)

    results_lemmatization = query_inverted_index(query, inverted_index, stop_words, punctuation, lemmatisation=True)
    results_dict_lemmatization[index_name] = len(results_lemmatization)

# Plotting the results

# For Tokenization
indices = list(results_dict_tokenization.keys())
num_documents_tokenization = list(results_dict_tokenization.values())

plt.figure(figsize=(10, 6))
plt.plot(indices, num_documents_tokenization, marker='o', linestyle='-', color='b', label='Documents Retrieved (Tokenization)')

plt.title('Number of Retrieved Documents by Index (Tokenization)', fontsize=14)
plt.xlabel('Index Name', fontsize=12)
plt.ylabel('Number of Documents', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# For Lemmatization
num_documents_lemmatization = list(results_dict_lemmatization.values())

plt.figure(figsize=(10, 6))
plt.plot(indices, num_documents_lemmatization, marker='o', linestyle='-', color='g', label='Documents Retrieved (Lemmatization)')

plt.title('Number of Retrieved Documents by Index (Lemmatization)', fontsize=14)
plt.xlabel('Index Name', fontsize=12)
plt.ylabel('Number of Documents', fontsize=12)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
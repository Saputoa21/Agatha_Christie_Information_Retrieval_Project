import pickle
from pathlib import Path
# from tokenizing_splitted_dataframes import tokenize_book


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


# Analysis of  inverted indices
input_dir = Path("agatha_christie_information_retrieval_project\Index\Inverted indices")

inverted_indices_as_pickle = sorted(input_dir.glob("*.pkl"))

indices_list = []

for index_file in inverted_indices_as_pickle:
    with open(index_file, 'rb') as f:
    #deserializing the object from the file
        loaded_inverted_index = pickle.load(f)
        #analyzing
        print(f"{index_file.name} loaded from the pickle file:")
        print(f"Type of the index: {type(loaded_inverted_index)}")
        print(f"Number of terms in index: {len(loaded_inverted_index)}")
        total_postings = sum(len(postings) for postings in loaded_inverted_index.values())
        print(f"Total postings across all terms: {total_postings}")
        print('\n')
        indices_list.append(loaded_inverted_index)

print(len(indices_list))

# Quering information from the index
def query_inverted_index(query, inverted_index, stop_words, punctuation, lemmatisation = False):
    query_terms = tokenize_query(query, stop_words, punctuation, lemmatisation) 
    if not query_terms:
        return []
    result = set(inverted_index.get(query_terms[0], []))
    for term in query_terms[1:]:
        postings = set(inverted_index.get(term, []))
        result &= postings
    return sorted(result)

# Example usage with one index
query = "Poirot detective"
loaded_index = indices_list[0]

results = query_inverted_index(query, loaded_index, stop_words, punctuation)
print(f"Documents matching '{query}': {results}")
print(f"Number of Documents matching: {len(results)}")

results = query_inverted_index(query, loaded_index, stop_words, punctuation, lemmatisation= True)
print(f"Documents matching '{query}': {results}")
print(f"Number of Documents matching: {len(results)}")


# Analysing all indices witht the query
# for loaded_index in indices_list:
#     results = query_inverted_index(query, loaded_index, stop_words, punctuation)
# print(f"Documents matching '{query}': {results}")
# print(f"Number of Documents matching: {len(results)}")

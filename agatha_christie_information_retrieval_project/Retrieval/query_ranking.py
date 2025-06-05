from collections import Counter
from retrieval_with_inverted_indices import indices_dict, tokenize_query, stop_words, punctuation

def ranked_query(query_terms, inverted_index):
    doc_scores = Counter()
    for term in query_terms:
        for doc_id in inverted_index.get(term, []):
            doc_scores[doc_id] += 1  
    return doc_scores.most_common()

query = "Who is the man in the brown suit?"

#tokenisation
query_terms = tokenize_query(query, stop_words, punctuation)
inverted_index = next(iter(indices_dict.values())) #the first index 
ranked_results = ranked_query(query_terms, inverted_index)

print(f"Ranked results for query: \"{query}\"")
for doc_id, score in ranked_results[:10]:
    print(f"Doc ID: {doc_id}, Score: {score}\n")

#lemmatisation
query_terms = tokenize_query(query, stop_words, punctuation, lemmatisation=True)
ranked_results = ranked_query(query_terms, inverted_index)

print(f"Ranked results for query: \"{query}\"")
for doc_id, score in ranked_results[:10]:
    print(f"Doc ID: {doc_id}, Score: {score}")



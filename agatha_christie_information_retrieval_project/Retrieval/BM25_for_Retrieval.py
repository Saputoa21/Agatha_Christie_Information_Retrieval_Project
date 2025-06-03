from rank_bm25 import BM25Okapi

#code from the website to see how it works

# The only requirements is that the class receives a list of lists of strings, which are the document tokens.
corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?",
    "How is the weather today in London?",
    "Is it windy today?",
]
tokenized_corpus = [doc.split(" ") for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)
print(bm25)

#Good to note that we also need to tokenize our query, 
#and apply the same preprocessing steps we did to the documents in order to have an apples-to-apples comparison
query = "windy London"
tokenized_query = query.split(" ")
doc_scores = bm25.get_scores(tokenized_query)
print(doc_scores)


#Instead of getting the document scores, you can also just retrieve the best documents with
relevant_docs = bm25.get_top_n(tokenized_query, corpus, n=2)
print(relevant_docs)
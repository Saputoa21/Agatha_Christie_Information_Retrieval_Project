from tokenizing_splitted_dataframes import tokenize_book
from tokenizing_splitted_dataframes import punctuation
from tokenizing_splitted_dataframes import new_signs
from tokenizing_splitted_dataframes import stop_words
from tokenizing_splitted_dataframes import nlp


# # Create a list where each element is the 'paragraph_text' from each row
# documents = almost_final_df['paragraph_text'].tolist()

# all_tokens = [ tokenize_book(doc, stop_words, punctuation, lemmatisation = False) for doc in documents] #without lemmatisation

# terms = set()
# for tokens in all_tokens:
#     terms.update(tokens)
# terms = list(terms)

# inverted_index = {}

# for term in terms:
#     document_ids = []
#     for index, tokens in enumerate(all_tokens):
#        if term in tokens:
#           book_title = almost_final_df.iloc[index]['book_title']
#           book_id = almost_final_df.iloc[index]['book_id']
#           chapter_id = almost_final_df.iloc[index]['chapter_id']
#           paragraph_id = almost_final_df.iloc[index]['paragraph_id']
#           document_identifier = f"Book {book_id} with the title '{book_title}', Chapter {chapter_id}, Paragraph {paragraph_id}"
#           document_ids.append(document_identifier)
#        inverted_index[term] = list(set(document_ids))

# i = 0
# for term, document_ids in inverted_index.items():
#     if i < 15:
#         print(term, "->", ", ".join(document_ids))
#         i += 1
#     else:
#         break

# # #storing inverted index in a pickle file
# # import pickle

# # filename = "inverted_index_preprocess_function.pkl"

# # #binary write mode ('wb')
# # with open(filename, 'wb') as f:
# #     #serializing the inverted index to the file
# #     pickle.dump(inverted_index, f)

# # print(f"Inverted index has been successfully saved to '{filename}'")


# # #binary read mode ('rb')
# # with open(filename, 'rb') as f:
# #     #deserializing the object from the file
# #     loaded_inverted_index = pickle.load(f)

# # #analyzing
# # print("\nInverted index loaded from the pickle file:")
# # print(type(loaded_inverted_index))
# # print("Length of term list", len(loaded_inverted_index))
# # total_postings = sum(len(postings) for postings in inverted_index.values())
# # print("Total postings:", total_postings)
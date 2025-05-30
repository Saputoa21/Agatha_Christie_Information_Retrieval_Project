import nltk
import string
from nltk.corpus import stopwords

# ! python -m spacy download en_core_web_trf
import spacy
nlp = spacy.load("en_core_web_trf")
import en_core_web_trf
nlp = en_core_web_trf.load()
print(spacy.info())  # Lists installed models

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)
new_signs = ['“', '‘', '’', '”', '—']  #specific signs that are not processed with just a punctuation list

# print(stop_words)
# print(punctuation)
# print(type(punctuation))
# print(len(punctuation))

# functions for tokenizing the dataframes
def tokenize_book(book, stop_words, punctuation, lemmatisation=False):
    clean_book_tokens = []
    processed_book = nlp(book)
    for token in processed_book:
        if token.text in punctuation or token.text in stop_words or token.text in new_signs:
            continue
        if lemmatisation:
            clean_book_tokens.append(token.lemma_)
        else:
            clean_book_tokens.append(token.text)
    return clean_book_tokens


# #preprocessing all books
# books = almost_final_df['book_title'].unique() #put all titles together as future key in a dict
# print(type(books))
# book_texts = {}

# for book in books:
#     paragraphs = almost_final_df[almost_final_df['book_title'] == book]['paragraph_text'].astype(str)
#     full_text = ' '.join(paragraphs.tolist())
#     book_texts[book] = full_text
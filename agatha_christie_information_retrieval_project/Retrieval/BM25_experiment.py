import pandas as pd
from rank_bm25 import BM25Okapi
from retrieval_with_inverted_indices import tokenize_query, stop_words, punctuation
from pathlib import Path

csv_files = [
    Path('Data/splitted_dataframes_with_dif_numbers_tokenized/tokenized_Agatha_Christie_Corpus_Combined_Paragraphs_10.csv'),
    Path('Data/splitted_dataframes_with_dif_numbers_tokenized/tokenized_Agatha_Christie_Corpus_Combined_Paragraphs_15.csv'),
    Path('Data/splitted_dataframes_with_dif_numbers_tokenized_lemmatised/tokenized_lemmatised_Agatha_Christie_Corpus_Combined_Paragraphs_10.csv'),
    Path('Data/splitted_dataframes_with_dif_numbers_tokenized_lemmatised/tokenized_lemmatised_Agatha_Christie_Corpus_Combined_Paragraphs_15.csv')
]


#with only tokenising the query
results_data = []

queries = ["Who is actually 'the man in the brown suit'?", 
           "Hercule Poirot",
           "The little grey cells!",
           ]

output_dir = Path("agatha_christie_information_retrieval_project\Retrieval\BM25_results_tokenised")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "bm25_comparison_results.csv"

# process each file
for query in queries:
    tokenized_query = tokenize_query(query, stop_words, punctuation, lemmatisation=False)
    for idx, file in enumerate(csv_files, 1):
        df = pd.read_csv(file)
        tokenized_docs = []
        doc_ids = []
        original_texts = []

        for _, row in df.iterrows():
            try:
                tokens = eval(row["tokenized"])
            except:
                continue
            doc_id = (
                f"Book {row['book_id']} with the title '{row['book_title']}', "
                f"Chapter {row['chapter_id']}, Paragraph {row['paragraph_id']}"
            )
            text = row["paragraph_text"]
            tokenized_docs.append(tokens)
            doc_ids.append(doc_id)
            original_texts.append(text)

        bm25 = BM25Okapi(tokenized_docs)
        scores = bm25.get_scores(tokenized_query)

        top_docs = bm25.get_top_n(tokenized_query, list(zip(doc_ids, original_texts)), n=5)

        for rank, (doc_id, text) in enumerate(top_docs, 1):
            score_index = doc_ids.index(doc_id)
            results_data.append({
                "File": f"File {idx} ({file.name})",
                "Query": query,
                "Rank": rank,
                "BM25_Score": scores[score_index],
                "Doc_ID": doc_id,
                "Paragraph_Text": text
            })

# save to CSV
results_df = pd.DataFrame(results_data)
results_df.to_csv(output_file, index=False)

print(f"Results saved to: {output_file.resolve()}")



#with lemmatising the query
results_data = []

queries = ["Who is actually 'the man in the brown suit'?", 
           "Hercule Poirot",
           "The little grey cells!",
           ]
           

output_dir = Path("agatha_christie_information_retrieval_project\Retrieval\BM25_results_lemmatised")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "bm25_comparison_results_lemmatised.csv"

# process each file
for query in queries:
    tokenized_query = tokenize_query(query, stop_words, punctuation, lemmatisation=True)
    for idx, file in enumerate(csv_files, 1):
        df = pd.read_csv(file)
        tokenized_docs = []
        doc_ids = []
        original_texts = []

        for _, row in df.iterrows():
            try:
                tokens = eval(row["tokenized"])
            except:
                continue
            doc_id = (
                f"Book {row['book_id']} with the title '{row['book_title']}', "
                f"Chapter {row['chapter_id']}, Paragraph {row['paragraph_id']}"
            )
            text = row["paragraph_text"]
            tokenized_docs.append(tokens)
            doc_ids.append(doc_id)
            original_texts.append(text)

        bm25 = BM25Okapi(tokenized_docs)
        scores = bm25.get_scores(tokenized_query)

        top_docs = bm25.get_top_n(tokenized_query, list(zip(doc_ids, original_texts)), n=5)

        for rank, (doc_id, text) in enumerate(top_docs, 1):
            score_index = doc_ids.index(doc_id)
            results_data.append({
                "File": f"File {idx} ({file.name})",
                "Query": query,
                "Rank": rank,
                "BM25_Score": scores[score_index],
                "Doc_ID": doc_id,
                "Paragraph_Text": text
            })

# save to CSV
results_df = pd.DataFrame(results_data)
results_df.to_csv(output_file, index=False)

print(f"Results saved to: {output_file.resolve()}")

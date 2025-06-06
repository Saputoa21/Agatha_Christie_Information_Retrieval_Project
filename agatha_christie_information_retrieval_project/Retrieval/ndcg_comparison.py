import pandas as pd
from sklearn.metrics import ndcg_score
from pathlib import Path

tokenised_dir = Path("agatha_christie_information_retrieval_project/Retrieval/BM25_results_tokenised")
lemmatised_dir = Path("agatha_christie_information_retrieval_project/Retrieval/BM25_results_lemmatised")

lemmatised_csv = lemmatised_dir / "BM25_comparison_results_lemmatised.csv"
tokenised_csv = tokenised_dir / "bm25_comparison_results.csv"

ref_df = pd.read_csv(lemmatised_csv)
comp_df = pd.read_csv(tokenised_csv)

# extract bm25 version name from file name
ref_df["Version"] = ref_df["File"].str.extract(r'Paragraphs_(\d+\.csv|\d+)', expand=False)
comp_df["Version"] = comp_df["File"].str.extract(r'Paragraphs_(\d+\.csv|\d+)', expand=False)

# clean version names (just "10", "15", etc.)
ref_df["Version"] = ref_df["Version"].str.replace(".csv", "", regex=False)
comp_df["Version"] = comp_df["Version"].str.replace(".csv", "", regex=False)

# Store nDCG results
results = []

# for each query and version
for query in ref_df["Query"].unique():
    for version in ref_df["Version"].unique():
        # filter rows
        ref_qv = ref_df[(ref_df["Query"] == query) & (ref_df["Version"] == version)]
        comp_qv = comp_df[(comp_df["Query"] == query) & (comp_df["Version"] == version)]

        # skip incomplete pairs
        if ref_qv.empty or comp_qv.empty:
            continue

        # merge on Doc_ID
        merged = ref_qv[["Doc_ID", "Rank"]].merge(
            comp_qv[["Doc_ID", "Rank"]],
            on="Doc_ID",
            suffixes=("_ref", "_comp")
        )

        # convert rank to relevance (1/rank)
        merged["rel_ref"] = 1 / merged["Rank_ref"]
        merged["rel_comp"] = 1 / merged["Rank_comp"]

        # prepare input for nDCG
        y_true = [merged["rel_ref"].values]
        y_score = [merged["rel_comp"].values]

        ndcg = ndcg_score(y_true, y_score, k=5)

        results.append({
            "Query": query,
            "Version": version,
            "nDCG@5": ndcg
        })

results_df = pd.DataFrame(results)
output_path = Path("Retrieval/ndcg_results/ndcg_against_lemmatised.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
results_df.to_csv(output_path, index=False)

print(f"nDCG scores saved to: {output_path.resolve()}")
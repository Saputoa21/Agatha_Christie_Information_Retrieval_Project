import pandas as pd
from sklearn.metrics import ndcg_score

# Load both result files
ref_df = pd.read_csv("results_1.csv")  # Reference
comp_df = pd.read_csv("results_2.csv")  # To compare

# Merge on document ID to align both rankings
merged = ref_df[['Doc_ID', 'Rank']].merge(
    comp_df[['Doc_ID', 'Rank']],
    on='Doc_ID',
    suffixes=('_ref', '_comp')
)

# Optionally: convert ranks to relevance scores (e.g., inverse rank)
merged['rel_ref'] = 1 / merged['Rank_ref']
merged['rel_comp'] = 1 / merged['Rank_comp']

# Prepare arrays for nDCG
y_true = [merged['rel_ref'].values]
y_score = [merged['rel_comp'].values]  # alternative ranking treated as predicted relevance

# Compute nDCG@k
k = 5  # or whatever cutoff makes sense
score = ndcg_score(y_true, y_score, k=k)
print(f"nDCG@{k}: {score:.4f}")

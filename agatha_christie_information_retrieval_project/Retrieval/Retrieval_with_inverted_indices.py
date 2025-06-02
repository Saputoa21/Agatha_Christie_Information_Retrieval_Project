import pickle
from pathlib import Path


# Analysis of  inverted indices:
input_dir = Path("agatha_christie_information_retrieval_project\Index\Inverted indices")

inverted_indices_as_pickle = sorted(input_dir.glob("*.pkl"))

for index_file in inverted_indices_as_pickle:
    with open(index_file, 'rb') as f:
    #deserializing the object from the file
        loaded_inverted_index = pickle.load(f)
        #analyzing
        print(f"{str(index_file)} loaded from the pickle file:")
        print(type(loaded_inverted_index))
        print("Length of term list", len(loaded_inverted_index))
        total_postings = sum(len(postings) for postings in loaded_inverted_index.values())
        print("Total postings:", total_postings)
        print('\n')
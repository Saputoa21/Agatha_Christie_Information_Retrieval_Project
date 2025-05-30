import pandas as pd

from preprocessing_functions import delete_matedata
from preprocessing_functions import find_chapters
from preprocessing_functions import find_main_book_content
from preprocessing_functions import extract_chapters_and_paragraphs
from preprocessing_functions import chapter_regex


# function to creating dataframes with splitted books  
def splitting_books_for_index(df, book_ids, chapter_regex, paragraph_num):
    """
    Process books from the given DataFrame by extracting chapters and paragraphs.

    Parameters:
        df (pd.DataFrame): The DataFrame containing 'book_id', 'book_title', 'content'.
        book_ids (list): List of integer book IDs to process.
        chapter_regex (str): Regex pattern to identify chapters.
        paragraph_num (int): Number of paragraphs to extract per chapter.

    Returns:
        pd.DataFrame: Concatenated DataFrame of processed book data.
    """
    all_books_df = []

    for i in book_ids:
        try:
            # Fetch book data
            book_text = df.iloc[i]["content"]
            book_title = df.iloc[i]["book_title"]
            book_id = int(df.iloc[i]["book_id"])

            # Remove metadata
            book_wo_metadata = delete_metadata(book_text)

            # Chapter list
            chapter_list = find_chapters(book_wo_metadata, chapter_regex)

            # Extract main content
            book_main_content = find_main_book_content(book_wo_metadata, chapter_list)

            # Debug output
            print(f"Chapter list for {book_title} (ID {book_id}): chapters: {chapter_list}, total: {len(chapter_list)}")

            # Split into chapters and paragraphs
            book_df = extract_chapters_and_paragraphs(
                book_main_content, chapter_list, book_id, book_title, paragraph_num
            )

            all_books_df.append(book_df)

        except Exception as e:
            print(f"[ERROR] Book ID {df.iloc[i]['book_id']} - {df.iloc[i]['book_title']}: {e}")

    return pd.concat(all_books_df, ignore_index=True)


normal_book_ids = [0, 1, 4, 5, 8, 9, 10, 12]  #resuts from the experiments in colab, there are the books which ger processed with created funtion in a right way
paragraph_values = [5, 7, 10] #values of splitting paragraphs to test

# for num in paragraph_values:
#     splitting_books_for_index(
#         df=agatha_christie_books_df, 
#         book_ids=normal_book_ids,  # or any IDs you want
#         chapter_regex=chapter_regex, 
#         paragraph_num=num, 
#         output_dir="Data\splitted_dataframes_with_dif_paragraph_numbers"
#     )


output_dir = "Data\splitted_dataframes_with_dif_paragraph_numbers"

if __name__ == "__main__":

# save_dataframe_to_excel(df, output_dir, processed_books.xlsx)

# save_dataframe_to_csv(df, output_dir, processed_books.xlsx)
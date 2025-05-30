import sqlite3
# from collections import defaultdict
# from pathlib import Path


# class SQLiteIndexer():

#     def __init__(self, db_file: str = "index_sqlite.db") -> None:
#         self._index: dict[str, dict[str, int]] = \
#             defaultdict(lambda: defaultdict(int))
#         self._documents: dict[str, str] = {}

#         with sqlite3.connect(db_file) as con:
#             self.cur = con.cursor()

#         self.initialize_tables()
    

#     def initialize_tables(self) -> None:
#         self.cur.execute("CREATE TABLE IF NOT EXISTS document (doc_id INTEGER PRIMARY KEY, filename TEXT UNIQUE, content TEXT)")
#         self.cur.execute("CREATE TABLE IF NOT EXISTS term (word_id INTEGER PRIMARY KEY, word TEXT UNIQUE)")
#         self.cur.execute("CREATE TABLE IF NOT EXISTS posting (word_id INTEGER, doc_id INTEGER, count INTEGER, unique(word_id, doc_id))")
#         # add indexes to speed up queries
#         self.cur.execute("CREATE INDEX IF NOT EXISTS idx_word ON term (word)")
#         self.cur.execute("CREATE INDEX IF NOT EXISTS idx_word_doc ON posting (word_id, doc_id)")


#     def index(self, doc_name: str, content: str) -> None:
#         # add the document to the database if it doesn't exist
#         self.cur.execute("INSERT OR IGNORE INTO document (filename, content) VALUES (?, ?)", (doc_name, content,))
#         self.cur.execute("SELECT doc_id FROM document WHERE filename = ?", (doc_name,))
#         doc_id = self.cur.fetchone()[0]

#         words = normalize_string(content).split(" ")
#         for word in words:
#             word = word.lower().strip()
#             # add a new word to the inverted index if it doesn't exist
#             self.cur.execute("INSERT OR IGNORE INTO term (word) VALUES (?)", (word,))
#             self.cur.execute("SELECT word_id FROM term WHERE word = ?", (word,))
#             word_id = self.cur.fetchone()[0]

#             # get the current count of the word in the document
#             self.cur.execute("SELECT count FROM posting WHERE word_id = ? AND doc_id = ?", (word_id, doc_id))
#             result = self.cur.fetchone()
#             if result:
#                 count = result[0] + 1
#                 self.cur.execute("UPDATE posting SET count = ? WHERE word_id = ? AND doc_id = ?", (count, word_id, doc_id))
#             else:
#                 # if the word is not in the document, insert it with count 1
#                 self.cur.execute("INSERT INTO posting (word_id, doc_id, count) VALUES (?, ?, ?)", (word_id, doc_id, 1))

#         # commit the changes to the database
#         self.cur.connection.commit()


#     def bulk_index(self, documents: list[tuple[str, str]]):
#         for doc_name, content in documents:
#             print(f"Indexing {doc_name}...")
#             self.index(doc_name, content)


#     def get_docs(self, keyword: str) -> dict[str, int]:
#         keyword = normalize_string(keyword)
#         return self._index[keyword]


# def main():
#     doc_files = Path(__file__).parent.parent / "data" / "Sherlock_Holmes/"
#     docs = [(doc.name, doc.read_text()) for doc in doc_files.glob("*.txt")]
#     sql_indexer = SQLiteIndexer()
#     sql_indexer.bulk_index(docs)
#     # for doc in docs:
#     #     sql_indexer.index(doc[0], doc[1])
#     print("Indexing complete.")

# if __name__ == "__main__":
#     main()
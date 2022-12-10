"""Load inverted index, stopwords, and pagerank into memory."""

import index


def load_stopwords(index_dir):
    """Load stopwords into memory."""
    stopwords_path = index_dir/"stopwords.txt"
    with open(stopwords_path, encoding="utf-8") as stopwords_file:
        stopwords = stopwords_file.read()
        index.app.config["STOPWORDS"] = stopwords.split()


def load_pagerank(index_dir):
    """Load pagerank into memory."""
    pagerank_path = index_dir/"pagerank.out"
    with open(pagerank_path, encoding="utf-8") as pagerank_file:
        for line in pagerank_file.readlines():
            line = line.rstrip()
            doc_id, pagerank = line.split(",")
            index.app.config["PAGERANK"][int(doc_id)] = float(pagerank)


def load_inverted_index(index_dir):
    """Load inverted index into memory."""
    index_path = index_dir/"inverted_index"/index.app.config["INDEX_PATH"]
    with open(index_path, encoding="utf-8") as inverted_index_file:
        for line in inverted_index_file.readlines():
            line = line.rstrip().split()
            word = line[0]
            idf = line[1]
            docs = []
            for i in range(2, len(line), 3):
                docs.append({
                    "doc_id": int(line[i]),
                    "tf": int(line[i + 1]),
                    "norm": float(line[i + 2])
                })
            index.app.config["INVERTED_INDEX"][word] = {
                "idf": float(idf),
                "docs": docs
            }

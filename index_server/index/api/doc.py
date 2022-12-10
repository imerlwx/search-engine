"""Doc processing: get doc vectors, validate the doc."""

from math import sqrt
import index


def get_valid_docs(query):
    """Select documents that contain every word in the cleaned query."""
    selected_doc = {}
    query_set = set(query)

    for query_term in query_set:
        for doc in index.app.config["INVERTED_INDEX"][query_term]["docs"]:
            # Recode how many times the query term appears in the document
            doc_id = doc["doc_id"]
            if doc_id not in selected_doc:
                selected_doc[doc_id] = 1
            else:
                selected_doc[doc_id] += 1

    return [doc_id for doc_id, num_of_query in selected_doc.items()
            if num_of_query == len(query_set)]


def get_docs_dict(query):
    """Return docs' dict in a form: {docid: {tfidf: [tf11 * idf1, ..]}, ..}."""
    docs_dict = {}
    query_set = set(query)
    valid_docs = get_valid_docs(query_set)

    # Construct a dictionary with the following format 
    # {doc_id1: {tf_idf: [tfi1 * idf1, ...], norm: norm}
    for query_term in query_set:
        idf = index.app.config["INVERTED_INDEX"][query_term]["idf"]
        for doc in index.app.config["INVERTED_INDEX"][query_term]["docs"]:
            doc_id = doc["doc_id"]
            if doc_id in valid_docs:
                tf = doc["tf"]
                if doc_id not in docs_dict.keys():
                    docs_dict[doc_id] = {}
                    docs_dict[doc_id]["norm"] = doc["norm"]
                    docs_dict[doc_id]["tf-idf"] = []
                docs_dict[doc_id]["tf-idf"].append(tf * idf)

    # Normalize the vectors and construct the docs matrix
    for _, doc_detail in docs_dict.items():
        norm = sqrt(doc_detail["norm"])
        doc_detail["tf-idf"] = [tfidf / norm for tfidf in doc_detail["tf-idf"]]

    return docs_dict

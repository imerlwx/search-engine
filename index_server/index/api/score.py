"""Mathematical process: calculate the score of the documents."""

import index


def get_tf_idf(vector1, vector2):
    """Calculate the tf-idf between two equal-length vectors."""
    if len(vector1) != len(vector2):
        return None

    tfidf_sum = 0
    for i, item in enumerate(vector1):
        tfidf_sum += item * vector2[i]

    return tfidf_sum


def get_scores(query_vector, doc_dict, weight):
    """Calculate the scores for a doc given a query and a pagerank weight."""
    doc_scores = []
    for doc_id, doc_detail in doc_dict.items():
        pagerank = index.app.config["PAGERANK"][doc_id]
        doc_vector = doc_detail["tf-idf"]
        tf_idf_score = get_tf_idf(query_vector, doc_vector)
        score = weight * pagerank + (1 - weight) * tf_idf_score
        doc_scores.append({
            "docid": doc_id,
            "score": score
        })

    # Sort the scores from highest to lowest, then sort by doc_id inversely
    doc_scores.sort(key=lambda x: (-x["score"], x["docid"]))
    return doc_scores

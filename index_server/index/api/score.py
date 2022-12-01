"""Mathematical process: calculate the score of the documents."""

import index
import flask


def get_weight():
    """Get weight from the user's input and clean it up."""
    weight = flask.request.args.get('w')
    # Use the default weight if no weight specified
    if weight is None:
        weight = 0.5
    else:
        weight = float(weight)


def get_tf_idf(vector1, vector2):
    """Calculate the tf-idf between two equal-length vectors."""
    if len(vector1) != len(vector2):
        return None

    sum = 0
    for i in range(len(vector1)):
        sum += vector1[i] * vector2[i]

    return sum


def get_scores(query_vector, doc_dict, weight):
    """Calculate the scores for a doc given a query and a pagerank weight."""
    doc_scores = []
    for doc_id, doc_detail in doc_dict.items():
        pagerank = index.app.config["PAGERANK"][doc_id]
        doc_vector = doc_detail["tf-idf"]
        tf_idf_score = get_tf_idf(query_vector, doc_vector)
        score = weight * pagerank + (1 - weight) * tf_idf_score
        doc_scores.append({
            "doc_id": doc_id,
            "score": score
        })

    # Sort the scores from highest to lowest, then sort by doc_id inversely
    doc_scores.sort(key=lambda x: (x["score"], -x["doc_id"]), reverse=True)
    return doc_scores

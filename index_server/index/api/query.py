"""Query processing: clean the query, get query vectors, validate the query."""

import re
from math import sqrt
import index


def clean_query(query):
    """Clean the query using the same procedure as the documents."""
    # Remove non-alphanumeric characters (that also aren’t spaces)
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    # Convert upper case characters to lower case
    query = query.casefold()
    # Split the text into whitespace-delimited terms.
    query_words = query.split()

    # Remove stop words
    query_list = []
    for word in query_words:
        if word not in index.app.config["STOPWORDS"]:
            query_list.append(word)

    return query_list


def get_query_vector(query):
    """Make a query vector in a form of [tf1 * idf1, tf2 * idf2, ...]."""
    # Calculate the tf for each term in the query
    query_tf = {}
    for term in query:
        if term in query_tf:
            query_tf[term] += 1
        else:
            query_tf[term] = 1

    # Calculate the tf * idf for each term in the query
    query_list = []
    norm = 0
    query_set = set(query)
    for term in query_set:
        idf = index.app.config["INVERTED_INDEX"][term]["idf"]
        query_list.append(query_tf[term] * idf)
        norm += (query_tf[term] * idf) ** 2

    norm = sqrt(norm)
    return [term / norm for term in query_list]


def valid_query(query):
    """Make sure each term in the query is contained in the inverted index."""
    for query_term in query:
        if query_term not in index.app.config["INVERTED_INDEX"]:
            return False

    return True

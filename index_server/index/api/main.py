"""REST API for index server."""

import pathlib
import flask
import index
from load import load_stopwords, load_pagerank, load_inverted_index
from query import clean_query, valid_query, get_query_vector
from doc import get_docs_dict
from score import get_scores, get_weight


@index.app.before_first_request
def get_start():
    """Load stopwords, pagerank, and inverted index into memory."""
    index_dir = pathlib.Path(__file__).parent.parent
    load_stopwords(index_dir)
    load_pagerank(index_dir)
    load_inverted_index(index_dir)


@index.app.route('/api/v1/', methods=['GET'])
def get_index():
    """Return a list of services available."""
    context = {
        "hits": flask.request.path + "hits/",
        "url": flask.request.path
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return a list of hits with doc ID and score."""
    # Get query string from the user's input
    query = flask.request.args.get('q')
    query = clean_query(query)
    # If not all terms are included in the inverted index, return empty json
    if not valid_query(query):
        context = {
            "hits": []
        }
        return flask.jsonify(**context)

    query_vector = get_query_vector(query)
    docs_dict = get_docs_dict(query)
    weight = get_weight()
    hits = get_scores(query_vector, docs_dict, weight)
    context = {
        "hits": hits
    }
    return flask.jsonify(**context)

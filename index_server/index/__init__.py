"""Index server package initializer."""

import os
import flask


# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name

# Different instances of the Index server will serve different segments of
# the inverted index. One Index server should load one segment from the file
# specified by the environment variable INDEX_PATH. If the environment variable
# is not set, then default to inverted_index_1.txt. 
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

app.config["PAGERANK"] = {} # doc_id: pagerank
app.config["STOPWORDS"] = [] # a list of stop words
app.config["INVERTED_INDEX"] = {} # word: {idf: idf, [{doc_id, tf, norm}, ...]}

import index.api  # noqa: E402  pylint: disable=wrong-import-position

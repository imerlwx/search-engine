"""Search server index (main) view."""

import threading
import heapq
import queue
import flask
import search
import requests


def get_hits(search_url, thread_result):
    """Return the hits detail from urls into a queue."""
    return thread_result.put(requests.get(search_url, timeout=10))


def key_func(hits):
    """Define a key function for the heapq.merge."""
    return hits['score']


def get_doc(doc_id):
    """Get doc detail from the database."""
    connection = search.model.get_db()  # connect to database
    cur = connection.execute(
        "SELECT title AS doc_title, summary AS doc_summary, url AS doc_url "
        "FROM Documents WHERE docid = ?", (doc_id, )
    )
    return cur.fetchone()


@search.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    queries = flask.request.args.get("q", type=str)
    weight = flask.request.args.get("w", default=0.5)
    context = {
        "query": queries,
        "weight": weight,
        "results": []
    }

    if queries:
        query = "+".join(queries.split())
        threads = []
        thread_result = queue.Queue()
        search_index = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']

        # Create threads for the urls
        for _, search_url in enumerate(search_index):
            search_url = search_url + "?q=" + query + "&w=" + str(weight)
            # Use threads to save the results from search indexes into a queue
            thread = threading.Thread(target=get_hits,
                                      args=(search_url, thread_result))
            threads.append(thread)
            thread.start()

        # Close threads
        for thread in threads:
            thread.join()

        results_list = []  # will have three sublists from the three urls
        while not thread_result.empty():
            hits_detail = thread_result.get().json()
            results_list.append(hits_detail['hits'])

        results_list = heapq.merge(*results_list, key=key_func, reverse=True)
        count = 10  # number of hit info shown on the page
        for result in results_list:
            context['results'].append(get_doc(result['docid']))
            count -= 1
            if count == 0:
                break

    return flask.render_template("index.html", **context)

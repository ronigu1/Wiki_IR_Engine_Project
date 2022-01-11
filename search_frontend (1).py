import csv
import gzip
from flask import Flask, request, jsonify
from tokenize_query import get_query_tokens
from inverted_index_gcp import *
from search_title import get_search_title
from cos_sim_search import *
from main_search import main_search

def open_pkl(base_dir, name):
        with open(Path(base_dir) / f'{name}.pkl', 'rb') as f:
            return pickle.load(f)


class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, **options):
        self.DL = open_pkl('/home/hodayat', 'DL')    
        self.title_index = InvertedIndex.read_index('/home/hodayat/title/postings_gcp', 'index')
        self.body_index = InvertedIndex.read_index('/home/hodayat/body/postings_gcp', 'index')
        self.titles = open_pkl('/home/hodayat/title', 'DocIdTile')
        with gzip.open('/home/hodayat/part-00000-6cdc51ec-4687-4fc0-a84e-38cdcf355376-c000.csv.gz', "rt") as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.pr = dict(csv_reader)
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, **options)


app = MyFlaskApp(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# Need to implement - (2) Average retrieval time (No longer than 35 sec): less than 2 sec(5 points), 2-5 sec(3 points), 5-10 sec(1 point).
@app.route("/search")
def search():
    """
    Returns up to a 100 of your best search results for the query. This is
    the place to put forward your best search engine, and you are free to
    implement the retrieval whoever you'd like within the bound of the
    project requirements (efficiency, quality, etc.). That means it is up to
    you to decide on whether to use stemming, remove stopwords, use
    PageRank, query expansion, etc.

    To issue a query navigate to a URL like:
     http://YOUR_SERVER_DOMAIN/search?query=hello+world
    where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
    if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each
        element is a tuple (wiki_id, title).
    """
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    query_tokenized = get_query_tokens(query)
    res = main_search(app.title_index, app.pr, app.titles, query_tokenized)
    # END SOLUTION
    return jsonify(res)


# Need to implement - (1.a) cosine similarity using tf-idf on the body of articles
@app.route("/search_body")
def search_body():
    """
    Returns up to a 100 search results for the query using
    TFIDF AND COSINE SIMILARITY OF THE BODY OF ARTICLES ONLY.
    DO NOT use stemming.
    DO USE the staff-provided tokenizer from Assignment 3 (GCP part) to do the
    tokenization and remove stopwords.

    To issue a query navigate to a URL like:
     http://YOUR_SERVER_DOMAIN/search_body?query=hello+world
    where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
    if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of up to 100 search results, ordered from best to worst where each
        element is a tuple (wiki_id, title).
    """
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    query_tokenized = get_query_tokens(query)
    res = cos_sim(app.body_index, query_tokenized, app.DL)
    # END SOLUTION
    return jsonify(res)


# Need to implement - (1.b) binary ranking using the title of articles
@app.route("/search_title")
def search_title():
    """
    Returns ALL (not just top 100) search results that contain
    A QUERY WORD IN THE TITLE of articles,
    ordered in descending order of the NUMBER OF QUERY WORDS that appear in the title.
    For example, a document with a title that matches two of the query words
    will be ranked before a document with a title that matches only one query term.

    Test_! this by navigating to the a URL like:
     http://YOUR_SERVER_DOMAIN/search_title?query=hello+world
    where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
    if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to
        worst where each element is a tuple (wiki_id, title).
    """
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    query_tokenized = get_query_tokens(query)
    res = get_search_title(query_tokenized, app.title_index, app.titles)
    # END SOLUTION
    return jsonify(res)


# Need to implement - (1.c) binary ranking using the anchor text
@app.route("/search_anchor")
def search_anchor():
    """
    Returns ALL (not just top 100) search results that contain
    A QUERY WORD IN THE ANCHOR TEXT of articles, ordered in descending order of
    the NUMBER OF QUERY WORDS that appear in anchor text linking to the page.
    For example, a document with a anchor text that matches two of the
    query words will be ranked before a document with anchor text that
    matches only one query term.

    Test_! this by navigating to the a URL like:
    http://YOUR_SERVER_DOMAIN/search_anchor?query=hello+world
    where YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
    if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ALL (not just top 100) search results, ordered from best to
        worst where each element is a tuple (wiki_id, title).
    """
    res = []
    query = request.args.get('query', '')
    if len(query) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    
    # END SOLUTION
    return jsonify(res)


# Need to implement - (1.d) ranking by PageRank
@app.route("/get_pagerank", methods=['POST'])
def get_pagerank():
    """
    Returns PageRank values for a list of provided wiki article IDs.
    Test_! this by issuing a POST request to a URL like:
      http://YOUR_SERVER_DOMAIN/get_pagerank
    with a json payload of the list of article ids. In python do:
      import requests
      requests.post('http://YOUR_SERVER_DOMAIN/get_pagerank', json=[1,5,8])
    As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
    if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of floats:
          list of PageRank scores that correrspond to the provided article IDs.
    """
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    for id in wiki_ids:
        if str(id) in app.pr.keys():
            res.append(app.pr[str(id)])
    # END SOLUTION
    return jsonify(res)


# Need to implement - (1.e) ranking by article page views
@app.route("/get_pageview", methods=['POST'])
def get_pageview():
    """
    Returns the number of page views that each of the provide wiki articles
    had in August 2021.
    Test_! this by issuing a POST request to a URL like:
      http://YOUR_SERVER_DOMAIN/get_pageview
    with a json payload of the list of article ids. In python do:
      import requests
      requests.post('http://YOUR_SERVER_DOMAIN/get_pageview', json=[1,5,8])
    As before YOUR_SERVER_DOMAIN is something like XXXX-XX-XX-XX-XX.ngrok.io
    if you're using ngrok on Colab or your external IP on GCP.
    Returns:
    --------
        list of ints:
          list of page view numbers from August 2021 that correrspond to the
          provided list article IDs.
    """
    res = []
    wiki_ids = request.get_json()
    if len(wiki_ids) == 0:
        return jsonify(res)
    # BEGIN SOLUTION
    
    # END SOLUTION
    return jsonify(res)


if __name__ == '__main__':
    # run the Flask RESTful API, make the server publicly available (host='0.0.0.0') on port 8080
    app.run(host='0.0.0.0', port=8080)

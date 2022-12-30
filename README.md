# Information Retrieval project:

## Building a search engine for English Wikipedia
We used common Python libraries, like Numpy and Pandas, Nltk (for text preprocess), and we saved our data 
(inverted index pickle files, page rank calculations, page views and more) in Google Cloud Platform (GCP).

We also used the Flask RESTful API, in order to make the server publicly available.
We published URL address to enables remote-users to query our engine and recieve results.

### Code Stucture:
1. inverted_index_gcp.py - Used to initializes the inverted index and create a necessary objects for writing and reading the relevant files to the appropriate path in GCP.

2. inverted_index_to_gcp.ipynb - Used to read the entire corpus (the wiki dump file) to an rdd, directly from Google Storage Bucket.
In addition, Used to build three inverted index objects (one for the documents body, one for title and one for anchor text)
and write them to the appropriate path in GCP, using inverted_index_gcp.py.

3. queries_train.json - Given training set of queries, with the optimal retrieval results.
Used for training and testing our retrieval engine.

4. search_frontend.py - Used to create the server (flask RESTful API), receive queries from clients and provide the mose relevant answers,
 using 6 - different search functions that use this fucntions:
   - tokenize_query.py - get_query_tokens
   - inverted_index_gcp.py - InvertedIndex.read_index
   - search_title -  get_search_title, In order to run our request in a relatively quick time, 
   we initially based ourselves on a smaller source of information than all the documents in the corpus - the titles
   - cos_sim_search - cos_sim, Contains implementations of a class that we use to retrieve using the cosine similarity measure.
   - main_search - main_search
 
 
 
 
 


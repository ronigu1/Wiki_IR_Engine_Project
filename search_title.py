import pickle
from collections import Counter, OrderedDict, defaultdict
from inverted_index_gcp import InvertedIndex

def open_pkl(src):
    with open(src, 'rb') as inp:
        doc_title = pickle.load(inp)
        return doc_title


def get_search_title(query, ind, docIdTitle):
    doc_count = Counter()
    index = ind
    for word in query:
        pl_dic = dict(InvertedIndex.read_posting_list(index, word, 'title'))
        pl_doc_ids = pl_dic.keys()
        doc_count.update(pl_doc_ids)
    lst_doc_id_by_score = sorted(doc_count, key=doc_count.get, reverse=True)
    titles = docIdTitle
    lst1 = []
    for doc_id in lst_doc_id_by_score :
        lst1.append((doc_id, titles[doc_id]))
    return lst1

from collections import Counter
from inverted_index_gcp import InvertedIndex
from tokenize_query import get_query_tokens


def get_doc_id_by_title(ind, query, docIdTitle):
    doc_count = Counter()
    for word in query:
        pl_dic = dict(InvertedIndex.read_posting_list(ind, word, 'title'))
        pl_doc_ids = pl_dic.keys()
        doc_count.update(pl_doc_ids)
    doc_ids_sorted_by_count = sorted(doc_count, key=doc_count.get, reverse=True)
    doc_ids_sorted_by_position = {}
    for doc in doc_ids_sorted_by_count:
        for word in query:
            doc_words = get_query_tokens(docIdTitle[doc])
            word_pos = 0
            if word in doc_words:
                word_pos = doc_words.index(word) + 1
            if word_pos > 0:
                if doc not in doc_ids_sorted_by_position.keys():
                    doc_ids_sorted_by_position[doc] = len(doc_words)/word_pos
                else:
                    doc_ids_sorted_by_position[doc] += len(doc_words)/word_pos
    return {k: v for k, v in sorted(doc_ids_sorted_by_position.items(), key=lambda item: item[1], reverse=True)}


def get_id_score_by_pr(pr, docs):
    ranked_docs = {}
    N = len(docs)
    i = len(docs)
    pr_values = {}
    for doc_id in docs:
        if str(doc_id) not in pr.keys():
            continue
        pr_values[doc_id] = float(pr[str(doc_id)])
    max_pr = float(max(pr_values.values(), key=float))
    for doc_id in docs:
        if doc_id not in pr_values.keys():
            ranked_docs[doc_id] = (i / N, i / N)
        else:
            ranked_docs[doc_id] = (i / N, pr_values[doc_id] / max_pr)
        i -= 1
    title_pr_dic = {}
    for doc_ic, score_tuple in ranked_docs.items():
        title_pr_dic[doc_ic] = score_tuple[0] * 0.6 + score_tuple[1] * 0.4
    res = {k: v for k, v in sorted(title_pr_dic.items(), key=lambda item: item[1], reverse=True)}
    return res


def get_score_titles(docIdTitle, scores):
    titles = docIdTitle
    lst1 = []
    for doc_id in scores:
        lst1.append((doc_id, titles[doc_id]))
    return lst1[:100]


def main_search(ind, pr, docIdTitle, query):
    doc_ids_by_title = get_doc_id_by_title(ind, query, docIdTitle)
    search_by_pr_and_title = get_id_score_by_pr(pr, doc_ids_by_title)
    return get_score_titles(docIdTitle, search_by_pr_and_title)

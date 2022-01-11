from inverted_index_gcp import InvertedIndex
import math


def query_to_dict_term_Fij(query):
    len_q = len(query)
    query_dic = {}
    for term in query:
        if term not in query_dic:
            query_dic[term] = 1 / len_q
        else:
            query_dic[term] += 1 / len_q
    #{term : tf_q}
    return query_dic


def doc_to_dict_term_Fij(index,query,DL):
    docs_dic={}
    for term in query:
        list_of_doc = InvertedIndex.read_posting_list(index, term, 'body')
        for doc_id, tf in list_of_doc:
            if doc_id not in docs_dic.keys():
                docs_dic[doc_id] = {}
            if docs_dic[doc_id].get(term) is None:
                #{doc_id:{term1:tf_ij,..}}
                docs_dic[doc_id][term]=tf/DL.get(doc_id)
    return docs_dic


def get_top_n(sim_dict, N=3):
    return sorted([(doc_id, round(score, 5)) for doc_id, score in sim_dict.items()], key=lambda x : x[1], reverse=True)[:N]


def cos_sim(index,query,DL):
    dict_cosSim = {}
    df = index.df
    docs_dic = doc_to_dict_term_Fij(index,query,DL)
    query_dic = query_to_dict_term_Fij(query)
    q_norm = sum([x*2 for x in query_dic.values()])
    for doc_id,term_tf_dic in docs_dic.items():
        mone = 0
        for term in query_dic.keys() :
            # w_ij = tf_ij * idf
            idf = math.log2(len(DL) / df.get(term))
            tf_doc = term_tf_dic.get(term)
            tf_query = query_dic.get(term)
            if tf_doc is None or tf_query is None or idf is None:
                continue
            else:
                mone += tf_doc * tf_query * idf
        dict_cosSim[doc_id] = (mone/(DL.get(doc_id) * q_norm)) * (len(term_tf_dic) ** 10)
    return get_top_n(dict_cosSim, 100)
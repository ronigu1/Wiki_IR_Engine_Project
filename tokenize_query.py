from collections import Counter, OrderedDict, defaultdict
import re
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords

nltk.download('stopwords')

english_stopwords = frozenset(stopwords.words('english'))
corpus_stopwords = ["category", "references", "also", "external", "links",
                    "may", "first", "see", "history", "people", "one", "two",
                    "part", "thumb", "including", "second", "following",
                    "many", "however", "would", "became"]

all_stopwords = english_stopwords.union(corpus_stopwords)
RE_WORD = re.compile(r"""[\#\@\w](['\-]?\w){2,24}""", re.UNICODE)

NUM_BUCKETS = 124


def get_query_tokens(text):
    tokens = [token.group() for token in RE_WORD.finditer(text.lower())]
    # YOUR CODE HERE
    tokens_list = []
    tokens_without_duplicaltion = list(OrderedDict.fromkeys(tokens))
    for t in tokens_without_duplicaltion:
        if t in all_stopwords:
            continue
        else:
            tokens_list.append(t)
    return tokens_list



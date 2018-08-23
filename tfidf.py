import math
import json
import re
from collections import OrderedDict

#calculate tf-idf
def tfidf(f,n,d,cacm_corpus):
    N=len(cacm_corpus)
    tf=float(f)/float(d)
    idf=math.log(float(N)/float(n))
    return tf*idf

#get tf-idf scores
def get_score(q1,cacm_corpus,cacm_index):
    q1_terms=q1.split(' ')
    score={}
    for query_term in q1_terms:
        if query_term not in cacm_index:
            continue
        else:
            for d_tf in cacm_index[query_term]:
                if d_tf[0] not in score:
                    score[d_tf[0]] = tfidf(d_tf[1],len(cacm_index[query_term]), get_doc_length(d_tf[0],cacm_corpus),cacm_corpus)
                else:
                    score[d_tf[0]] += tfidf(d_tf[1], len(cacm_index[query_term]), get_doc_length(d_tf[0],cacm_corpus),cacm_corpus)

    score = OrderedDict(sorted(score.items(), key=lambda x: x[1],reverse=True))
    return score

#parse the query
def parse_query(query):
    #remove urls
    query = re.sub(r'^https?:\/\/.*[\r\n]*',' ', query, flags=re.MULTILINE)
    #remove punctuations but preserve numbers
    regex=re.compile('[^a-zA-Z0-9\.,]') #remove symbols
    query=regex.sub(' ',query)
    query=re.sub(r"(?!\d)[.,](?!\d)",'',query) #retain decimal numbers
    #case fold
    query=query.lower() #comment to disable case folding
    query=re.sub(r" +"," ",query)

    return query

#retrieval function
def tfidf_retrieval(q,cacm_corpus,cacm_index):
    scores = get_score(parse_query(q),cacm_corpus,cacm_index)
    return {k: scores[k] for k in list(scores)[:100]}


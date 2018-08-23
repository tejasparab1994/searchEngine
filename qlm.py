import math
import json
import re
from collections import OrderedDict

#returns the length of the document
def get_doc_length(i,cacm_corpus):
    return len(cacm_corpus[i])

#returna the size of the corpus
def C(cacm_corpus):
    l=0
    for k,v in cacm_corpus.items():
        l+=len(v)
    return l

#returns the corpus freqeuncy of a term
def get_corpus_freq(term,cacm_corpus):
    t=0
    for c in cacm_corpus:
        for te in cacm_corpus[c]:
            if te==term:
                t+=1
    return t

#calculate qlm score
def qlm(f,D,c,cacm_corpus):

    num1=float(f/D)
    num2=float(c/C(cacm_corpus))
    LAMBDA=0.35
    score=math.log(((1-LAMBDA)*num1) + (LAMBDA*num2))

    return score

#get qlm scores for all documents
def get_score(q1,cacm_corpus,cacm_index):
    q1_terms=q1.split(' ')
    score={}
    for query_term in q1_terms:
        if query_term not in cacm_index:
            continue
        else:
            for d_tf in cacm_index[query_term]:

                if d_tf[0] not in score:
                    score[d_tf[0]]=qlm(d_tf[1],get_doc_length(d_tf[0],cacm_corpus),get_corpus_freq(query_term,cacm_corpus),cacm_corpus)
                else:
                    score[d_tf[0]]+=qlm(d_tf[1],get_doc_length(d_tf[0],cacm_corpus),get_corpus_freq(query_term,cacm_corpus),cacm_corpus)


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
    query=query.lower() #case folding
    query=re.sub(r" +"," ",query)#remove extra spaces

    return query

#retrieval function
def qlm_retrieval(q,cacm_corpus,cacm_index):
    scores = get_score(parse_query(q),cacm_corpus,cacm_index)
    return {k: scores[k] for k in list(scores)[:100]}



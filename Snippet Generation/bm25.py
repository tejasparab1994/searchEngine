import math
import json
import re
from collections import OrderedDict

#returns the length of the given document
def get_doc_length(i,cacm_corpus):
    return len(cacm_corpus[i])

#returns avg doc length of the corpus
def avg_doc_length(cacm_corpus):
    l=0
    for c in cacm_corpus:
        l+=len(c)

    return (float)(l/len(cacm_corpus))

#calculate bm25 scores
def bm25(f,n,q,L,cacm_corpus):

    k2=100
    k1=1.2
    b=0.75
    N=len(cacm_corpus)
    R=0
    r=0

    K=k1*((b*L)+(1-b))
    num1=((k2+1)*q)/(k2+q)
    num2=((k1+1)*f)/(K+f)
    num3=math.log10((r+0.5)*(N-n-R+r+0.5))/((n-r+0.5)*(R-r+0.5))

    score=num1*num2*num3
    return score

#calculate score for each query term
def get_score(q1,cacm_corpus,cacm_index):
    q1_terms=q1.split(' ')
    score={}
    seen=[]
    for query_term in q1_terms:
        if query_term not in cacm_index or query_term in seen:
            continue
        else:
            seen.append(query_term)
            for d_tf in cacm_index[query_term]:
                L=float(get_doc_length(d_tf[0],cacm_corpus)/avg_doc_length(cacm_corpus))

                if d_tf[0] not in score:
                    score[d_tf[0]]=bm25(d_tf[1],len(cacm_index[query_term]),q1.count(query_term),L,cacm_corpus)
                else:
                    score[d_tf[0]]+=bm25(d_tf[1],len(cacm_index[query_term]),q1.count(query_term),L,cacm_corpus)


    score = OrderedDict(sorted(score.items(), key=lambda x: x[1],reverse=True))
    return score

#parse query no stopping
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
def bm25_retrieval(q,cacm_corpus,cacm_index):
    scores = get_score(parse_query(q),cacm_corpus,cacm_index)
    return {k: scores[k] for k in list(scores)[:100]}


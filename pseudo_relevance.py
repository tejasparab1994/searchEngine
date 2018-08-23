import json
import os
from bs4 import BeautifulSoup
from bm25 import bm25_retrieval
from qlm import qlm_retrieval
from tfidf import tfidf_retrieval

'''
READING ALL THE FILES
'''
#read corpus
cacm_file = open("CACM/cacm.json","r")
cacm_corpus = json.load(cacm_file)

#read index from file
cacm_index_file = open("CACM/inverted_index_cacm.json","r")
cacm_index = json.load(cacm_index_file)

def get_queries():
    queries = {}
    soup = BeautifulSoup(open("Queries/cacm.query.txt"),"lxml")
    doc = soup.findAll("doc")
    raw_queries = []
    spaces_removed = []
    none_removed = []
    for query in doc:
        raw_queries.append(query.getText().replace("\n"," "))
    for query in raw_queries:
        spaces_removed.append(query.split(" "))
    for query in spaces_removed:
        none_removed.append([word for word in query if word])
    for query in none_removed:
        queries[query[0]] = " ".join(query[1:])
    return queries

def get_top_words(words,n):
    word_counts = {}
    stop_words = get_stopwords()
    without_stop_words = []
    for word in words:
        if word not in stop_words:
            without_stop_words.append(word)
    for words in without_stop_words:
        word_counts[words] = without_stop_words.count(words)
    top_words = sorted(list(word_counts.items()),key=lambda x:x[1],reverse=True)[:n]
    top_words_list = []
    for k,v in top_words:
        top_words_list.append(k)
    return top_words_list

def get_stopwords():
    f = open("Stopwords/common_words.txt","r")
    raw_words = f.readlines()
    stop_words = []
    for word in raw_words:
        stop_words.append(word.strip("\n"))
    return stop_words

def make_flat_list(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list

def compute_psr(query,query_id,path):
    k = 5 #top docs
    n = 4 #top words
    old_results = bm25_retrieval(query,cacm_corpus,cacm_index)
    top_k_docs = []
    top_n_words = []
    for key,value in list(old_results.items())[:k]:
        top_k_docs.append(key)
    for document in top_k_docs:
        top_n_words.append(get_top_words(cacm_corpus[document],n))
    expanded = query+" "+" ".join(make_flat_list(top_n_words))
    new_results = bm25_retrieval(expanded,cacm_corpus,cacm_index)

    write_dictionary(new_results, query_id, path, "cacm_bm25_pseudo_relevance")

def write_dictionary(dictionary, query_id, path, system):
    f = open(path,"w")
    titles = ["Query #", "Literal", "Document", "Rank", "Score", "System Name"]
    f.write("{:<10}{:<10}{:<30}{:<10}{:<20}{:<10}".format(*titles))
    f.write("\n\n")
    for k,v in dictionary.items():
        entries = [query_id, "Q0", str(k), str(list(dictionary.keys()).index(k) + 1), str(v), system]
        f.write("{:<10}{:<10}{:<30}{:<10}{:<20}{:<10}".format(*entries))
        f.write("\n")


def pseudo_relevance_feedback(path):
    if not os.path.exists(path):
        os.makedirs(path)
    queries = get_queries()
    for key, value in queries.items():
        print("Computing Pseudo Relevance on query: "+str(key))
        compute_psr(value,key,str(path)+str(key)+".txt")


pseudo_relevance_feedback("CACM_PRF/")


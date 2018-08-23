#encoding: utf-8
from bs4 import BeautifulSoup
import json
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

#read stopped corpus
cacm_stopped_file = open("CACM Stopped/cacm_stopped_corpus.json","r")
cacm_stopped_corpus = json.load(cacm_stopped_file)

#read stopped index from file
cacm_stopped_index_file = open("CACM Stopped/inverted_index_cacm_stopped.json","r")
cacm_stopped_index = json.load(cacm_stopped_index_file)

#read stemmed corpus
cacm_stemmed_file = open("CACM Stemmed/cacm_stemmed_corpus.json","r")
cacm_stemmed_corpus = json.load(cacm_stemmed_file)

#read stemmed index from file
cacm_stemmed_index_file = open("CACM Stemmed/inverted_index_cacm_stemmed.json","r")
cacm_stemmed_index = json.load(cacm_stemmed_index_file)



def get_stopwords():
    f = open("Stopwords/common_words.txt","r")
    raw_words = f.readlines()
    stop_words = []
    for word in raw_words:
        stop_words.append(word.strip("\n"))
    return stop_words

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


def get_stemmed_queries():
    q = {}
    query_file = open("Queries/cacm_stem.query.txt","r")
    raw_queries = query_file.readlines()
    queries = []
    for query in raw_queries:
        queries.append(query.strip("\n"))
    for query in queries:
        q[queries.index(query)+1] = query
    return q

def write_dictionary(dictionary, query_id, path, system):
    f = open(path,"w")
    titles = ["Query #", "Literal", "Document", "Rank", "Score", "System Name"]
    f.write("{:<10}{:<10}{:<30}{:<10}{:<20}{:<10}".format(*titles))
    f.write("\n\n")
    for k,v in list(dictionary.items()):
        entries = [query_id, "Q0", str(k), str(list(dictionary.keys()).index(k) + 1), str(v), system]
        f.write("{:<10}{:<10}{:<30}{:<10}{:<20}{:<10}".format(*entries))
        f.write("\n")


def retrieve_cacm_bm25():
    queries = get_queries()
    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(bm25_retrieval(v,cacm_corpus,cacm_index),k,"CACM_BM25/"+str(k)+".txt","cacm_bm25")

def retrieve_cacm_tfidf():
    queries = get_queries()
    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(tfidf_retrieval(v,cacm_corpus,cacm_index),k,"CACM_TFIDF/"+str(k)+".txt","cacm_tfidf")

def retrieve_cacm_qlm():
    queries = get_queries()
    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(qlm_retrieval(v,cacm_corpus,cacm_index),k,"CACM_QLM/"+str(k)+".txt","cacm_qlm")

def retrieve_stopped_cacm_bm25():
    queries=get_queries()
    stop_words=get_stopwords()
    new_query=""
    for q in queries:
        query_terms=queries[q].split(' ')
        for qt in query_terms:
            if qt not in stop_words:
               new_query+=qt+" "
        if len(new_query)!=0:
            queries[q]=new_query

    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(bm25_retrieval(v,cacm_corpus,cacm_index),k,"CACM_STOPPED_BM25/"+str(k)+".txt","cacm_stopped_bm25")

def retrieve_stopped_cacm_tfidf():
    queries=get_queries()
    stop_words=get_stopwords()
    new_query=""
    for q in queries:
        query_terms=queries[q].split(' ')
        for qt in query_terms:
            if qt not in stop_words:
               new_query+=qt+" "
        if len(new_query)!=0:
            queries[q]=new_query

    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(tfidf_retrieval(v,cacm_corpus,cacm_index),k,"CACM_STOPPED_TFIDF/"+str(k)+".txt","cacm_stopped_tfidf")

def retrieve_stopped_cacm_qlm():
    queries=get_queries()
    stop_words=get_stopwords()
    new_query=""
    for q in queries:
        query_terms=queries[q].split(' ')
        for qt in query_terms:
            if qt not in stop_words:
               new_query+=qt+" "
        if len(new_query)!=0:
            queries[q]=new_query

    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(qlm_retrieval(v,cacm_corpus,cacm_index),k,"CACM_STOPPED_QLM/"+str(k)+".txt","cacm_stopped_qlm  ")

def retrieve_stemmed_cacm_tfidf():
    queries=get_stemmed_queries()

    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(tfidf_retrieval(v,cacm_stemmed_corpus,cacm_stemmed_index),k,"CACM_STEMMED_TFIDF/"+str(k)+".txt","cacm_stemmed_tfidf")

def retrieve_stemmed_cacm_bm25():
    queries=get_stemmed_queries()

    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(bm25_retrieval(v,cacm_stemmed_corpus,cacm_stemmed_index),k,"CACM_STEMMED_BM25/"+str(k)+".txt","cacm_stemmed_bm25")

def retrieve_stemmed_cacm_qlm():
    queries=get_stemmed_queries()

    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(qlm_retrieval(v,cacm_stemmed_corpus,cacm_stemmed_index),k,"CACM_STEMMED_QLM/"+str(k)+".txt","cacm_stemmed_qlm")


#uncomment the below functions to perform retrieval of your choice

#retrieve_cacm_bm25() #normal bm25 run
#retrieve_cacm_tfidf() #normal tf-idf run
#retrieve_cacm_qlm() #normal qlm run

#retrieve_stopped_cacm_qlm() #stopped qlm run
#retrieve_stopped_cacm_tfidf() #stopped tf-idf run
#retrieve_stopped_cacm_bm25() #stopped bm25 run

#retrieve_stemmed_cacm_qlm() #stemmed qlm run
#retrieve_stemmed_cacm_tfidf() #stemmed tf-idf run
#retrieve_stemmed_cacm_bm25() #stemmed bm25 run

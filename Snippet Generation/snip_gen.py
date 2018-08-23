#encoding: utf-8

from collections import defaultdict
import math
import json
import re
from collections import OrderedDict
from bm25 import bm25_retrieval
from bs4 import BeautifulSoup

#read corpus
cacm_file = open("CACM/cacm.json","r")
cacm_corpus = json.load(cacm_file)

#read index from file
cacm_index_file = open("CACM/inverted_index_cacm.json","r")
cacm_index = json.load(cacm_index_file)

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


def generate_snippet(filename,q):

    score = defaultdict(list)
    f = open(str(filename), "r")
    lines = f.read()
    f.close()

    lines=parse_query(lines)

    line = lines.split()
    per_line = 5
    for i in range(0, len(line), per_line):
        line[i]=" ".join(line[i:i + per_line])

    sl = open("stoplist.txt", "r")
    stop = sl.readlines()
    sl.close()

    l = []

    for item in stop:
        l.append(item.strip("\n"))

    stoplist = filter(None, l)

    significant = {}
    for d in range(0,len(line),per_line):
        significant[line[d]]=0

    query=q.split()
    for s in significant:
        for qt in query:
            if qt in s and qt not in l:
                count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(qt), s)) #for exact match
                significant[s]+=count

    significant=OrderedDict(sorted(significant.items(), key=lambda x: x[1],reverse=True))
    return {k: significant[k] for k in list(significant)[:3]}

def snippet(doc,q):

    sl = open("stoplist.txt", "r")
    stop = sl.readlines()
    sl.close()

    l = []

    for item in stop:
        l.append(item.strip("\n"))

    stoplist = filter(None, l)

    snip=generate_snippet(doc,q)
    slist=[]
    for s in snip:
        slist.append(s)

    query=q.split()
    for s in range(0,len(slist)):
        for qt in query:
            if qt in slist[s] and qt not in l:
                slist[s]=re.sub(r' '+qt+' ',' *%s* ' %qt, slist[s])

    for s in range(0,len(slist)):
        slist[s]="..."+slist[s]+"..."

    return slist

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

def write_dictionary(dictionary, query_id, path, system,query):
    f = open(path,"w")
    titles = ["Query #", "Literal", "Document", "Rank", "Score", "System Name"]
    f.write("{:<10}{:<10}{:<30}{:<10}{:<20}{:<10}".format(*titles))
    f.write("\n\n")
    for k,v in list(dictionary.items()):
        entries = [query_id, "Q0", str(k), str(list(dictionary.keys()).index(k) + 1), str(v), system]
        f.write("{:<10}{:<10}{:<30}{:<10}{:<20}{:<10}".format(*entries))
        f.write("\n\n")
        doc=k.split("/")[1]
        doc=doc.replace(".html",".txt")
        s=snippet(doc,query)
        for sen in s:
            f.write("\t%s\n"%sen)
        f.write("\n")
    f.close()


def retrieve_cacm_bm25():
    queries = get_queries()
    for k,v in list(queries.items()):
        print(("Processing query: "+str(k)))
        write_dictionary(bm25_retrieval(v,cacm_corpus,cacm_index),k,"SNIPPET_BM25/"+str(k)+".txt","snippet_bm25",v)



retrieve_cacm_bm25()

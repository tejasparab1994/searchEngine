import json
from collections import defaultdict
from operator import itemgetter
from itertools import groupby
from BM25 import BM25

# Getting the uni-gram index from HW3
print("Please wait.. Reading inverted-index")
json_data = open("1-gram_inverted_index.json")
inverted_index = json.load(json_data)

# Getting the word-tokens data structure from HW3
print("Please wait.. Reading word-tokens")
word_tokens = open("word-tokens.json")
tokens = json.load(word_tokens)

# Storing document length in a separate dictionary
document_length = defaultdict(list)
for key,value in tokens.items():
    document_length[key] = len(value)

# Getting the queries

queriesFile = open("queries.txt","r")
query = queriesFile.readlines()
queries = []
for q in query:
    queries.append(q.strip("\n"))

# Getting average document length

def getAvgDL(length):
    count = 0
    for key, value in length.items():
        count += value
    return float(count) / float(len(length))

# Ranking documents

def ranker(queries,inverted_index):
    result = defaultdict(list)
    splitQueries = queries.split(" ")
    for word in splitQueries:
        if word in inverted_index:
            docList = inverted_index[word]
            for document, frequency, word_position in docList:
                BMScore = BM25(document_length[document] ,getAvgDL(document_length), len(docList), len(inverted_index), frequency, 1, 0)
                if document in result:
                    result[document] += BMScore
                else:
                    result[document] = BMScore
    return result

def check_word_proximity(result,inverted_index,query):
    query_words = query.split()
    relevant_docs = get_documents_having_all_query_terms(result,query)
    term_pos = defaultdict(list)
    for word in query_words:
        if word in inverted_index:
            inverted_list = inverted_index[word]
            for item in inverted_list:
                if item[0] in relevant_docs:
                    term_pos[item[0]].append([word,item[2]])
    rel = []
    for key, value in term_pos.items():
        rel.append(check_prox(key,value,query_words))
    return [_f for _f in rel if _f]


def check_prox(document,terms_pos,query_words):
    term_dict = {}
    for i in range(len(query_words)):
        for item in terms_pos:
            if query_words[i] is item[0]:
                term_dict[i+1] = item[1]
    to_compare = []
    for i in range(len(term_dict)):
        to_compare.append(term_dict[i+1])
    if find_conse(to_compare,query_words) is True or find_conse_one(to_compare,query_words) is True or find_conse_two(to_compare,query_words) is True or find_conse_three(to_compare,query_words) is True:
        return document


def find_conse(wopos,query_words):
    prox = False
    for item in wopos[0]:
        for i in range(1,len(query_words)-1):
            if item+i in wopos[i]:
                if item+i+i in wopos[i+1]:
                    prox = True
    return prox

def find_conse_one(wopos, query_words):
    prox = False
    for item in wopos[0]:
        for i in range(1,len(query_words)-1):
            if item+1+i in wopos[i]:
                if item+1+i+i in wopos[i+1]:
                    prox = True
    return prox

def find_conse_two(wopos, query_words):
    prox = False
    for item in wopos[0]:
        for i in range(1, len(query_words) - 1):
            if item + 2 + i in wopos[i]:
                if item + 2 + i + i in wopos[i + 1]:
                    prox = True
    return prox

def find_conse_three(wopos, query_words):
    prox = False
    for item in wopos[0]:
        for i in range(1, len(query_words) - 1):
            if item + 3 + i in wopos[i]:
                if item + 3 + i + i in wopos[i + 1]:
                    prox = True
    return prox

def make_flat_list(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list


def get_documents_having_all_query_terms(result,query):
    query_words = query.split()
    doc_list = []
    for key, value in result.items():
        words_in_doc = tokens[key]
        if set(query_words).issubset(words_in_doc):
            doc_list.append(key)
    return doc_list


# Performing ranking for each query
def processQueries(queries, inverted_index):
    for query in queries:
        print("Processing query: "+str(query))
        result = ranker(query,inverted_index)

        rel = check_word_proximity(result,inverted_index,query)
        for doc in rel:
            result[doc] += 10

        writer = open("BM25 Query-" + str(queries.index(query) + 1) + ".txt", "w")
        titles = ["Query #", "Literal", "Document", "Rank", "BM25 Score", "System Name"]
        writer.write("{:<10}{:<10}{:<30}{:<10}{:<30}{:<10}".format(*titles))
        writer.write("\n\n")

        sort = sorted(iter(result.items()), key=lambda value:value[1],reverse=True)

        for i in sort[:100]:
            entries = [str(queries.index(query) + 1), "Q0", str(i[0]), str(sort.index(i) + 1), str(i[1]),
                       "unigram_casefolded_BM25_proximity"]
            writer.write("{:<10}{:<10}{:<30}{:<10}{:<30}{:<10}".format(*entries))
            writer.write("\n")
    print("Done!, You'll find " + str(len(queries)) + " files, one for each query generated within this directory")

processQueries(queries,inverted_index)

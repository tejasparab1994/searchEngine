import glob
from collections import defaultdict
from read_html_file import parse_html
from read_html_file import parse_html_without_stopwords
from stemmed_parser import generate_stemmed_corpus
import json
import os

def get_corpus_file_names(path):
    corpusFiles = []
    for file in glob.glob(str(path)+"/*.html"):
        corpusFiles.append(file)
    return corpusFiles

def get_original_html_content(path):
    corpus = defaultdict(list)
    corpus_files = get_corpus_file_names(path)
    for file in corpus_files:
        #print "Processing file: "+str(file)
        corpus[file] = parse_html(file)
    return corpus

def get_stopped_html_content(path):
    corpus = defaultdict(list)
    corpus_files = get_corpus_file_names(path)
    for file in corpus_files:
        #print "Processing file: "+str(file)
        corpus[file] = parse_html_without_stopwords(file)
    return corpus

def generate_stemmed_index(path):
    inverted_index = defaultdict(list)
    corpus = generate_stemmed_corpus()
    for key,value in corpus.iteritems():
        word_list = value
        for word in set(value):
            inverted_index[word].append([key,word_list.count(word)])
    os.makedirs("CACM Stemmed")
    with open("CACM Stemmed/inverted_index_cacm_stemmed.json", "w") as f:
        json.dump(inverted_index,f)
    with open("CACM Stemmed/cacm_stemmed.json","w") as cf:
        json.dump(corpus,cf)

def generate_stopped_index(path):
    inverted_index = defaultdict(list)
    corpus = get_stopped_html_content(path)
    for key,value in corpus.iteritems():
        word_list = value
        for word in set(value):
            inverted_index[word].append([key,word_list.count(word)])
    os.makedirs("CACM Stopped")
    with open("CACM Stopped/inverted_index_cacm_stopped.json", "w") as f:
        json.dump(inverted_index,f)
    with open("CACM Stopped/cacm_stopped.json","w") as cf:
        json.dump(corpus,cf)

def generate_original_index(path):
    inverted_index = defaultdict(list)
    corpus = get_original_html_content(path)
    for key,value in corpus.iteritems():
        word_list = value
        for word in set(value):
            inverted_index[word].append([key,word_list.count(word)])
    os.makedirs("CACM")
    with open("CACM/inverted_index_cacm.json", "w") as f:
        json.dump(inverted_index,f)
    with open("CACM/cacm.json","w") as cf:
        json.dump(corpus,cf)


def indexer():
    print "Which inverted index do you want to create?"
    print "1. CACM Original (without stopping)"
    print "2. CACM with Stopping"
    print "3. CACM with Stemming"
    print "4. All of the above"
    print "\n"
    option = raw_input("Enter appropriate number (eg. 1, 2, 3, or 4): ")
    print "\n"
    print "Enter appropriate path of the corpus (eg. 'corpus/' if the corpus is located in the same directory)"
    path = raw_input("::")
    print "Please wait, generating index"
    if int(option) == 1:
        print "Generating original inverted index, please wait.."
        generate_original_index(path)
    elif int(option) == 2:
        print "Generating stopped inverted index, please wait.."
        generate_stopped_index(path)
    elif int(option) == 3:
        print "Generating stemmed inverted index, please wait.."
        generate_stemmed_index(path)
    elif int(option) == 4:
        print "Generating original inverted index, please wait.."
        generate_original_index(path)
        print "Generating stopped inverted index, please wait.."
        generate_stopped_index(path)
        print "Generating stemmed inverted index, please wait.."
        generate_stemmed_index(path)

    else:
        "Incorrect choice"

indexer()







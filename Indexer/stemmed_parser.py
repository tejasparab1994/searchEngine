from collections import defaultdict

def read_stem_file():
    file = open("cacm_stem.txt","r")
    raw_docs = "".join(file.readlines())
    return raw_docs


def generate_stemmed_corpus():
    corpus = defaultdict(list)
    separate_docs = read_stem_file().split("#")[1:]
    for document in separate_docs:
        tokens = document.split()
        corpus[tokens[0]] = tokens[1:]
    return corpus


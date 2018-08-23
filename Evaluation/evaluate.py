import glob
from calculate import PR
from calculate import get_AVP_and_RR
from read_data import get_rel_judgements

def get_corpus_file_names(path):
    corpusFiles = []
    for file in glob.glob(str(path)+"/*.txt"):
        corpusFiles.append(file)
    return corpusFiles

def evaluate(source,destination):
    all_files = get_corpus_file_names(source)
    for file in all_files:
        PR(file,destination)

    # getting all the generated evaulated files
    all_generated_files = get_corpus_file_names(destination)

    # defining variable to store summation of all the AP
    total_AP = 0

    # defining variable to store summation of all the RR
    total_RR = 0

    for file in all_generated_files:
        total_AP += float(get_AVP_and_RR(file)[0])
        total_RR += float(get_AVP_and_RR(file)[1])

    # getting total number of queries
    total_queries = len(all_generated_files)

    # calculating mean average precision
    # MAP = float(total_AP) / float(total_queries) #TODO: exclude documents not having relevance judgements
    try:
        MAP = float(total_AP) / float(len(get_rel_judgements("cacm.rel.txt")))
    except ZeroDivisionError:
        MAP = 0

    # calculating mean reciprocal rank
    try:
        MRR = float(total_RR) / float(len(get_rel_judgements("cacm.rel.txt")))
    except ZeroDivisionError:
        MRR = 0

    summary_file = open(destination+"summary.txt","w")
    summary_file.write("MAP: "+str(MAP))
    summary_file.write("\n")
    summary_file.write("MRR: "+str(MRR))


#replace the parameters by "<source files>/","<destination files>/"
evaluate("CACM_PRF/","CACM_PRF_EVAL/")

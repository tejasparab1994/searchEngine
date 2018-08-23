from read_data import get_result_data
from read_data import get_rel_judgements
import os

def is_relevant_document(QUERY_ID, document_name, relevance_judgement):
    relevant_docs = relevance_judgement[QUERY_ID]
    d = document_name.rstrip(".html")
    document = d[d.index("/")+1:]
    if document in relevant_docs:
        return "R"
    else:
        return "N"

def relevancy(status):
    if status is "R":
        return 1
    else:
        return 0

# function to return the precision at rank 5

def pAt5(table):
    return table[4][2]

# function to return the precision at rank 5

def pAt20(table):
    return table[19][2]


def PR(file,destination):

    # read data
    retrieval_data = get_result_data(file)
    relevance_judgements = get_rel_judgements("cacm.rel.txt")

    # get query ID from result file
    QUERY_ID = retrieval_data[0][0]

    # defining precision-recall table
    PR_TABLE = []

    # defining variable to store relevant documents found so far
    relevant_so_far = 0

    # defining variable to add precision values of relevant documents
    precision_summation = 0

    # defining variable to store flag of relevant document fo reciprocal rank
    reciprocal_flag = "N"

    # defining variable to store the rank of first relevant document
    rank = 0

    # iterating over each entry in the result
    for line in retrieval_data:

        # relevancy status for document
        is_relevant = is_relevant_document(QUERY_ID,line[2],relevance_judgements)

        # calculating relevant documents so far
        relevant_so_far += relevancy(is_relevant)

        # calculating precision
        PRECISION = float(relevant_so_far) / float(line[3])

        # calculating recall
        try:
            RECALL = float(relevant_so_far) / float(len(relevance_judgements[QUERY_ID])) # using relevance data available beforehand
        except ZeroDivisionError:
            RECALL = 0

        # appending values to PR TABLE

        PR_TABLE.append([line[3], is_relevant, PRECISION, RECALL])

        # summation of precision values of relevant documents
        if is_relevant is "R":
            precision_summation += PRECISION

        if reciprocal_flag is not "R":
            reciprocal_flag = is_relevant
            if reciprocal_flag is "R":
                rank = line[3]

    # calculating reciprocal rank
    try:
        reciprocal_rank = float(1) / float(rank)
    except ZeroDivisionError:
        reciprocal_rank = 0

    # calculating average precision
    try:
        #average_precision = float(precision_summation) / float(relevant_so_far) #TODO: use relevance info beforehand
        average_precision = float(precision_summation) / float(len(relevance_judgements[QUERY_ID]))
    except ZeroDivisionError:
        average_precision = 0

    #write everything to file

    write(PR_TABLE,average_precision,reciprocal_rank,pAt5(PR_TABLE),pAt20(PR_TABLE),destination,QUERY_ID)



def write(pr_table, average_precision, reciprocal_rank, pat5, pat20, destination, query_id):
    if not os.path.exists(destination):
        os.makedirs(destination)
    f = open(str(destination)+str(query_id)+".txt","w")
    f.write("AVP: "+str(average_precision))
    f.write("\n")
    f.write("RR: "+str(reciprocal_rank))
    f.write("\n")
    f.write("P@5: "+str(pat5))
    f.write("\n")
    f.write("P@20: "+str(pat20))
    f.write("\n")
    titles = ["Rank", "R/N", "Precision", "Recall"]
    f.write("{:<10}{:<10}{:<30}{:<30}".format(*titles))
    f.write("\n")
    for line in pr_table:
        f.write("{:<10}{:<10}{:<30}{:<30}".format(*line))
        f.write("\n")


def get_AVP_and_RR(file):
    f = open(file,"r")
    all_lines = f.readlines()
    avp_raw = all_lines[0].strip("\n")
    rr_raw = all_lines[1].strip("\n")
    avp = avp_raw.split(" ")[1]
    rr = rr_raw.split(" ")[1]
    return avp, rr

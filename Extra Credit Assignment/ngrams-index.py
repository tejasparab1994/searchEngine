import json
import glob
import re
from collections import defaultdict
from collections import OrderedDict

#The data-structure to store the number of tokens in each file
wordTokens = defaultdict(list)

#create word n-grams
def ngram(wordList,n):
    grams = [wordList[i:i+n] for i in range(len(wordList)-n+1)]
    returnList = []
    for item in grams:
        returnList.append(" ".join(item))
    return returnList

#gets the names of all the ".txt" files in a folder and returns a list
def getCorpusFileNames(path):
    corpusFiles = []
    for file in glob.glob(str(path)+"/*.txt"):
        corpusFiles.append(file)
    return corpusFiles

#takes each line from the document file and splits each word and creates a list
def processFile(fileData):
    processedData = []
    for line in fileData:
        processedData.append(line.strip("\n")) #Removes break-line from each element of the list
    eachWord = []
    for item in [_f for _f in processedData if _f]:
        temp = item.split(" ") #Splits the string into words
        for thing in temp:
            eachWord.append(thing)
    return [_f for _f in eachWord if _f] # Returns list with empty elements removed

# The index generator function that takes a list of words, the name of the document and the dictionary data structure
def indexer(wordList,documentName,invertedIndex):
    for word in set(wordList):
        word_positions = [i for i, x in enumerate(wordList) if x == word]
        invertedIndex[word].append([documentName,wordList.count(word),word_positions]) #Creates the row of the inverted index
        wordTokens[documentName].append(word) #Maintains the separate data-structure for number of tokens in each document

#The main function that takes the corpus directory path and THE NUMBER OF N-GRAMS you want to generate
def makeIndex(corpusPath,nstart,ngrams):
    for i in range(nstart,ngrams+1): #the loop will run for each n-gram
        inverted = defaultdict(list)
        for item in getCorpusFileNames(corpusPath):
            file = open(item, "r")
            workFile = processFile(file.readlines())
            indexer(ngram(workFile,i), item, inverted) #create index for that file
            print(("Processing file: "+item+" for "+str(i)+"-gram"))
        generateTermFreqTable(inverted,i) #create term frequency table
        generateDocumentFreqTable(inverted,i) #create document frequency table
        f = open(str(i)+"-gram_inverted_index.txt", "wb")
        for key,value in sorted(inverted.items()): #write the index to a file for viewing purpose
            f.write(str(key)+" : " +str(value))
            f.write("\n")
        with open(str(i)+"-gram_inverted_index.json", "w") as f: #write the index to json for querying in the future
            json.dump(inverted, f)
        with open("word-tokens.json","w") as fw:
            json.dump(wordTokens,fw)


#function to generate term frequency table, it takes the inverted index and the n-gram number
def generateTermFreqTable(inverted,i):
    tfTable = defaultdict(list)
    for key,value in list(inverted.items()):
        print(("Generating Term Frequency Table for "+str(i)+"-gram"))
        counter = 0 #maintains a counter to calculate number of terms
        for subvalue in value:
            counter = counter + subvalue[1]
        tfTable[key] = counter #stores the terms in the dictionary data structure
    f = open(str(i)+"-gram_term_frequency.txt","w")
    sort = OrderedDict(sorted(list(tfTable.items()),key=lambda i: i[1], reverse=True)) #sorts the dictionary by highest frequency
    for key,value in list(sort.items()):
        f.write(str(key)+" : "+str(value))
        f.write("\n")

#function to generate document frequency table, it takes the inverted index and the n-gram number
def generateDocumentFreqTable(inverted,i):
    dfTable = defaultdict(list)
    for key, value in list(inverted.items()):
        print(("Generating Document Frequency Table for " + str(i) + "-gram"))
        documents = [] #maintains a list of all documents for that term
        for subvalue in value:
            documents.append(subvalue[0]) #stores the list of all the documents for that term
        dfTable[key] = [documents, len(documents)] #stores the term, the names of the document and it's frequency
    f = open(str(i)+"-gram_document_frequency.txt", "w")
    for key,value in sorted(dfTable.items()):
        f.write(str(key)+" : "+str(value))
        f.write("\n")

print("Write the path, the name of your folder followed by a slash (without quotes)")
print("\n")
print("Example: corpus/ if there is folder named 'corpus' in the same directory")
print("The folder that you are providing should contain text files")
corpusPath = eval(input("Write the path for your corpus eg. corpus/ :"))
print("Specify the value of n to generate inverted index")
ngramType = eval(input("1. Unigram  2. Bigram  3. Trigram  4. All\n"))
if int(ngramType) is 1:
    makeIndex(str(corpusPath),1,int(ngramType))
elif int(ngramType) is 2:
    makeIndex(str(corpusPath),2,int(ngramType))
elif int(ngramType) is 3:
    makeIndex(str(corpusPath),3,int(ngramType))
else:
    makeIndex(str(corpusPath),1,3)


All the python files for the basic as well as stopped and stemmed runs can be found in this directory.
All codes are written in Python 3

Files were executed and run on Pycharm

Execution:
The python files can be executed using any IDE like PyCharm
Or
They can be run form terminal : >>python <filename>.py
				>>./<filename>.py

Libraries Used:
	1) json
	2) BeautifulSoup
	3) os
	4) re
	5) OrderedDict


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
All retieval models:

Run the file "retrieval.py" to run the following:

Basic Runs:
bm25 : Results in CACM_BM25 folder
query likelihood model with JM smoothing : Results in CACM_QLM folder
tf-idf : Results in CACM_TFIDF folder

Stopped Corpus and Query runs:
bm25 stopped : Results in CACM_STOPPED_BM25 folder
qlm stopped : Results in CACM_STOPPED_QLM folder
tf-idf stopped : Results in CACM_STOPPED_TFIDF folder

Stemmed Corpus and Query runs:
bm25 stemmed : Results in CACM_STEMMED_BM25 folder
qlm stemmed : Results in CACM_STEMMED_BM25 folder
tf-idf stemmed : Results in CACM_STEMMED_BM25 folder

At the end of code, the function calls for each of the above runs can be found commented out.
Uncomment the call of the retrieval you want to run.

NOTE: For all the bm25 runs, relevant information was not considered. Only for task 3 while computing evaluations it is considered.

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Psuedo Relevance Feedback:

Run the file "pseudo_relevance.py" to run the program which performs query exapansion using Pseudo Relevance Feedback using BM25 retrieval algorithm.
Top 5 documents are retrived using BM25.
From those top 5 documents, the count of top words excluding the stop words in each document is calculated.
Highest 4 ranking words from all documents are added to the query.

BM25 scores are then again calculated for the documents and they are ranked accordingly.
The results can be found in "CACM_PRF" folder. 

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Lucene:

The lucene implementaion is in Java. Use an IDE such as eclipse and load the project "Lucene" into it.
Run the "HW4.java" file to generate results.
The results can be found in "CACM_LUCENE" folder.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Snippet Generation:

Since the document length is less, the approach for snippet generation mentioned in the texbook fails.
Hence, we consider 5 words to form a sentence in order to incorporate the short length of the documents. The number of query terms found in those sentences are counted 
and sentences are accordingly scored. Stop words in query are not counted.
Then top 3 sentences are displayed in format "...<sentence>..." with query term highlighted as *<query term>*

Snippets are generated for the BM25 retrieval model.

Navigate to the folder "Snippet Generation"
Run the file "snip_gen.py". This generates the results in "SNIPPET_BM25" folder.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Query by Query Analysis:

Analysis for the stemmed documents for 3 queries can be found in "Analysis.txt" file in the root directory.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Evaluation:

The codes and results for Evaluation can be found in "Evaluation" folder. There is a separate "ReadMe.txt" file found in that folder. Please go through that in order to receive instructions for that part of the code.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Bonus Credit:

The codes and results for extra credit part can be found in the folder "Extra Credit Assignment". There is a separate "ReadMe.txt" file found in that folder. Please go through that in order to receive instructions for that part of the code.

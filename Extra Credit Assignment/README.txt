EXTRA CREDIT ASSIGNMENT:

The following assignment contains the following files:

1. ngrams-index.py
——————————
This is the indexer program. We have used this file from the HW3, and modified it to add word positions to the inverted index.

It generates, inverted index in TXT as well as JSON format. We are using the JSON format inverted index and “word-tokens” file to calculate the scores using BM25 retrieval model.

2. ranking.py
————

This is the ranking program which takes the inverted_index JSON file and calculates its BM25 score (taken from Assignment 4). However, we have modified the scoring in order to make the documents having proximity terms to be ranked higher. 

In our approach, we normally calculate the BM25 score. Then we check all the scored documents to see which document has the query terms in proximity and exact order. 

We do this by revisiting the inverted index for all the words in the query and extracting the proximity information for one document in a separate list. We then compare the proximity information for that document to see whether that document contains query terms in proximity or not. We continue doing this step for all the documents that were scored by BM25 function.

When we encounter a document having query terms proximity, we add +10 to its BM25 score. We then reverse sort the list by the score, thus if a document has query terms in proximity then it appears at the top ranks.

3. BM25.py
———
This is the scoring function from Assignment 4

4. queries.txt

This file contains all the CACM queries provided by the professor in txt format and parsed by removing stop words.

5. queries_without_stopping.txt

This file contains all the CACM queries provided by the professor in txt format and parsed without removing stop words.


HOW TO RUN:

The CACM corpus in HTML format is converted to txt files and stored in “Corpus_with_stopping” and “Corpus_without_stopping” directories. 

First run the “ngrams-indexer.py” and provide the path to the corpus and ONLY make unigram inverted index. This will generate the inverted index JSON files along with other files.

Then run the “ranking.py”, make sure you are providing the appropriate query files “queries.txt” to the program and run it. This will generate 64 files, one for each query using the BM25 algorithm.

We have used the same EVALUATION CODE provided in the project, with a minor change.

The directories, “BM25_Prox_EVAL”, and “BM25_Stopping_Prox_EVAL” contains the evaluation results for unstopped and stopped corpus respectively.

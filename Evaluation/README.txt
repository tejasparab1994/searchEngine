This part of the project is the evaluation system. The main program is “evalauate.py” and it should be executed. All other programs are its dependencies. 

In the program, “evaluate.py”, there is a function call at the end. 
									
									evaluate("<source files>/","<destination files>/")

For source files, you should type the name of the retrieval model for which you want evaluation results. (For eg. "CACM_PRF/")
For destination files, you should type the name of the folder where you want the evaluation results to be pasted. (For eg. "CACM_PRF_EVAL/")

The results from the retrieval models are stored in their respective folders, eg. CACM_BM25 folder contains the results after using BM25 retrieval model on the original corpus (without stopping and without stemming). Similarly, CACM_STOPPED_BM25 folder contains the results after using BM25 retrieval model on the original corpus (after stopping).

This system reads the “cacm.rel.txt” file in order to get the relevance judgements and thus it shouldn’t be removed from the directory.

The folder “Evaluation Results” contain the evaluation results of the following:

1. CACM_BM25 (CACM corpus without stopping using BM25 retrieval model)
2. CACM_QLM (CACM corpus without stopping using Query Likelihood retrieval model)
3. CACM_TFIDF (CACM corpus without stopping using TFIDF retrieval model)
4. CACM_LUCENE (CACM corpus without stopping using LUCENE DEFAULT retrieval model)
5. CACM_PRF (CACM corpus without stopping, with pseudo relevance feedback using BM25 retrieval model)
6. CACM_STOPPED_BM25 (CACM corpus with stopping using BM25 retrieval model)
7. CACM_STOPPED_QLM (CACM corpus with stopping using Query Likelihood retrieval model)
8. CACM_STOPPED_TFIDF (CACM corpus with stopping using TFIDF retrieval model)

The result folders are named accordingly with "_EVAL" used as suffix for the above folder names.
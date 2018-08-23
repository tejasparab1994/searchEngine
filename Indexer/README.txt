The main file of this project is "process_corpus.py", all other files are dependencies. Please run "process_corpus.py"
file.

This is the indexer program that creates an inverted index from the provided HTML corpus files. The inverted index
is stored in JSON file. Along with the inverted index, we are also storing the entire corpus in a dictionary
data structure and storing it in another JSON file.

On running the program, you'll be asked to choose which type of inverted index do you want to create. Later you'll be
asked to enter the path to the corpus folder. The inverted index will be stored in its appropriate folder. All the
folders will be automatically created and you don't need to create any folder.

This program uses "cacm_stem.txt" file which is the stemmed corpus, and thus this file should not be removed from
the project folder.

For generating stopped inverted index/corpus, the "common_words.txt" file is used and thus, it shouldn't be removed
from the project folder.
# CS481-BioInformatics-Pattern-Matching
Given two sequences T and P we aim to find whether P occurs exactly within T, and if it does, the locations of P in T.  

Implemented using the following algorithms: 
*  Brute force search 
*  Knuth-Morris-Pratt 
*  Boyer-Moore. 
 
### Parameters: 
The program must make use of the following command-like arguments: 
* -i: path of the FASTA file to be queried (T). 
* -o: path of the FASTA file containing the query (Q) 
* -a: a value specifying the algorithm to be used. Said values are: – BF for brute force search. – KMP for Knuth-Morris-Pratt. – BM for Boyer-Moore. – A for all of them. In this case, each algorithm must be run individually and the best among them be reported at the end. 

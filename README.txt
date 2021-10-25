Muhammed Doğancan Yılmazoğlu
21801804
CS 481 - HW 1

This homework is completed using python3. Make file can run each one of the algorithms or all of the algorithms at once. Usage:
Brute-Force: make bf
Knuth-Morris-Pratt: make kmp
Boyer-Moore: make bm
All: make all

In order to use the make file, pattern sequence must be in patt.fa file while text sequence must in data.fa file. If custom files
from different directories needed to be used for testing, then either make file can be edited or single python3 command can be used since
the program is just a single python3 file. Usage:

python3 hw1.py -i [path of text file] -o [path of pattern file] -a [algorithm name: BF,KMP,BM,A]

May not run on python2, so python3 must be strictly used for running the program.

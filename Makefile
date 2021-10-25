all:
	python3 hw1.py -i ./data.fa -o ./patt.fa -a A
kmp:
	python3 hw1.py -i ./data.fa -o ./patt.fa -a KMP
bm:
	python3 hw1.py -i ./data.fa -o ./patt.fa -a BM
bf:
	python3 hw1.py -i ./data.fa -o ./patt.fa -a BF
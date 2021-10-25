import argparse
import sys
import os.path
import time

def bruteForce(sequence,pattern):
    foundIndex = -1 
    comparisons = 0

    for i in range(0, len(sequence)):
        for j in range(0,len(pattern)):
            if(i + j < len(sequence)):
                if(sequence[i + j] != pattern[j]):
                    comparisons += 1
                    break
                else:
                    comparisons += 1
                    if( j >= len(pattern) - 1):
                        comparisons += 1
                        foundIndex = i
                        return foundIndex, comparisons
            else:
                break

    return foundIndex, comparisons

def KmpFailureGen(pattern):
    failure = [None] * len(pattern)
    failure[0] = 0
    index1 = 1
    index2 = 0

    while index1 < len(pattern):
        if(pattern[index1] == pattern[index2] ):
            failure[index1] = index2 + 1
            index1 = index1 + 1
            index2 = index2 + 1
        elif index2 > 0:
            index2 = failure[index2-1]
        else:
            failure[index1] = 0
            index1 = index1 + 1

    return failure

def Kmp(sequence,pattern):
    failure = KmpFailureGen(pattern)
    index1 = 0
    index2 = 0
    comparisons = 0

    while index1 < len(sequence):
        
        if(sequence[index1] == pattern[index2]):
            comparisons += 1
            if index2 == len(pattern) - 1:
                return index1 - index2, comparisons
            else:
                index1 = index1 + 1
                index2 = index2 + 1
        else:
            comparisons += 1
            if index2 > 0:
                index2 = failure[index2 - 1]
            else:
                index1 = index1 + 1
                index2 = 0
    
    return -1, comparisons

def goodSuffixOne(pattern):
    gs1 = [None] * len(pattern)
    m = len(pattern)
    gs1[m-1] = 0

    for j in range(1,len(pattern)):
        foundK = -1

        for k in range(m-j,m):
            if(pattern[k-m+j-1] != pattern[j-1]):
                if(pattern[j:m] == pattern[k-m+j:k]):
                    foundK = k
        
        if(foundK != -1):
            gs1[j-1] = foundK
        else:
            gs1[j-1] = 0       
    return gs1

def goodSuffixTwo(pattern):
    gs2 = [0] * len(pattern)
    m = len(pattern)
    gs2[m-1] = 0

    for j in range(1,m):
        for k in range(0,m-j):
            if(pattern[0:k+1] == pattern[m-k-1:m]):
                gs2[j-1] = k + 1

    return gs2

def genGoodSuffixTable(pattern):
    gst = [None] * len(pattern)
    gs1 = [None] * len(pattern)
    gs2 = [None] * len(pattern)
    m = len(pattern)

    gs1 = goodSuffixOne(pattern)
    gs2 = goodSuffixTwo(pattern)

    for j in range(0, len(pattern)):
        gst[j] = m - max(gs1[j],gs2[j])

    gst[m-1] = 1

    return gst

def badCharacterTable(pattern):
    chars = list(set(pattern))
    chars.sort()
    bct = [[None for x in range(len(chars))] for y in range(len(pattern))]

    for i in range(0,len(pattern)):
        for j in range(0,len(chars)):
            bct[i][j] = pattern[0:i+1].rfind(chars[j])

    return bct

def boyerMoore(sequence,pattern):
    gst = genGoodSuffixTable(pattern)
    bct = badCharacterTable(pattern)
    chars = list(set(pattern))
    chars.sort()

    n = len(sequence)
    m = len(pattern)

    i = m - 1 
    j = m - 1
    lastIndex = m -1

    comparisons = 0
 
    while i >= 0 and i < n:
        if( j  < 0):
            return i + 1, comparisons

        while j >= 0:
            lastIndex = i

            if(sequence[i] == pattern[j]):
                comparisons += 1
                i = i - 1

                if(i < 0):
                    break

                j = j - 1
            else:
                comparisons += 1
                gstValue = gst[j]

                if(sequence[i] in chars):
                    bctValue = bct[j][chars.index(sequence[i])]
                else:
                    bctValue = 0

                if(gstValue >= bctValue):
                    shift = gstValue 
                    j = m - 1
                    i = lastIndex + shift

                    if(i >= n):
                        break
                else:
                    shift = m - bctValue - 1
                    j = m - 1
                    i = lastIndex + shift
                    if(i >= n):
                        break
    
    return -1,comparisons

parser = argparse.ArgumentParser(description="Pattern Matching Program using bruteforce,Knuth-Morris-Pratt, Boyer-Moore Algorithms")
parser.add_argument("-i", type=str, required=True, help="Path of the FASTA file to be queried")
parser.add_argument("-o", type=str,required=True, help="Path of the FASTA file containing the query")
parser.add_argument("-a", type=str,required=True, help="A value specifiying the algorithm to be used which are BF, KMP, BM, A")

args = parser.parse_args()

file1Path = args.i
file2Path = args.o
algoType = args.a

if(not os.path.isfile(file1Path)):
    print(file1Path + ": file does not exists")
    sys.exit()

if(not os.path.isfile(file2Path)):
    print(file2Path + ": file does not exists")
    sys.exit()

if(not (algoType == "BF" or  algoType == "KMP" or algoType == "BM" or algoType == "A")):
    print(algoType + " is not a valid algorithm type parameter")
    sys.exit()

file1 = open(file1Path) 
file2 = open(file2Path)

sequence = ""
pattern = ""

for line in file1.readlines():
    if(line.startswith(">")):
        continue
    sequence = sequence + line.replace("\n","")

for line in file2.readlines():
    if(line.startswith(">")):
        continue
    pattern = pattern + line.replace("\n","")


if(algoType == "BF"):
    startTime = time.time()
    result = bruteForce(sequence,pattern)
    endTime = time.time()

    if(result[0] != -1):
        print("pattern was found in query file at position " + str(result[0] + 1))
    else:
        print("pattern was not found in query file")

    print(str(result[1]) + " character comparisons performed.")
    print("Run time was " + str(int((endTime - startTime)*1000)) + " ms.")
elif(algoType == "KMP"):
    startTime = time.time()
    result = Kmp(sequence,pattern)
    endTime = time.time()

    if(result[0] != -1):
        print("pattern was found in query file at position " + str(result[0] + 1))
    else:
        print("pattern was not found in query file")

    print(str(result[1]) + " character comparisons performed.")
    print("Run time was " + str(int((endTime - startTime)*1000)) + " ms.")
elif(algoType == "BM"):
    startTime = time.time()
    result = boyerMoore(sequence,pattern)
    endTime = time.time()

    if(result[0] != -1):
        print("pattern was found in query file at position " + str(result[0] + 1))
    else:
        print("pattern was not found in query file")

    print(str(result[1]) + " character comparisons performed.")
    print("Run time was " + str(int((endTime - startTime)*1000)) + " ms.")
elif(algoType == "A"):
    startTime = time.time()
    resultBF = bruteForce(sequence,pattern)
    endTime = time.time()

    print("Brute Force:")
    if(resultBF[0] != -1):
        print("pattern was found in query file at position " + str(resultBF[0] + 1))
    else:
        print("pattern was not found in query file")

    print(str(resultBF[1]) + " character comparisons performed.")
    print("Run time was " + str(int((endTime - startTime)*1000)) + " ms.")

    print()

    startTime = time.time()
    resultKMP = Kmp(sequence,pattern)
    endTime = time.time()

    print("Knuth-Morris-Pratt:")
    if(resultKMP[0] != -1):
        print("pattern was found in query file at position " + str(resultKMP[0] + 1))
    else:
        print("pattern was not found in query file")

    print(str(resultKMP[1]) + " character comparisons performed.")
    print("Run time was " + str(int((endTime - startTime)*1000)) + " ms.")

    print()

    startTime = time.time()
    resultBM = boyerMoore(sequence,pattern)
    endTime = time.time()

    print("Boyer-Moore:")
    if(resultBM[0] != -1):
        print("pattern was found in query file at position " + str(resultBM[0] + 1))
    else:
        print("pattern was not found in query file")

    print(str(resultBM[1]) + " character comparisons performed.")
    print("Run time was " + str(int((endTime - startTime)*1000)) + " ms.")

    results = [resultBF[1],resultKMP[1],resultBM[1]]
    index = results.index(min(results))

    print()

    if(index == 0):
        print("The best algorithm was Brute Force")
    elif(index == 1):
        print("The best algorithm was Knuth Morris Pratt")
    elif(index == 2):
        print("The best algorithm was Boyer Moore")

file1.close()
file2.close()
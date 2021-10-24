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
                        foundIndex = i
                        return foundIndex, comparisons
            else:
                break    
                
        # if(sequence[i: i+len(pattern)] == pattern):
        #     foundIndex = i
        #     break

    return foundIndex, comparisons

def KmpFailureGen(pattern):
    failure = [None] * len(pattern)
    failure[0] = 0
    i = 1
    j = 0

    while i < len(pattern):
        if(pattern[i] == pattern[j] ):
            failure[i] = j +1
            i = i + 1
            j = j + 1
        elif j > 0:
            j = failure[j-1]
        else:
            failure[i] = 0
            i = i + 1

    return failure

def Kmp(sequence,pattern):
    failure = KmpFailureGen(pattern)
    i = 0
    j = 0
    comparisons = 0

    while i < len(sequence):
        
        if(sequence[i] == pattern[j]):
            comparisons += 1
            if j == len(pattern) - 1:
                return i - j, comparisons
            else:
                i = i + 1
                j = j + 1
        else:
            comparisons += 1
            if j > 0:
                j = failure[j - 1]
            else:
                i = i + 1
                j = 0
    
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
    
    return 0,comparisons

parser = argparse.ArgumentParser(description="Pattern Matching Program using bruteforce,Knuth-Morris-Pratt, Boyer-Moore Algorithms")
parser.add_argument("-i", type=str, required=True, help="Path of the FASTA file to be queried")
parser.add_argument("-o", type=str,required=True, help="Path of the FASTA file containing the query")
parser.add_argument("-a", type=str,required=True, help="A value specifiying the algorithm to be used which are BF, KMP, BM, A")

args = parser.parse_args()

# print(args.i)
# print(args.o)
# print(args.a)

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

file1 = open("data.fa") 
file2 = open("patt.fa")

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

    print("pattern was found in query file at position " + str(result[0]))
    print(str(result[1]) + " character comparisons performed.")
    print("Run time was " + str(((endTime - startTime)*1000)) + " ms.")
elif(algoType == "KMP"):
    startTime = time.time()
    result = Kmp(sequence,pattern)
    endTime = time.time()

    print("pattern was found in query file at position " + str(result[0]))
    print(str(result[1]) + " character comparisons performed.")
    print("Run time was " + str(((endTime - startTime)*1000)) + " ms.")
elif(algoType == "BM"):
    startTime = time.time()
    result = boyerMoore(sequence,pattern)
    endTime = time.time()

    print("pattern was found in query file at position " + str(result[0]))
    print(str(result[1]) + " character comparisons performed.")
    print("Run time was " + str(((endTime - startTime)*1000)) + " ms.")
elif(algoType == "A"):
    startTime = time.time()
    resultBF = bruteForce(sequence,pattern)
    endTime = time.time()

    print("pattern was found in query file at position " + str(resultBF[0]))
    print(str(resultBF[1]) + " character comparisons performed.")
    print("Run time was " + str(((endTime - startTime)*1000)) + " ms.")

    print()

    startTime = time.time()
    resultKMP = Kmp(sequence,pattern)
    endTime = time.time()

    print("pattern was found in query file at position " + str(resultKMP[0]))
    print(str(resultKMP[1]) + " character comparisons performed.")
    print("Run time was " + str(((endTime - startTime)*1000)) + " ms.")

    print()

    startTime = time.time()
    resultBM = boyerMoore(sequence,pattern)
    endTime = time.time()

    print("pattern was found in query file at position " + str(resultBM[0]))
    print(str(resultBM[1]) + " character comparisons performed.")
    print("Run time was " + str(((endTime - startTime)*1000)) + " ms.")

    results = [resultBF[1],resultKMP[1],resultBM[1]]
    index = results.index(min(results))

    if(index == 0):
        print("The best algorithm was Brute Force")
    elif(index == 1):
        print("The best algorithm was Knuth Morris Pratt")
    elif(index == 2):
        print("The best algorithm was Boyer Moore")


# f = KmpFailureGen("abaaba")

# print("failure: ", f)

# print("KMP: ", Kmp(sequence,pattern));

# print(goodSuffixOne("ATCACATCATCA"))

#print(badCharacterTable("ATCACATCATCA"))




# print(goodSuffixOne(pattern))
# print(goodSuffixTwo(pattern))
#print(goodSuffixTwo(pattern))
file1.close()
file2.close()
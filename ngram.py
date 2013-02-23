from __future__ import with_statement
import sys
import itertools
import nltk.data
import copy
import random
from nltk.tokenize import WordPunctTokenizer


sentence = """STARTSEN You will rejoice to hear that no disaster has accompanied the
commencement of an enterprise which you have regarded with such evil
forebodings.ENDSEN STARTSEN  I arrived here yesterday, and my first task is to assure
my dear sister of my welfare and increasing confidence in the success
of my undertaking. ENDSEN"""
sentence2 = "That's just like, your opinion, man"
unigrams = dict()
ngrams = dict()
totalCount = 0


#Perhaps make an ngram object
#Could be a list of the n words

def unigram():
    for w in sentence.split(" "):
        if w in unigrams:
            unigrams[w] = unigrams.pop(w) + 1
        else:
            unigrams[w] = 1
'''
def nltkTest():
    text = """
... Punkt knows that the periods in Mr. Smith and Johann S. Bach
... do not mark sentence boundaries.  And sometimes sentences
... can start with non-capitalized words.  i is a good variable
... name.
... """
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    print '\n-----\n'.join(sent_detector.tokenize(text.strip()))
'''

#n: number of grams (1 = unigram, 2 = bigram, etc.)
#words: a group of words to model
#Returns a dictionary with keys that strings representing lists of words, and values that are counts
#TO-DO: Punctuation (find and replace should do the trick)
smoothingBound = 3 #Will eventually turn this into a param whenever I figure this out
def ngram(n, words):
    global totalCount
    countList = [0]*(smoothingBound + 1)
    prev = list()
    vocab = dict()
    for w in WordPunctTokenizer().tokenize(words):
        #Convert everything to lowercase. Check that this is ok
        w = w.lower()
        #This happens to be a unigram
        if w in vocab:
            vocab[w] = vocab.pop(w) + 1
        else:
            vocab[w] = 1
        #Mantain queue of n most recent words
        if len(prev) >= n:
            prev.pop(0)
        #Look up n-1 words + current word in HT
        prev.append(w)
        if len(prev) < n:
            continue
        totalCount = totalCount + 1
        temp = copy.deepcopy(prev)
        nthWord = temp.pop()
        nMinusOneKey = str(temp)
        if nMinusOneKey in ngrams:
            miniDict = ngrams[nMinusOneKey] #Copy or pointer?
            if nthWord in miniDict:
                miniDict[nthWord] = miniDict.pop(nthWord) + 1
            else:
                miniDict[nthWord] = 1
        else:
            ngrams[nMinusOneKey] = {nthWord : 1}
        count = ngrams[nMinusOneKey][nthWord]
        if count > 1:
            countList[count-1] -= 1
        if count <= smoothingBound:
            countList[count] += 1
    countList[0] = totalCount**n - len(ngrams)
    #print("---")
    #print(countList)
    #print("---")
    fillZeros(vocab, n)
    #print(ngrams)
    applySmoothing(countList, smoothingBound)
        
def fillZeros(vocab, n):
    for perm in itertools.product(vocab.keys(), repeat=n):
        key = list()
        for p in perm[0:(n-1)]:
            key.append(p)
        last = str(perm[n-1])
        key = str(key)
        
        #key = key.replace("(", "[")
        #key = key.replace(")", "]")
        #Do this better. Data with parentheses will break ^
        if not (key in ngrams): 
            ngrams[key] = {last : 0};
        else:
            if not (last in ngrams[key]):
                (ngrams[key])[last] = 0 

#Utility functions for our special nested dictionary
def updateCount(dict, ngram, newCount):
    #Convert the string input to a list
    l = [ngram.strip(" '") for ngram in ngram.strip('[]').split(',')]
    #the last word
    word = l.pop() 
    key = str(l)
    if key in dict and word in dict[key]:
        dict[key][word] = newCount
        return
    print("WARNING: " + ngram + " is not in the current model, so it can't be updated")

def getCount(dict, ngram):
    #Convert the string input to a list
    l = [ngram.strip(" '") for ngram in ngram.strip('[]').split(',')]
    #the last word
    word = l.pop() 
    key = str(l)
    if key in dict and word in dict[key]:
        return dict[key][word]
    return 0

#Currently not used
def gtSmooth(countList, ngram, smoothingBound):
    count = 0
    if ngram in ngrams:
        count = ngrams[ngram]
    if count >= smoothingBound:
        return count
    return (count + 1) * (countList[count+1] / countList[count])

#Applies Good-Turing smoothing to all ngrams in dict that appear less than bound times
#We might have to iterate over the whole dictionary. Yuck.
#Optimization could be to iterate before we fill with zeros - the dict will be much smaller
def applySmoothing(countList, smoothingBound):
    for k in ngrams.keys():
        for k2 in ngrams[k].keys():
            count = ngrams[k][k2]
            if count < smoothingBound:
                ngrams[k][k2] = (count + 1) * (float(countList[count+1]) / float(countList[count]))

def randomSentence():
    prev = "['startsen']"
    sentence = ""
    #Import bigram table if it exists
    #Otherwise generate one
    while True:
        sum = float(0)
        rand = random.random()
        if prev in ngrams:
            for v in ngrams[prev].values():
                sum += v
            print("COUNT: " + str(sum))
            runningSum = float(0)
            for (k,v) in ngrams[prev].iteritems():
                runningSum += v / sum
                if (runningSum >= rand):
                    if k == "startsen":
                        break
                    if k == "endsen":
                        return sentence
                    sentence += " " + k
                    prev = "['" + k + "']"
        else:
            print("Error: " + prev + " not in ngram model")
            break



#ngram(int(sys.argv[1]), sentence)

ngram(2, sentence)
print("Count 0: "+ str(getCount(ngrams, "['ate', 'apple']")))
print("Random sentence: " + randomSentence())
print(ngrams["['.']"])
#print(str(ngrams))
print(totalCount)
#nltkTest()

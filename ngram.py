from __future__ import with_statement
import sys
import itertools
import nltk.data
import copy


sentence = "Apple ate an Apple"
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
def ngram(n, words):
    global totalCount
    prev = list()
    vocab = dict()
    for w in words.split(" "):
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

    fillZeros(vocab, n)
        
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
    pass

def getCount(dict, ngram):
    pass

#Applies Good-Turing smoothing to all ngrams in dict that appear less than bound times
#We might have to iterate over the whole dictionary. Yuck.
#Optimization could be to iterate before we fill with zeros - the dict will be much smaller
def gtSmooth(dict, bound):
    pass
#ngram(int(sys.argv[1]), sentence)
ngram(3, sentence)
#print(unigrams["Apple"])
print(str(ngrams))
print(totalCount)
#nltkTest()

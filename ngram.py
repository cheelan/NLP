from __future__ import with_statement
import sys
import itertools
import nltk.data
import copy
import random
from nltk.tokenize import WordPunctTokenizer

class Gram:
    dictionary = None
    n = 0
    word_count = 0

    def __init__(self, args):
        self.n = args
        self.dictionary = {}

    def print_out(self):
        sorted_dictionary = sorted(self.dictionary.iteritems(), key= operator.itemgetter(1), reverse = True)
        print(sorted_dictionary[:100])

    def add(self, word):
        if word in self.dictionary:
            self.dictionary[word]+=1
        else:
            self.word_count+=1
            self.dictionary[word] = 1

sentence = """STARTSEN You will rejoice to hear that no disaster has accompanied the
commencement of an enterprise which you have regarded with such evil
forebodings.ENDSEN STARTSEN  I arrived here yesterday, and my first task is to assure
my dear sister of my welfare and increasing confidence in the success
of my undertaking. ENDSEN"""

unigrams = dict()
ngrams = dict()
totalCount = 0
countList = []

#n: number of grams (1 = unigram, 2 = bigram, etc.)
#text: a text corpus to model
#Returns a dictionary with keys that strings representing lists of words, and values that are counts
#TO-DO: Punctuation (find and replace should do the trick)
def ngram(n, text, smoothingBound = 3):
    global totalCount
    global countList
    countList = [0]*(smoothingBound + 1)
    prev = list()
    vocab = dict()
    for sentence in nltk.tokenize.sent_tokenize(text):
        for w in WordPunctTokenizer().tokenize(text):
        for word in nltk.tokenize.word_tokenize(i)
            #Convert everything to lowercase. Check that this is ok
            w = w.lower()
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
    applySmoothing(smoothingBound)

#sent: a regular sentence string, not delimited or anything
#model: the n-gram model of choice
#n: the n in n-gram
#output: a score proportional to the probability of the sentence coming from that model
#Handling unknowns... hmmm
def getSentencePerplexity(sent, model, n):
    p = 1.0
    lst = list()
    for w in WordPunctTokenizer().tokenize(sent):
        w = w.lower()
        lst.append(w)
        if len(lst) < n:
            continue
        if len(lst) > n:
            lst.pop(0)
        nMinusOne = str(lst.pop())
        key = str(lst)
        #Need to adjust these for unknown words
        if not (key in model):
            return 0
        if not (nMinusOne in model[key]):
            p *= (float(countList[1]) / float(countList[0]))
            continue
        i = 0
        sum = 0.
        for v in model[key].values():
            i += 1
            sum += v
        #TO-DO Let's double check that..
        sum += float(totalCount - i) * (float(countList[1]) / float(countList[0])) 
        p *= 1. / (float(model[key][nMinusOne]) / sum)

    return p**(1. / float(len(sent)))

        
        
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
def gtSmooth(ngram, smoothingBound):
    count = 0
    if ngram in ngrams:
        count = ngrams[ngram]
    if count >= smoothingBound:
        return count
    return (count + 1) * (countList[count+1] / countList[count])

#Applies Good-Turing smoothing to all ngrams in dict that appear less than bound times
#We might have to iterate over the whole dictionary. Yuck.
#Optimization could be to iterate before we fill with zeros - the dict will be much smaller
def applySmoothing(smoothingBound):
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
            i = 0
            for v in ngrams[prev].values():
                i += 1
                sum += v
            #sum += float(totalCount - i) * p
                #TO-DO: Need to add in (total number of ngrams possible - ngrams seen) * prob(0 occurrences)
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
                    break
            #TO-DO: If this part is reached, then pick a random gram that appears 0 times
        else:
            print("Error: " + prev + " not in ngram model")
            break



#ngram(int(sys.argv[1]), sentence)

ngram(2, sentence)
print("Count 0: "+ str(getCount(ngrams, "['ate', 'apple']")))
#print("Random sentence: " + randomSentence())
print("Score of a sentence: " + str(getSentencePerplexity("You will rejoice to hear that no disaster has accompanied", ngrams, 2)))
#print(ngrams["[',']"])
#print(str(ngrams))

#nltkTest()

from __future__ import with_statement

"hi"
sentence = "Apple ate an Apple"
unigrams = dict()
ngrams = dict()

#Perhaps make an ngram object
#Could be a list of the n words

def unigram():
    for w in sentence.split(" "):
        if w in unigrams:
            unigrams[w] = unigrams.pop(w) + 1
        else:
            unigrams[w] = 1


#n: number of grams (1 = unigram, 2 = bigram, etc.)
#words: a group of words to model
#Returns a dictionary with keys that strings representing lists of words, and values that are counts
#TO-DO: Punctuation (find and replace should do the trick)
def ngram(n, words):
    prev = list()
    for w in words.split(" "):
        #Convert everything to lowercase. Check that this is ok
        w = w.lower()
        #Mantain queue of n most recent words
        if len(prev) >= n:
            prev.pop(0)
        #Look up n-1 words + current word in HT
        prev.append(w)
        if len(prev) < n:
            continue
        hashcode = str(prev)
        if hashcode in ngrams:
            ngrams[hashcode] = ngrams.pop(hashcode) + 1
        else:
            ngrams[hashcode] = 1
        
        
        

unigram()
ngram(3, sentence)
print(unigrams["Apple"])
print(str(ngrams))


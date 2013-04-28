import math, time
from ngram import *
import Queue
import covertree
import pickle

class Knn:
    #token_list: List of lists of words/characters/parts of speech that'll we'll turn into ngrams
    def __init__(self, k, n, deceptive_list, truthful_list, importname=""):
        if importname != "":
            with open(importname, 'rb') as f:
                self.ct = pickle.load(f)
                print("Loaded training file " + importname)
            return
        self.k = k
        self.n = n
        self.deceptive_ngrams = list() #Each training sentence gets its own n-gram model
        self.truthful_ngrams = list()
        for lst in deceptive_list:
            self.deceptive_ngrams.append(Gram(n, lst, 0))
        for lst in truthful_list:
            self.truthful_ngrams.append(Gram(n, lst, 0))
        self.ct = covertree.CoverTree(manhattan)
        for ngram in self.deceptive_ngrams:
            self.ct.insert((ngram, 0))
        for ngram in self.truthful_ngrams:
            self.ct.insert((ngram, 1))
        #Pickle this
        with open('knn.pickle', 'wb') as f: 
            pickle.dump(self.ct, f)
            print("Done pickling")
        
 
    def skclassify(self, test_lst):

        ans = []
        print("Starting the fun")
        for t in test_lst:
            knns = self.ct.knn(self.k, (Gram(self.n, t, 0), 0))
            reals = 0
            fakes = 0
            for neighbor in knns:
                if neighbor[0][1] == 0:
                    fakes += 1
                else:
                    reals += 1
            if reals > fakes:
                #print(1)
                ans.append(1)
            elif reals < fakes:
                #print(0)
                ans.append(0)
            else:
                ans.append(1)
        return ans


    #Returns true iff istruthful. Assumes that test was broken down into a list of words/pos/chars
    def classify(self, test):
        start = time.time()
        #Generate an n-gram for test
        test_ngram = Gram(self.n, test, 0) 
        end = time.time()
        print("Time for ngram" + str(end - start))
        start = time.time()
        #For each ngram in the deceptive and truthful ngrams, calculate the distance and keep track of the k closest training examples
        q = Queue.PriorityQueue()
        for ngram in self.truthful_ngrams:
            q.put((self.manhattan(test_ngram, ngram), True))
        for ngram in self.deceptive_ngrams:
            q.put((self.manhattan(test_ngram, ngram), False))
        end = time.time()
        print("Time for populating queue" + str(end - start))
        start = time.time()
        #Check to see who has the majority of the neighbors
        trueCount = 0
        falseCount = 0
        for i in range(0, self.k):
            (score, isTruthful) = q.get()
            if (isTruthful):
                trueCount += 1
            else:
                falseCount += 1
        end = time.time()
        print("Time for finding k nearest neighbors" + str(end - start))
        print("")
        return trueCount > falseCount
        #What to do about ties? Currently biased towards deceptive

    #Returns the normalized manhattan distance between the test n-gram and a train n-gram
def manhattan(test_ngram, train_ngram):
    #Only needed with cover tree
    test_ngram = test_ngram[0]
    train_ngram = train_ngram[0]

    sum = 0.
    for ngram in test_ngram.dictionary.keys():
        sum += math.fabs(test_ngram.get_count(ngram) - train_ngram.get_count(ngram))
    for ngram in train_ngram.dictionary.keys():
        sum += math.fabs(train_ngram.get_count(ngram) - test_ngram.get_count(ngram))
    return float(sum) / float((len(test_ngram.dictionary.keys()) + len(train_ngram.dictionary.keys())))
        
    
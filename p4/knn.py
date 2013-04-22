import math
import ngram
class Knn:
    #token_list: List of lists of words/characters/parts of speech that'll we'll turn into ngrams
    def init(self, k, n, deceptive_list, truthful_list):
        self.k = k
        self.n = n
        self.decptive_ngrams = list() #Each training sentence gets its own n-gram model
        self.truthful_ngrams = list()
        for lst in deceptive_list:
            self.decptive_ngrams.append(ngram.Gram(n, lst, 0))
        for lst in truthful_list:
            self.truthful_ngrams.append(ngram.Gram(n, lst, 0))

    #Returns true iff istruthful. Assumes that test was broken down into a list of words/pos/chars
    def classify(self, test):
        #Generate an n-gram for test
        test_ngram = ngram(n, test, 0) 
        #For each ngram in the deceptive and truthful ngrams, calculate the distance and keep track of the k closest training examples
        q = Queue.PriorityQueue()
        for ngram in self.truthful_ngrams:
            q.put((self.manhattan(test_ngram, ngram), True))
        for ngram in self.deceptive_ngrams:
            q.put((self.manhattan(test_ngram, ngram), False))
        #Check to see who has the majority of the neighbors
        trueCount = 0
        falseCount = 0
        for i in range(0, self.k):
            (score, isTruthful) = q.pop()
            if (isTruthful):
                trueCount += 1
            else:
                falseCount += 1
        return trueCount > falseCount
        #What to do about ties? Currently biased towards deceptive

    #Returns the normalized manhattan distance between the test n-gram and a train n-gram
    def manhattan(self, test_ngram, train_ngram):
        sum = 0.
        for ngram in test_ngram.dictionary.keys():
            sum += math.fabs(test_ngram.get_count(ngram) - train_ngram.get_count(ngram))
        for ngram in train_ngram.dictionary.keys:
            sum += math.fabs(train_ngram.get_count(ngram) - test_ngram.get_count(ngram))
        return sum / (len(test_ngram.dictionary.keys) + len(train_ngram.dictionary.keys))
    
import math
import ngram
from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist, GoodTuringProbDist

class Perplexity:
    #deceptive_list: List of every word/char/pos in every review (unlike knn, this is just a list,
    #not a list of lists)
    def __init__(self, n, smoothingBound, deceptive_list, truthful_list):
        #self.deceptive_model = ngram.Gram(n, deceptive_list, smoothingBound)
        #self.truthful_model = ngram.Gram(n, truthful_list, smoothingBound)
        est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        
        self.deceptive_model = NgramModel(n, deceptive_list, estimator=est)
        self.truthful_model = NgramModel(n, truthful_list, estimator=est)
    
    def classify(self, test):
        #ptrue = self.truthful_model.getPerplexity(test) 
        #pdeceptive = self.deceptive_model.getPerplexity(test) 
        ptrue = self.truthful_model.perplexity(test)
        pdeceptive = self.deceptive_model.perplexity(test)
        if ptrue < pdeceptive:
            return 0
        elif ptrue > pdeceptive:
            return 1
        else:
            print("Perplexity tie")
            return 1

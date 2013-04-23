import math
import ngram
class Perplexity:
    #deceptive_list: List of every word/char/pos in every review (unlike knn, this is just a list,
    #not a list of lists)
    def __init__(self, n, smoothingBound, deceptive_list, truthful_list):
        self.deceptive_model = ngram.Gram(n, deceptive_list, smoothingBound)
        self.truthful_model = ngram.Gram(n, truthful_list, smoothingBound)
    
    def classify(self, test):
        return self.truthful_model.getPerplexity(test) > self.deceptive_model.getPerplexity(test) 
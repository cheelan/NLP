import sys, itertools, copy, random, nltk.tokenize, os, re, math

class Word:
    total_count = 0
    senses = None

    def __init__(self):
        pass
    
    def get_sense_prob(self, sense):
        pass

    def add_sense(self, sense):
        pass


class Sense:
    occurrences = 0
    featureUnigram = None

    def __init__(self):
        pass

    #If feature does not occur, return a smoothed value
    def get_feature_count(self, feature):
        pass

#For testing and such
class Supervised:
    
    def __init__(self):
        pass



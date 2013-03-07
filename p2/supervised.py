import sys, itertools, copy, random, nltk.tokenize, os, re, math

class Word:
    total_count = 0
    senses = None

    def __init__(self):
        self.senses = dict()
    
    def get_sense_count(self, sense):
        if sense in self.senses:
            return self.senses[sense].occurrences
        else:
            #TO-DO: SMOOTH
            return 0

    def add_sense(self, sense):
        this.senses[sense] = Sense()

    def add_feature(self, sense, feature):
        #Check if sense is in the dictionary
        #Call Sense.add_feature
        pass


class Sense:
    occurrences = 0
    featureUnigram = None

    def __init__(self):
        self.featureUnigram = dict()
    
    #or perhaps add_features
    def add_feature(self, feature):
        if feature in self.featureUnigram:
            self.featureUnigram[feature] += 1
        else:
            self.featureUnigram[feature] = 1

    def get_feature_count(self, feature):
        if feature in self.featureUnigram:
            return self.featureUnigram[feature]
        #TO-DO: Return a smoothed value
        return 0

#For testing and such
class Supervised:
    word_sense_dictionary = None

    def __init__(self):
        this.word_sense_dictionary = dict()

    #Trains the model on one line's worth of info
    #Need to account for case, stemming, etc
    #Senses is a list of ints
    def train_line(context, target, senses):
        #Lookup target in the dictionary
        if target not in self.word_sense_dictionary:
            self.word_sense_dictionary[target] = Word()
        for s in senses:
            self.word_sense_dictionary[target].add_sense(s)
        #Call add_features(context) on the entry
        #Update word/sense counts
        
        pass

    #Given a train file, fill in the nested dictionary
    def train(file):
        pass

    def test(file):
        pass



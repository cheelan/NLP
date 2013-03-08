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
        self.senses[sense] = Sense()

    def add_features(self, sense, features):
        #Check if sense is in the dictionary
        if not sense in self.senses:
            self.senses[sense] = Sense()
        for f in features:
            self.senses[sense].add_feature(f)


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
        self.word_sense_dictionary = dict()

    #target: the word to disambiguate
    #sense: An int between 0 and n-1, where n is the number of senses that the word has
    def get_sense_prob(self, target, sense):
        if target not in self.word_sense_dictionary:
            print("ERROR: " + target + " not in dictionary")
            return -1
        if sense not in self.word_sense_dictionary[target].senses:
            print("ERROR: " + sense + " is not a valid sense")
        features = self.word_sense_dictionary[target].senses[sense]
        prob = get_initial_prob()
        #Abstract this to another method
        #get the feature count count(f_j, s)
        sense_count = self.word_sense_dictionary[target].senses[sense].occurrences
        for f in features.featureUnigram.keys():
            feature_count = features.get_feature_count(f)
            prob *= float(feature_count) / float(sense_count)
        return prob
    
    #TO-DO
    def get_initial_prob():
        return 1.0

    #Trains the model on one line's worth of info
    #Need to account for case, stemming, etc
    #Senses is a list of ints
    def train_line(self, context, target, senses):
        #Convert context to features
        features = context.split(" ")
        #Lookup target in the dictionary
        if target not in self.word_sense_dictionary:
            self.word_sense_dictionary[target] = Word()
        #Call add_features(context) on the entry
        for s in senses:
            self.word_sense_dictionary[target].add_features(s, features)
        #Update word/sense counts

        pass

    #Given a train file, fill in the nested dictionary
    def train(self, file):
        pass

    def test(self, file):
        pass

    def print_dict(self):
        for w in self.word_sense_dictionary.keys():
            print(w + " : ")
            for s in self.word_sense_dictionary[w].senses:
                print("\t" + str(self.word_sense_dictionary[w].senses[s].featureUnigram))

s = Supervised()
s.train_line("I went fishing for some sea", "bass", [0])
s.train_line("The line of the song is too weak", "bass", [1])

s.print_dict()
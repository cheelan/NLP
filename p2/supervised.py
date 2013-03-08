import sys, itertools, copy, random, nltk, os, re, math
from nltk.stem.porter import PorterStemmer

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
            self.total_count += 1


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
        self.occurrences += 1

    def get_feature_count(self, feature):
        if feature in self.featureUnigram:
            return self.featureUnigram[feature]
        #TO-DO: Return a smoothed value
        return 0

#For testing and such
class Supervised:
    wsd = None

    def __init__(self):
        self.wsd = dict()

    #target: the word to disambiguate
    #sense: An int between 0 and n-1, where n is the number of senses that the word has
    def get_sense_prob(self, target, sense):
        if target not in self.wsd:
            print("ERROR: " + target + " not in dictionary")
            return -1
        if sense not in self.wsd[target].senses:
            print("ERROR: " + str(sense) + " is not a valid sense")
            return -1
        features = self.wsd[target].senses[sense]
        prob = self.get_initial_prob()
        #Abstract this to another method
        #get the feature count count(f_j, s)
        sense_count = self.wsd[target].senses[sense].occurrences
        for f in features.featureUnigram.keys():
            feature_count = features.get_feature_count(f)
            prob *= float(feature_count) / float(sense_count)
        return prob
    
    #TO-DO
    def get_initial_prob(self):
        return 1.0

    def train_line_test(self, context, target, senses):
        #Convert context to features
        features = context.split(" ")
        #Lookup target in the dictionary
        if target not in self.wsd:
            self.wsd[target] = Word()
        #Call add_features(context) on the entry
        for s in senses:
            self.wsd[target].add_features(s, features)
        #Update word/sense counts

        pass

    #Trains the model on one line's worth of info
    #Need to account for case, stemming, etc
    #Senses is a list of ints
    def train_line(self, text):
        #Convert text into partitions. 
        #features[0]: word.pos t0 t1 ... tk
        #features[1]: prev-context
        #features[2]: head
        #features[3]: next-context
        features = text.lower().split("@")
        # Handling of features[0] and combining of prev and next context into features
        senselist= re.findall('\w+', features[0])
        features = nltk.tokenize.regexp_tokenize((features[1] + " " + features[3]), r'\w+')
        # Stemming of all features
        ps = PorterStemmer()
        for i in range(len(features)):
            features[i] = ps.stem(features[i])
        # Word already exists.
        if self.wsd.contains_key(senselist[0]):
            pass
        else:
            self.wsd[senselist[0]] = Word()
            #for 

        '''
        #Lookup target in the dictionary
        if target not in self.wsd:
            self.wsd[target] = Word()
        #Call add_features(context) on the entry
        for s in senses:
            self.wsd[target].add_features(s, features)
        #Update word/sense counts
        '''

    #Given a train file, fill in the nested dictionary
    def train(self, filename):
        data = open(filename, 'r')
        if (data == None):
            print("Error: Training file not found")
        else:
            data = data.readlines()
            for line in data:
                self.train_line(line)

    def test(self, file):
        pass

    #Returns all senses that are good
    #Senses: List of 0s
    #@Return: Returns the senses list with 0s replaced by 1s
    def test_line(self, target, context, senses):
        ans_list = [0]*len(senses)
        thres = 0.0
        if target not in self.wsd:
            print("ERROR: " + target + " not in dictionary")
            pass
        sense_num = 0 #Skip the first sense because it's a "no-answer"
        for s in range(len(senses)-1):
            sense_num += 1
            score = self.get_sense_prob(target, sense_num)
            if score > thres:
                ans_list[sense_num] = 1
        print ans_list
                
            

    def print_dict(self):
        for w in self.wsd.keys():
            print(w + " : ")
            for s in self.wsd[w].senses:
                print("\t" + str(self.wsd[w].senses[s].featureUnigram))

s = Supervised()
#s.train("testing_data.data")
'''
s.train_line("I went fishing for some sea", "bass", [0])
s.train_line("The line of the song is too weak", "bass", [1])
s.print_dict()
'''

s.train_line_test("I went fishing for some sea", "bass", [1])
s.train_line_test("The line of the song is too weak", "bass", [2])
s.test_line("bass", "I fishing sea fish apple", [0, 0, 0])

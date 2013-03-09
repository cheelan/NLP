import sys, itertools, copy, random, nltk, os, re, math, string
from nltk.stem.porter import PorterStemmer

#Factor for +k smoothing
smoothing = .01

class Word:
    total_count = smoothing
    senses = None

    def __init__(self):
        self.senses = dict()
    
    def get_sense_count(self, sense):
        if sense in self.senses:
            return self.senses[sense].occurrences
        else:
            return smoothing

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
    occurrences = smoothing
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
        else:
            return smoothing

#For testing and such
class Supervised:
    wsd = None

    def __init__(self):
        self.wsd = dict()

    #target: the word to disambiguate
    #sense: An int between 0 and n-1, where n is the number of senses that the word has
    def get_sense_prob(self, target, context, sense):
        if target not in self.wsd:
            print("ERROR: " + target + " not in dictionary")
            return -1
        if sense not in self.wsd[target].senses:
            print("ERROR: " + str(sense) + " is not a valid sense")
            return -1
        features = self.wsd[target].senses[sense]
        prob = self.get_initial_prob(target, sense)
        #Abstract this to another method
        #get the feature count count(f_j, s)
        sense_count = self.wsd[target].get_sense_count(sense)
        for f in context:
            feature_count = features.get_feature_count(f)
            #print( str(float(feature_count)) + " / " + str(float(sense_count)))
            prob *= float(feature_count) / float(sense_count)
        #return prob
        return prob**(1. / float(len(context)))
    
    def get_initial_prob(self, target, sense):
        sense_count = self.wsd[target].get_sense_count(sense)
        word_count = self.wsd[target].total_count
        if word_count == 0:
            print("ERROR: No words in the dictionary")
        return float(sense_count) / float(word_count)

    #Given a line, fill in the nested dictionary
    def train_line(self, context, target, senses):
        #Convert context to feature words
        features = nltk.tokenize.regexp_tokenize(context, r'\w+')
        filtered_features = list()
        '''
        #Perforning feature filtering based on part of speach tag. 
        result = nltk.pos_tag(features)
        print(result)
        '''
        '''
        #Performing stemming on feature words
        ps = PorterStemmer()
        for i in range(len(features)):
            features[i] = ps.stem(features[i])
        '''
        #Lookup target in the dictionary
        if target not in self.wsd:
            self.wsd[target] = Word()
        #Call add_features(context) on the entry
        for s in senses:
            self.wsd[target].add_features(s, features)
            #Update word/sense counts
            self.wsd[target].senses[s].occurrences += 1

    #Given a train file, fill in the nested dictionary
    def train(self, filename):
        data = open(filename, 'r')
        if (data == None):
            print("Error: Training file not found")
        else:
            data = data.readlines()
            for line in data:
                #Convert text into partitions. #features[0]: word.pos t0 t1 ... tk
                #features[1]: prev-context, features[2]: head, features[3]: next-context
                features = line.lower().split("@")
                # Spliting of features[0] into components and combining of prev and next context into context
                senselist= re.findall('\w+', features[0])
                context = features[1] + features[3]
                # Handling of senselist
                senses = list()
                for i in range(3,len(senselist)):
                    if senselist[i] == "1":
                        senses.append(i-3)
                # Call the train line function to handle
                self.train_line(context, senselist[0], senses)


    #Returns all senses that are good
    #Senses: List of 0s
    #@Return: Returns the senses list with 0s replaced by 1s
    def test_line(self, target, context, senses):
        ans_list = list()
        ans_list.append(0) #First entry is a no-answer
        thres = 0.0
        sense_num = 0 
        features = context.split(" ")
        if target not in self.wsd:
            print("ERROR: " + target + " not in dictionary")
            pass
        for s in range(len(senses)-1):
            score = self.get_sense_prob(target, features, sense_num)
            print("Sense Num: " + str(sense_num) + " Value: " + str(score))
            if score > thres:
                ans_list.append(1)
            else:
                ans_list.append(0)
            sense_num += 1
        return ans_list

    def print_dict(self):
        for w in self.wsd.keys():
            print("Word: " + w )
            print("# of senses: " + str(len(self.wsd[w].senses)))
            for s in self.wsd[w].senses:
                print(str(s) + ":\t" + str(self.wsd[w].senses[s].featureUnigram))

s = Supervised()
s.train("testing_data.data")
print(str(s.test_line("begin", "There is the clearing of the room , the removal of any trace of what had previously filled it . There is the laying by of all the necessary materials . Not , he wrote ( and Goldberg went on typing ) , that here in London one is cut off from such supplies in the normal course of events , but that work cannot until one knows one will not have to bother with such things , for a while at least . It is not a question , he wrote , of drawing up an inventory of all that is required , because that suggests that one can know exactly what will be required . Everything possible must be done , he wrote , and yet it must be as though nothing had been done.", [0, 0, 0, 0, 0])))
#begin.v 0 0 1 0 0 @ There is the clearing of the room , the removal of any trace of what had previously filled it . There is the laying by of all the necessary materials . Not , he wrote ( and Goldberg went on typing ) , that here in London one is cut off from such supplies in the normal course of events , but that work cannot @begin@ until one knows one will not have to bother with such things , for a while at least . It is not a question , he wrote , of drawing up an inventory of all that is required , because that suggests that one can know exactly what will be required . Everything possible must be done , he wrote , and yet it must be as though nothing had been done .
'''
s.print_dict()
print(str(s.test_line("begin", "I need to begin to pay off the money I owe.", [0, 0, 0, 0, 0])))
'''
'''
s.train_line("I went fishing for some sea", "bass", [0])
s.train_line("The line of the song is too weak", "bass", [1])
s.print_dict()
'''
'''
s.train_line("I went fishing for some sea", "bass", [0])
s.train_line("sea fishing fish", "bass", [0])
s.train_line("The line of the song is too weak", "bass", [1])
print(str(s.test_line("bass", "I fishing sea fish apple", [0, 0, 0])))
'''

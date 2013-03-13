import sys, nltk, re, math, string, pickle
from nltk.stem.porter import PorterStemmer

#Factor for +k smoothing
smoothing = .01
thres = 0.03
allowed_pos = ["FW", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

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

    def add_features(self, sense, features):
        #Check if sense is in the dictionary
        if not sense in self.senses:
            self.senses[sense] = Sense()
        for f in features:
            self.senses[sense].add_feature(f)
        #Update word/sense counts
        self.total_count += 1
        self.senses[sense].occurrences += 1

    #Returns most frequently occurring sense. Used only for a base line, not the actual algorithm
    def get_most_common_sense(self):
        max_count = 0.
        max_sense = -1
        for (k, v) in self.senses:
            if v.occurrences > max_count:
                max_count = v.occurrences
                max_sense = k
        return max_sense

    #Returns the most common sense in answer format ie [0; 1; 0; 0]
    def get_common_sense_list(self):
        ans = list()
        best = self.get_most_common_sense()
        for i in range(len(self.senses)):
            if i == best:
                ans.append(1)
            else:
                ans.append(0)
        return ans

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
    #returns the total probability of the sense given the target word, context and sense
    def get_prob(self, target, context, sense):
        #Error checking. 
        if target not in self.wsd:
            print("ERROR: " + target + " not in dictionary")
            return -1
        if sense not in self.wsd[target].senses:
            #print("ERROR: " + str(sense) + " is not a valid sense")
            #print(self.wsd[target].senses)
            return 0.
        sense_prob = self.get_sense_prob(target, sense)
        features_prob = self.get_features_prob(target, sense, context)
        #Final probability calculation for the sense
        return sense_prob * (10**(float(features_prob) / float(len(context))))
    
    #Returns the probability of the sense given the word. Used to be called init_prob
    def get_sense_prob(self, target, sense):
        sense_count = self.wsd[target].get_sense_count(sense)
        word_count = self.wsd[target].total_count
        if word_count == 0:
            print("ERROR: No words in the dictionary")
        return float(sense_count) / float(word_count)

    #Returns the probability of the context given the sense. Used to be in sense_prob.
    def get_features_prob(self, target, sense, context):
        features = self.wsd[target].senses[sense]
        prob = 0.
        #get the feature count count(f_j, s)
        sense_count = self.wsd[target].get_sense_count(sense)
        for f in context:
            feature_count = features.get_feature_count(f)
            prob += math.log10(float(feature_count) / float(sense_count))
        return prob

    #Given a line, fill in the nested dictionary
    def train_line(self, target, context, senses):
        #Convert context to feature words
        features = nltk.tokenize.regexp_tokenize(context, r'\w+')
        #Perforning feature filtering based on part of speech tag. 
        filtered_features = list()
        result = nltk.pos_tag(features)
        for i in range(len(result)):
            if str(result[i][1]) in allowed_pos:
                filtered_features.append(result[i][0])
        features = filtered_features
        #Performing Porter stemming on feature words
        ps = PorterStemmer()
        for i in range(len(features)):
            features[i] = ps.stem(features[i])
        #Lookup target in the dictionary
        if target not in self.wsd:
            self.wsd[target] = Word()
        #Call add_features(context) on the entry
        for s in senses:
            self.wsd[target].add_features(s, features)
            
    #Given a train file, fill in the nested dictionary
    def train(self, filename, importname=""):
        if importname != "":
            with open(importname, 'rb') as f:
                self.wsd = pickle.load(f)
                print("Loaded training file " + importname)
                return
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
                context = ""
                for component in features[1::2]:
                    context+=component
                # Handling of senselist
                senses = list()
                for i in range(3,len(senselist)):
                    if senselist[i] == "1":
                        senses.append(i-3)
                # Call the train line function to handle
                self.train_line(senselist[0], context, senses)
            print("Done training")
            with open('supervised_training.pickle', 'wb') as f: 
                pickle.dump(self.wsd, f)
                print("Done pickling")
        

    #Returns all senses that are good
    #Senses: List of 0s
    #@Return: Returns the senses list with 0s replaced by 1s
    def test_line(self, target, context, senses):
        ans_list = list()
        #Convert context to feature words
        features = nltk.tokenize.regexp_tokenize(context, r'\w+')
        #Perforning feature filtering based on part of speach tag. 
        filtered_features = list()
        result = nltk.pos_tag(features)
        for i in range(len(result)):
            if str(result[i][1]) in allowed_pos:
                filtered_features.append(result[i][0])
        features = filtered_features
        #Performing stemming on feature words
        ps = PorterStemmer()
        for i in range(len(features)):
            features[i] = ps.stem(features[i])
        #Compare features with sense data
        if target not in self.wsd:
            print("ERROR: " + target + " not in dictionary")
            return
        #Calculate sense probabilities for all senses
        max_score = 0.
        max_index = 0
        for s in range(len(senses)-1):
            score = self.get_prob(target, features, s)
            #print("Sense Num: " + str(s) + " Value: " + str(score))             #DEBUG: print statement for sense probabilities
            '''
            #New system: Pick only the best sense
            if score > max:
                max_index = s + 1
            ans_list.append(0)
            '''
            #Old system: Pick anything above a threshold     
            if score > thres:
                ans_list.append(1)
            else:
                ans_list.append(0)
        ans_list.insert(0, 0)                           #UNORTHODOX.
        return ans_list

    #Given a train file, fill in the nested dictionary
    def test(self, filename):
        outputfile = open("results.txt", 'w+')
        ones = 0
        data = open(filename, 'r')
        if (data == None):
            print("Error: Testing file not found")
        else:
            data = data.readlines()
            case = 0
            total_answers = 0
            mistakes = 0
            for line in data:
                #Convert text into partitions. #features[0]: word.pos t0 t1 ... tk
                #features[1]: prev-context, features[2]: head, features[3]: next-context
                features = line.lower().split("@")
                # Spliting of features[0] into components and combining of prev and next context into context
                senselist= re.findall('\w+', features[0])
                context = ""
                for component in features[1::2]:
                    context+=component
                # Handling of senselist
                senses = list()
                for i in range(2,len(senselist)):
                    senses.append(0)
                # Call the train line function to handle
                cor_answer = senselist[2:]
                results = self.test_line(senselist[0], context, senses)
                #print("Case " + str(case) + ": " + str(results) + " Correct Answer: " + str(cor_answer))     #DEBUG: print statement for final answer. 
                case+=1
                #Write output to file for Kaggle.
                output_write = ''
                for piece in results:
                    output_write += str(piece) + '\n'
                outputfile.write(output_write)
                #Generate statistics regarding results
                for j in range(len(results)):
                    if str(results[j]) != str(cor_answer[j]):
                        mistakes+=1
                    total_answers+=1
                    #if (results[j] == "1"):
                        #ones += 1
            #print("Ones guessed: " + ones)
            accuracy = float(total_answers-mistakes)/float(total_answers)
            print("Accuracy is: " + str(accuracy))
            return accuracy

    def print_dict(self):
        for w in self.wsd.keys():
            print("Word: " + w )
            print("# of senses: " + str(len(self.wsd[w].senses)))
            for s in self.wsd[w].senses:
                print(str(s) + ":\t" + str(self.wsd[w].senses[s].featureUnigram))

#autolog = open("autotestingresults.txt", 'w+')
#print("Smoothing factor: " + str(smoothing))
#print("Threshold: " + str(thres))

thres = .007
smoothing = .01

s = Supervised()
#Pickled Data Training
s.train("Training Data.data", "supervised_training.pickle")
#Nonpickled Data Training
#s.train("Training Data.data")
#Automated testing
#while (smoothing < 1):
#    autolog.write("Smoothing factor: " + str(smoothing) + '\n')
#while (thres < .035):
a = s.test("Test Data.data")
#autolog.write("Smoothing factor: " + str(smoothing) + " Threshold: " + str(thres) + " Accuracy: " + str(a) + '\n')
#print(("Smoothing factor: \t" + str(smoothing) + "\t Threshold: \t" + str(thres) + "\t Accuracy: \t" + str(a)))
    #thres+=.001


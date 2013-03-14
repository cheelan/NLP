from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re, nltk

allowed_pos = ["FW", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

class dictWSD:
    dictionary = None
    data = None
    cor_answer = None
    sum_maximum  = 0
    count_maximum = 0
    
    def __init__(self, file):       # take out file from parameters after taking out correct answer parsing
        print 'Initialize'
        self.dictionary = self.genXmlDictionary('Dictionary.xml')
        
        self.data = self.parse_data(file)
        
        #################### Finds the correct answer
        ### TAKE OUT ***
        
        ones = 0
        ans = open(file, 'r')
        self.cor_answer = list()
        if (ans == None):
            print("Error: Testing file not found")
        else:
            ans = ans.readlines()
            case = 0
            
            for line in ans:
                #Convert text into partitions. #features[0]: word.pos t0 t1 ... tk
                #features[1]: prev-context, features[2]: head, features[3]: next-context
                features = line.lower().split("@")
                # Spliting of features[0] into components and combining of prev and next context into context
                senselist= re.findall('\w+', features[0])
                # Handling of senselist
                senses = list()
                for i in range(2,len(senselist)):
                    senses.append(0)
                # Call the train line function to handle
                self.cor_answer.append(senselist[2:])
                #print("Case " + str(case) + ": " + str(results) + " Correct Answer: " + str(self.cor_answer))     #DEBUG: print statement for final answer. 
                case+=1
                
        print 'finished cor_answer'
        
        #########################
        
        
    def main(self, file, threshold):
        dictWSDResults = open("dictWSDResults.txt", 'w')

        ourans = list()
        
        total_answers = 0
        mistakes = 0
        
        allzeros = 1
            
        for (target, context) in self.data:
            #results = self.WSD(target, context)
            
            results = self.WSD(target, context, threshold)
            
            ###
            ourans.append(results)          ### TAKE OUT ***
            if 1 in results:
                allzeros = 0
            ###
            
            ######################### write to file
            '''
            for result in results:
                dictWSDResults.write(str(result) + '\n')
            '''
                
        print 'allzeros:'
        if allzeros==0:
            print 'has a 1'
        else:
            print 'has all zeros'
                
        
        
        ############################ Compares against correct answer
        ### TAKE OUT ***
        
        print 'finished ourans'
        #Generate statistics regarding results
        for j in range(len(ourans)):
            for a in range(len(ourans[j])):
                if str(ourans[j][a]) != str(self.cor_answer[j][a]):
                    mistakes+=1
                total_answers+=1
            #if (results[j] == "1"):
                #ones += 1
        #print("Ones guessed: " + ones)
        accuracy = float(total_answers-mistakes)/float(total_answers)
        print("Accuracy is: " + str(accuracy))
        
        #############################
        
        #############################
        ### TAKE OUT***
        
        print 'sum'
        print self.sum_maximum
        print 'average'
        print self.sum_maximum / float(self.count_maximum)

        #############################
        
        #print self.dictionary
        #self.dictionary = {}
        #self.dictionary['word1'] = ['A very fast candy bar', 'A very fast cat']
        #self.dictionary['word2'] = ['A very fast car file is very fast candy']
        #self.dictionary['word2'] = ['A very slow dog', 'A slow but very fat slow dog candy bar']
        #self.dictionary['fall'] = ['The season of sadness', 'The action of anti elevating', 'Hey Casey, what is up?']
        #self.dictionary['flying'] = ['The action of elevating above', 'Some kind of fishing', 'Being too cool for school']
        #self.dictionary['birds'] = ['Badminton stuff that goes above', 'Mammals that love the action of elevating above']
        
    #def WSD(self, target, context):             # executes WSD for the target word in a context
    def WSD(self, target, context, threshold):             # executes WSD for the target word in a context
        #features = self.context_filter(context.split(' '))
        features = self.POSfilter(context)
        
        test = None
        results = None
        
        for feature in features:
            temp = self.compareWords(target, feature)
            #print feature
            #print temp
            if test==None:
                test = temp
                results = temp     # take out
            else:
                for i in range(len(test)):
                    test[i] = test[i]+temp[i]
        
        print 'sum: '
        print test
        
        maxIndex = 0
        maxValue = 0
        
        #highest score only
        '''
        for s in range(len(test)):
            if test[s]>maxValue:
                maxIndex = s
                maxValue = test[s]
        for k in range(len(results)):
            if k!=maxIndex:
                results[k]=0
            else:
                results[k]=1
        '''
        
        # threshold checking
        '''for t in range(len(test)):
            if test[t]>50:
                blah[t] = 1
            else:
                blah[t] = 0'''
        #print 'final: '
        #print blah
        
        # uses a threshold
        '''
        for s in range(len(test)):
            if test[s]>threshold:
                results[s] = 1
                #results[s] = 0
            else:
                results[s] = 0
        '''
        
        # find max and then take a percentage as a threshold
        # hack: for now treat the threshold number as a percentage
        
        for s in range(len(test)):
            if test[s]>maxValue:
                maxValue = test[s]
        
        self.count_maximum += 1
        print self.count_maximum
        print maxValue
        self.sum_maximum += maxValue
        
        
        maxValue = maxValue * threshold / 100.0
        for k in range(len(results)):
            if test[k]>maxValue:
                results[k] = 1
            else:
                results[k] = 0
                
        ##############
        
        ###TAKE THIS OUT
        #results = test
        ###
        return results
                
    def compareWords(self, target, feature):    # compares the target word to a context feature
        scores = [0]
        runningScore = 0
        targetSenses = self.dictionary[target]
        #featureSenses = self.dictionary[feature]            # add checks to see if it exists
        featureSenses = self.define_word(self.dictionary, feature)
        
        #ps = PorterStemmer()
        
        for tSense in targetSenses:
            runningScore = 0
            
            ### pos filter of target sense
            '''
            tFiltered = self.POSfilterToString(tSense)
            for fSenses in featureSenses:
                runningScore += self.getScore(tFiltered, fSenses)     # add normalization here
            '''
            ### porter stemmer
            '''
            tStemmed = ps.stem(tSense)
            for fSenses in featureSenses:
                runningScore += self.getScore(tStemmed, fSenses)     # add normalization here
            '''
            ###
            
            ### original
            
            for fSenses in featureSenses:
                runningScore += self.getScore(tSense, fSenses)     # add normalization here
            
            ###
            scores.append(runningScore)                     # will change this later to match with the parsed dictionary
        
        return scores
        
    def getScore(self, targetdef,featuredef):   # computes overlap of one target sense and one context feature sense
        #assume that each input is a string
        featureNextWord= "";
        targetNextWord= "";
        fWordList = featuredef.lower().split(" ")
        
        #tWordList = targetdef.lower().split(" ")
        tWordList = self.POSfilter(targetdef)
        
        fWordCounter=0;
        score=0;
        tWordCounter=0;
        retain=0;
        checkWordsCount=0;
        while (tWordCounter < len(tWordList)):
            while (fWordCounter < len(fWordList)):
                if tWordList[tWordCounter] == fWordList[fWordCounter]:
                    featureNextWord= fWordList[fWordCounter];
                    targetNextWord= tWordList[tWordCounter];
                    while(targetNextWord == featureNextWord):
                        checkWordsCount =checkWordsCount + 1;
                        fWordCounter = fWordCounter + 1
                        tWordCounter = tWordCounter + 1
                        if (fWordCounter>=len(fWordList) or tWordCounter>=len(tWordList)):
                            break
                        featureNextWord= fWordList[fWordCounter];
                        targetNextWord = tWordList[tWordCounter];
                    score = score + (((2.0)*checkWordsCount)/len(fWordList));
                    #score = score + (((2.0)**checkWordsCount)/len(fWordList));
                    #score = score + ((2.0)**checkWordsCount);
                    #score = score + ((2.0)*checkWordsCount);
                    checkWordsCount=0;
                else:
                    fWordCounter = fWordCounter + 1;
                tWordCounter= retain;
            fWordCounter=0;
            retain =retain +1;
            tWordCounter= retain;
        #return score
        return score/len(tWordList)
        
    #Returns a list of the definitions of all senses/synonyms of a word
    def define_word(self, d, word):
        try:
            xmldef = self.xml_definition(d,word)
            if len(xmldef) > 0:
                return xmldef
        except:
            synsets = wordnet.synsets(word)
            definitions = list()
            for s in synsets:
                definitions.append(s.definition)
            return definitions

    def genXmlDictionary(self, file):
        xml = open(file).read()
        dictionary = {}

        item_re = re.compile('item="([^"]*)"')
        #synset_re = re.compile('synset="([^"]*)"')
        gloss_re = re.compile('gloss="([^"]*)"')

        entries = xml.split("lexelt")
        for i in range(1, len(entries), 2):
            item = item_re.findall(entries[i])
            item = (item[0].split("."))[0]
            definitions = gloss_re.findall(entries[i])
            #syns = synset_re.findall(entries[i])
            #dictionary[item] = (definitions, syns)
            dictionary[item] = definitions
        return dictionary

    #Returns the definitions of a word in the XML dictionary, or [] or something if it isn't defined
    def xml_definition(self, d, word):
        return d[word]

    # Joe's code
    '''
    def parse_data(self, file):
        f = open(file)
        lines = f.readlines()
        parsed = list()
        
        for l in lines:
            space_split = l.split(' ')
            target = space_split[0][:-2]
            at_split = l.split('@')
            context = at_split[1:]
            temp = ""
            for c in context:
                temp += c
            parsed.append((target, temp))
        return parsed
    '''
    
    # Alex's code
    def parse_data(self, file):
        f = open(file)
        data = f.readlines()
        parsed = list()
        
        for line in data:
            #Convert text into partitions. #features[0]: word.pos t0 t1 ... tk
            #features[1]: prev-context, features[2]: head, features[3]: next-context
            features = line.lower().split("@")
            # Spliting of features[0] into components and combining of prev and next context into context
            senselist= re.findall('\w+', features[0])
            context = ""
            for component in features[1::2]:
                context+=component
            parsed.append((senselist[0], context))
            
        return parsed
        
    # code from Alex
    def POSfilter(self, line):
        #Convert context to feature words
        features = nltk.tokenize.regexp_tokenize(line, r'\w+')
        #Perforning feature filtering based on part of speech tag.
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
        return features
        
    def POSfilterToString(self, line):
        #print 'pos filter to string'
        output = ''
        #Convert context to feature words
        features = nltk.tokenize.regexp_tokenize(line, r'\w+')
        #Perforning feature filtering based on part of speech tag.
        filtered_features = list()
        result = nltk.pos_tag(features)
        for i in range(len(result)):
            if str(result[i][1]) in allowed_pos:
                filtered_features.append(result[i][0])
        features = filtered_features
        #Performing stemming on feature words
        ps = PorterStemmer()
        for i in range(len(features)):
            output += ps.stem(features[i]) + ' '
        return output
    
    # written by Casey
    def context_filter(self, context):
        unwanted_pos=['CC','IN','DT']
        filtered_features = list()
        result = nltk.pos_tag(context)
        for i in range(len(result)):
            if str(result[i][1]) not in unwanted_pos:
                filtered_features.append(result[i][0])
        features = filtered_features
        return features

#parse_training('debug_training.data')        
#d = dictWSD('Test Data.data')

# KAGGLE
'''
d = dictWSD('Test Data.data')
d.main('Test Data.data', 90)
'''

# validation
'''
d = dictWSD('validation_test.data')
d.main('validation_test.data', 0)
'''

# traverse through different thresholds
d = dictWSD('validation_test.data')
for i in range(90,91):
    print 'range'
    print i
    d.main('validation_test.data', i)
    
    
#d.main('validation_test.data', 0)

'''lemma = WordNetLemmatizer()
input_str = ""
for word in 'is a dog':
    input_str += lemma.lemmatize(word)
d.WSD(lemma.lemmatize('activate'), input_str)'''

#d.WSD('activate', 'is a dog')       output = each list is a list of scores for each sense in the target overlapping with one feature
#print d.compareWords('a b c d e', 'b b c a f')
#print d.compareWords('A very fast candy bar', 'A very fast car file is very fast candy')

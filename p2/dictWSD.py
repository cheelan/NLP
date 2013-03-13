from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import re

class dictWSD:
    dictionary = None
    
    def __init__(self, file):
        print 'Initialize'
        self.dictionary = self.genXmlDictionary('Dictionary.xml')
        dictWSDResults = open("dictWSDResults.txt", 'w')
        data = self.parse_data(file)
        
        for (target, context) in data:
            results = self.WSD(target, context)
            for result in results:
                dictWSDResults.write(str(result) + '\n')
        
        
        #print self.dictionary
        #self.dictionary = {}
        #self.dictionary['word1'] = ['A very fast candy bar', 'A very fast cat']
        #self.dictionary['word2'] = ['A very fast car file is very fast candy']
        #self.dictionary['word2'] = ['A very slow dog', 'A slow but very fat slow dog candy bar']
        #self.dictionary['fall'] = ['The season of sadness', 'The action of anti elevating', 'Hey Casey, what is up?']
        #self.dictionary['flying'] = ['The action of elevating above', 'Some kind of fishing', 'Being too cool for school']
        #self.dictionary['birds'] = ['Badminton stuff that goes above', 'Mammals that love the action of elevating above']
        
    def WSD(self, target, context):             # executes WSD for the target word in a context
        features = context.split(' ')
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
        #print 'sum: '
        #print test
        
        maxIndex = 0
        maxValue = 0
        
        for s in range(len(test)):
            if test[s]>maxValue:
                maxIndex = s
                maxValue = test[s]
        for k in range(len(results)):
            if k!=maxIndex:
                results[k]=0
            else:
                results[k]=1
        
        # threshold checking
        '''for t in range(len(test)):
            if test[t]>50:
                blah[t] = 1
            else:
                blah[t] = 0'''
        #print 'final: '
        #print blah
        
        return results
                
    def compareWords(self, target, feature):    # compares the target word to a context feature
        scores = [0]
        runningScore = 0
        targetSenses = self.dictionary[target]
        #featureSenses = self.dictionary[feature]            # add checks to see if it exists
        featureSenses = self.define_word(self.dictionary, feature)
        
        for tSenses in targetSenses:
            runningScore = 0
            for fSenses in featureSenses:
                runningScore += self.getScore(tSenses, fSenses)     # add normalization here
            scores.append(runningScore)                     # will change this later to match with the parsed dictionary
        
        return scores
        
    def getScore(self, targetdef,featuredef):   # computes overlap of one target sense and one context feature sense
        #assume that each input is a string
        featureNextWord= "";
        targetNextWord= "";
        fWordList = featuredef.lower().split(" ")
        tWordList = targetdef.lower().split(" ")
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
                    score = score+ (2)**checkWordsCount;
                    checkWordsCount=0;
                else:
                    fWordCounter = fWordCounter + 1;
                tWordCounter= retain;
            fWordCounter=0;
            retain =retain +1;
            tWordCounter= retain;
        return score
        
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
        
    def POSfilter(self, line):
        #Convert context to feature words
        features = nltk.tokenize.regexp_tokenize(context, r'\w+')
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

#parse_training('debug_training.data')        
d = dictWSD('Test Data.data')

'''lemma = WordNetLemmatizer()
input_str = ""
for word in 'is a dog':
    input_str += lemma.lemmatize(word)
d.WSD(lemma.lemmatize('activate'), input_str)'''

#d.WSD('activate', 'is a dog')       output = each list is a list of scores for each sense in the target overlapping with one feature
#print d.compareWords('a b c d e', 'b b c a f')
#print d.compareWords('A very fast candy bar', 'A very fast car file is very fast candy')

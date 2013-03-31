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
    
    # initializes the dictionary and parses the test file
    def __init__(self, file):
        self.dictionary = self.genXmlDictionary('Dictionary.xml')
        
        self.data = self.parse_data(file)
        
        # Finds the correct answer - VALIDATION
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
                case+=1
    
    # main method that calls the WSD algorithm and then prints accuracy (applicable if answers are given,
    # if not then the accuracy should be ignored by the user)
    def main(self):
        dictWSDResults = open("dictWSDResults.txt", 'w')
        ourans = list()
        total_answers = 0
        mistakes = 0
        allzeros = 1
            
        for (target, context) in self.data:
            results = self.WSD(target, context)
            ourans.append(results)
            
            for result in results:
                dictWSDResults.write(str(result) + '\n')    # write 0/1 to file

        # Compares against correct answer
        #Generate statistics regarding results
        for j in range(len(ourans)):
            for a in range(len(ourans[j])):
                if str(ourans[j][a]) != str(self.cor_answer[j][a]):
                    mistakes+=1
                total_answers+=1
        accuracy = float(total_answers-mistakes)/float(total_answers)
        print("Accuracy is: " + str(accuracy))

    # executes WSD algorithm for the target word in a context
    def WSD(self, target, context):             
        features = self.POSfilter(context)
        test = None
        results = None

        for feature in features:
            temp = self.compareWords(target, feature)
            if test==None:
                test = temp
                results = temp
            else:
                for i in range(len(test)):
                    test[i] = test[i]+temp[i]
            
        maxIndex = 0
        maxValue = 0
        
        # find the highest score only
        for s in range(len(test)):
            if test[s]>maxValue:
                maxIndex = s
                maxValue = test[s]
        for k in range(len(results)):
            if k!=maxIndex:
                results[k]=0
            else:
                results[k]=1
                
        return results
        
    # compares the target word to a context feature
    def compareWords(self, target, feature):
        scores = [0]
        runningScore = 0
        targetSenses = self.dictionary[target]
        featureSenses = self.define_word(self.dictionary, feature)
        
        for f in range(len(featureSenses)):
            featureSenses[f] = self.stemmer(nltk.tokenize.regexp_tokenize(featureSenses[f], r'\w+'))
        
        for tSense in targetSenses:
            runningScore = 0
            
            stemmedTSense= self.stemmer(nltk.tokenize.regexp_tokenize(tSense.lower(), r'\w+'))
            for fSenses in featureSenses:
                runningScore += self.getScore(stemmedTSense, fSenses)
            scores.append(runningScore)
        
        return scores
        
    # computes overlap of one target sense and one context feature sense
    def getScore(self, parsedtargetdef,fWordList):
        featureNextWord= ""
        targetNextWord= ""

        fWordCounter=0
        score=0
        tWordCounter=0
        retain=0
        checkWordsCount=0
        
        while (tWordCounter < len(parsedtargetdef)):
            while (fWordCounter < len(fWordList)):
                if parsedtargetdef[tWordCounter] == fWordList[fWordCounter]:
                    featureNextWord= fWordList[fWordCounter]
                    targetNextWord= parsedtargetdef[tWordCounter]
                    while(targetNextWord == featureNextWord):
                        checkWordsCount =checkWordsCount + 1
                        fWordCounter = fWordCounter + 1
                        tWordCounter = tWordCounter + 1
                        if (fWordCounter>=len(fWordList) or tWordCounter>=len(parsedtargetdef)):
                            break
                        featureNextWord= fWordList[fWordCounter]
                        targetNextWord = parsedtargetdef[tWordCounter]
                    score = score + (((2.0)*checkWordsCount)/len(fWordList))
                    checkWordsCount=0
                else:
                    fWordCounter = fWordCounter + 1
                tWordCounter= retain
            fWordCounter=0
            retain =retain +1
            tWordCounter= retain
        return score/len(parsedtargetdef)
        
    # Returns a list of the definitions of all senses/synonyms of a word
    def define_word(self, d, word):
        synsets = wordnet.synsets(word)
        definitions = list()
        for s in synsets:
            definitions.append(s.definition)
        return definitions

    # Parses the provided XML dictionary
    def genXmlDictionary(self, file):
        xml = open(file).read()
        dictionary = {}

        item_re = re.compile('item="([^"]*)"')
        gloss_re = re.compile('gloss="([^"]*)"')

        entries = xml.split("lexelt")
        for i in range(1, len(entries), 2):
            item = item_re.findall(entries[i])
            item = (item[0].split("."))[0]
            definitions = gloss_re.findall(entries[i])
            dictionary[item] = definitions
        return dictionary
    
    # returns target words and their corresponding contexts
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
        
    # filters out certain parts of speech and also stems the remaining words
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
        return self.stemmer(features)

    #Perform stemming on feature words
    def stemmer(self, features):
        ps = PorterStemmer()
        for i in range(len(features)):
            features[i] = ps.stem(features[i])
        return features


# KAGGLE

d = dictWSD('Test Data.data')
d.main()

### end KAGGLE

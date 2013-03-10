class dictWSD:
    dictionary = None
    
    def __init__(self):
        print 'Initialize'
        self.dictionary = {}
        #self.dictionary['word1'] = ['A very fast candy bar', 'A very fast cat']
        #self.dictionary['word2'] = ['A very fast car file is very fast candy']
        #self.dictionary['word2'] = ['A very slow dog', 'A slow but very fat slow dog candy bar']
        self.dictionary['fall'] = ['The season of sadness', 'The action of anti elevating']
        self.dictionary['flying'] = ['The action of elevating above', 'Some kind of fishing', 'Being too cool for school']
        self.dictionary['birds'] = ['Badminton stuff that goes above', 'Mammals that love the action of elevating above']
        
        
    def WSD(self, target, context):             # executes WSD for the target word in a context
        features = context.split(' ')
        test = None
        
        for feature in features:
            temp = self.compareWords(target, feature)
            print temp
            if test==None:
                test = temp
            else:
                for i in range(len(test)):
                    test[i] = test[i]+temp[i]
        print test
        
    def compareWords(self, target, feature):    # compares the target word to a context feature
        scores = [0]
        runningScore = 0
        targetSenses = self.dictionary[target]
        featureSenses = self.dictionary[feature]            # add checks to see if it exists
        
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
        
d = dictWSD()
d.WSD('fall', 'flying birds')
#print d.compareWords('a b c d e', 'b b c a f')
#print d.compareWords('A very fast candy bar', 'A very fast car file is very fast candy')
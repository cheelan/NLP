import sys, itertools, copy, random, nltk.tokenize

sentence = '''<S>You will rejoice to hear that no disaster has accompanied the
commencement of an enterprise which you have regarded with such evil
forebodings.</S><S>  I arrived here yesterday, and my first task is to assure
my dear sister of my welfare and increasing confidence in the success
of my undertaking.</S>'''

class Gram:
    n = 0
    dictionary = None
    unique_words = 0
    total_grams = 0
    count_list = [0]
    smoothing_bound = 0

    #n: number of grams (1 = unigram, 2 = bigram, etc.)
    #text: a text corpus to model
    #smoothingBound: smooth all words that appear less than the smoothingBound
    #Returns a dictionary with keys that strings representing lists of words, and values that are counts
    #TO-DO: Punctuation (find and replace should do the trick)
    def __init__(self, n, text, smoothing_bound ):
        self.n = n
        self.dictionary = {}
        self.count_list*=(smoothing_bound+1)
        unique_ngrams = 0

        previous = list()   # Sentences are NOT independent of one another. 
        word_generator = self.text_parse(text)
        for word in word_generator:
            #Maintain queue of n most recent words
            previous.append(word)
            if len(previous) < n:
                continue
            while len(previous) > n:
                previous.pop(0)
            # Updating the occurence counts
            temp = copy.deepcopy(previous)
            nthWord = temp.pop()
            nMinusOneKey = str(temp)
            if nMinusOneKey in self.dictionary:
                miniDict = self.dictionary[nMinusOneKey] #Copy or pointer?
                if nthWord in miniDict:
                    miniDict[nthWord]+= 1
                else:
                    miniDict[nthWord] = 1
                    self.unique_words+=1
                    unique_ngrams+=1
            else:
                ngrams[nMinusOneKey] = {nthWord : 1}
                unique_ngrams+=1
            # Keeping track of counts in the countList
            if (smoothingBound > 0):
                count = ngrams[nMinusOneKey][nthWord]
                if count > 1:
                    self.count_list[count-1] -= 1
                if count <= smoothingBound:
                    self.count_list[count] += 1
        self.count_list[0] = self.unique_words**n - unique_ngrams
        self.applySmoothing()

    #Applies Good-Turing smoothing to all ngrams in dict that appear less than bound times
    #We might have to iterate over the whole dictionary. Yuck.
    #Optimization could be to iterate before we fill with zeros - the dict will be much smaller
    def applySmoothing(self):
        for k in self.dictionary.keys():
            for k2 in self.dictionary[k].keys():
                count = self.dictionary[k][k2]
                if count < self.smoothingBound:
                    self.dictionary[k][k2] = (count + 1) * (float(self.count_list[count+1]) / float(self.count_list[count]))

    '''
    def print_out(self):
        sorted_dictionary = sorted(self.dictionary.iteritems(), key= operator.itemgetter(1), reverse = True)
        print(sorted_dictionary[:100])

    def add(self, word):
        if word in self.dictionary:
            self.dictionary[word]+=1
        else:
            self.word_count+=1
            self.dictionary[word] = 1
    '''
'''
    #text: regular text
    #model: the n-gram model of choice
    #n: the n in n-gram
    #output: a score proportional to the probability of the sentence coming from that model
    #Handling unknowns... hmmm
    def getPerplexity(text):
        p = 1.0
        lst = list()
        word_generator = parse_text(text)
        for word in word_generator:
            #Maintain queue of n most recent words
            lst.append(word) 
            if len(lst) < n:
                continue
            while len(lst) > n:
                lst.pop(0)
            nMinusOne = str(lst.pop())
            key = str(lst)
            #Need to adjust these for unknown words
            if self.smoothing_bound > 0:
                zero_count = float(self.count_list[1]) / float(self.count_list[0])
            else:
                zero_count = 0

            
            numerator = 0.
            denominator = 0.

            if not (key in model):
                numerator = zero_count
                denominator = 
            elif key in model and (not (nMinusOne in model[key])):

            elif key in model and nMinusOne in model[key]:
             

           

            if not (key in model) or (not (nMinusOne in model[key])):
                numerator = zero_count
            else:
                numerator = (float(model[key][nMinusOne]))

            i = 0
            summation = 0.
            for v in model[key].values():
                i += 1
                summation += v
            #TO-DO Let's double check that..
            summation += float(totalCount - i) * (float(countList[1]) / float(countList[0])) 
            p *= 1. / numerator / summation)

        return p**(1. / float(len(sent)))
'''
        
        
def fillZeros(vocab, n):
    for perm in itertools.product(vocab.keys(), repeat=n):
        key = list()
        for p in perm[0:(n-1)]:
            key.append(p)
        last = str(perm[n-1])
        key = str(key)
        
        #key = key.replace("(", "[")
        #key = key.replace(")", "]")
        #Do this better. Data with parentheses will break ^
        if not (key in ngrams): 
            ngrams[key] = {last : 0};
        else:
            if not (last in ngrams[key]):
                (ngrams[key])[last] = 0 

#Utility functions for our special nested dictionary
def updateCount(dict, ngram, newCount):
    #Convert the string input to a list
    l = [ngram.strip(" '") for ngram in ngram.strip('[]').split(',')]
    #the last word
    word = l.pop() 
    key = str(l)
    if key in dict and word in dict[key]:
        dict[key][word] = newCount
        return
    print("WARNING: " + ngram + " is not in the current model, so it can't be updated")

def getCount(dict, ngram):
    #Convert the string input to a list
    l = [ngram.strip(" '") for ngram in ngram.strip('[]').split(',')]
    #the last word
    word = l.pop() 
    key = str(l)
    if key in dict and word in dict[key]:
        return dict[key][word]
    return 0

#Currently not used
def gtSmooth(ngram, smoothingBound):
    count = 0
    if ngram in ngrams:
        count = ngrams[ngram]
    if count >= smoothingBound:
        return count
    return (count + 1) * (countList[count+1] / countList[count])

def randomSentence():
    prev = "['startsen']"
    sentence = ""
    #Import bigram table if it exists
    #Otherwise generate one
    while True:
        sum = float(0)
        rand = random.random()
        if prev in ngrams:
            i = 0
            for v in ngrams[prev].values():
                i += 1
                sum += v
            #sum += float(totalCount - i) * p
                #TO-DO: Need to add in (total number of ngrams possible - ngrams seen) * prob(0 occurrences)
            print("COUNT: " + str(sum))
            runningSum = float(0)
            for (k,v) in ngrams[prev].iteritems():
                runningSum += v / sum
                if (runningSum >= rand):
                    if k == "startsen":
                        break
                    if k == "endsen":
                        return sentence
                    sentence += " " + k
                    prev = "['" + k + "']"
                    break
            #TO-DO: If this part is reached, then pick a random gram that appears 0 times
        else:
            print("Error: " + prev + " not in ngram model")
            break



#ngram(int(sys.argv[1]), sentence)

test = Gram(2, sentence, 3)
#print("Count 0: "+ str(getCount(ngrams, "['ate', 'apple']")))
#print("Random sentence: " + randomSentence())
#print("Score of a sentence: " + str(getSentencePerplexity("You will rejoice to hear that no disaster has accompanied", ngrams, 2)))
#print(ngrams["[',']"])
#print(str(ngrams))

#nltkTest()

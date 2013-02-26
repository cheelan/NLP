import sys, itertools, copy, random, nltk.tokenize, os, re, math

'''
sentence = """You will rejoice to hear that no disaster has accompanied the
commencement of an enterprise which you have regarded with such evil
forebodings. I arrived here yesterday, and my first task is to assure
my dear sister of my welfare and increasing confidence in the success
of my undertaking."""
'''
sentence = "I went to the bank. The bank had a lot of people. The people had a lot of money. The people went to the cars."


class Gram:
    n = 0
    dictionary = None
    unique_words = 0
    total_grams = 0
    count_list = [0]
    smoothing_bound = 0
    vocab = set()

    #n: number of grams (1 = unigram, 2 = bigram, etc.)
    #text: a text corpus to model
    #smoothingBound: smooth all words that appear less than the smoothingBound
    #Returns a dictionary with keys that strings representing lists of words, and values that are counts
    #TO-DO: Punctuation (find and replace should do the trick)
    def __init__(self, n, text, smoothingBound ):
        self.n = n
        self.dictionary = {}
        self.smoothing_bound = smoothingBound
        self.count_list= [0]*(self.smoothing_bound + 1)
        unique_ngrams = 0
        self.vocab = set()
        previous = list()   # Sentences are NOT independent of one another. 
        word_generator = self.text_parse(text)
        for word in word_generator:
            self.vocab.add(word)
            #Maintain queue of n most recent words
            previous.append(word)
            if len(previous) < n:
                continue
            self.total_grams += 1
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
                    unique_ngrams+=1
            else:
                self.dictionary[nMinusOneKey] = {nthWord : 1}
                self.unique_words+=1
                unique_ngrams+=1
            # Keeping track of counts in the countList
            if (self.smoothing_bound > 0):
                count = self.dictionary[nMinusOneKey][nthWord]
                if count > 1 and count <= (self.smoothing_bound+1):
                    self.count_list[count-1] -= 1
                if count <= self.smoothing_bound:
                    self.count_list[count] += 1

        self.unique_words = len(self.vocab)
        self.count_list[0] = self.unique_words**n - unique_ngrams
        print("UNique_words: " + str(self.unique_words))
        print("UNique_grams: " + str(unique_ngrams))
        if (self.smoothing_bound > 0):
            self.apply_smoothing()

    #Applies Good-Turing smoothing to all ngrams in dict that appear less than bound times
    #We might have to iterate over the whole dictionary. Yuck.
    #Optimization could be to iterate before we fill with zeros - the dict will be much smaller
    def apply_smoothing(self):
        for k in self.dictionary.keys():
            for k2 in self.dictionary[k].keys():
                count = self.dictionary[k][k2]
                if count < self.smoothing_bound:
                    self.dictionary[k][k2] = (count + 1) * (float(self.count_list[count+1]) / float(self.count_list[count]))

    # Parses the text by removing the HTML tags and creates a generator of the words in the text.
    def text_parse(self, text):
        if text == None:
            text = ''
            for fname in os.listdir(os.getcwd()):
                if fname.endswith(".train"):
                    inputFile = open(fname,'r')
                    text+=inputFile.read()
                    inputFile.close()
            text = re.compile(r'<.*?>').sub('',text)
        for sentence in nltk.tokenize.sent_tokenize(text):
            for word in (['<S>'] + nltk.tokenize.word_tokenize(sentence) + ['</S>']):
                yield(word.lower())

    #text: regular text
    #model: the n-gram model of choice
    #n: the n in n-gram
    #output: a score proportional to the probability of the sentence coming from that model
    #Handling unknowns... hmmm
    def getPerplexity(self, text):
        p = 1.0
        lst = list()
        word_generator = self.text_parse(text)
        length = 0
        try:
            for word in word_generator:
                length += 1
                #Maintain queue of n most recent words
                lst.append(word) 
                if len(lst) < self.n:
                    continue
                while len(lst) > self.n:
                    lst.pop(0)
                temp = copy.deepcopy(lst)
                nMinusOne = str(temp.pop())
                key = str(temp)
                #Need to adjust these for unknown words
                if self.smoothing_bound > 0:
                    zero_count = float(self.count_list[1]) / float(self.count_list[0])
                else:
                    zero_count = 0
                numerator = 0.
                denominator = 0.

                if not (key in self.dictionary):
                    numerator = zero_count
                    denominator = self.total_grams + (zero_count * self.count_list[0])
                elif key in self.dictionary and (not (nMinusOne in self.dictionary[key])):
                    numerator = zero_count
                    i = 0
                    for v in self.dictionary[key].values():
                        i += 1
                        denominator += v
                    denominator += float(self.unique_words - i) * zero_count
                elif key in self.dictionary and nMinusOne in self.dictionary[key]:
                    i = 0
                    numerator = self.dictionary[key][nMinusOne]
                    for v in self.dictionary[key].values():
                        i += 1
                        denominator += v
                    denominator += float(self.unique_words - i) * zero_count
                else:
                    print("Hit a spot where it should never go.")
                p += math.log10(denominator / numerator)
            return 10**(p * (1. / float(length)))   
        except:
            #print("Infinity")
            return 0

    def randomSentence(self):
        prev = "['<s>']"
        sentence = ""
        if self.smoothing_bound > 0:
            zero_count = float(self.count_list[1]) / float(self.count_list[0])
        else:
            zero_count = 0
        if self.n == 1:
            while True:
                rand = random.random()
                runningSum = 0.
                for (k,v) in self.dictionary['[]'].iteritems():
                    runningSum += float(v) / (self.total_grams)
                    if (runningSum >= rand):
                        if k == "<s>":
                            break
                        if k == "</s>":
                            return sentence
                        sentence += " " + k
                        break
        elif self.n > 2:
            print("ERROR: Random sentences does not work on n grams where n > 2")
            return ""
        #Import bigram table if it exists
        #Otherwise generate one
        while True:
            sum = float(0)
            rand = random.random()
            if prev in self.dictionary:
                i = 0
                for v in self.dictionary[prev].values():
                    i += 1
                    sum += v
                sum += float(self.unique_words - i) * zero_count
                    #sum += float(totalCount - i) * p
                    #TO-DO: Need to add in (total number of ngrams possible - ngrams seen) * prob(0 occurrences)
            
                runningSum = float(0)
                for (k,v) in self.dictionary[prev].iteritems():
                    runningSum += v / sum
                    if (runningSum >= rand):
                        if k == "<s>":
                            break
                        if k == "</s>":
                            return sentence
                        sentence += " " + k
                        prev = "['" + k + "']"
                        break
                copySet = copy.deepcopy(self.vocab)
                copySet = list(copySet)
                while True:
                    setRand = int(random.random() * len(copySet))         
                    randEl = copySet.pop(setRand)
                    if randEl in self.dictionary[prev]:
                        continue
                    sentence += " " + randEl
                    break
            else:
                return "Error: " + prev + " not in ngram model"

'''      
def authorTrainPreprocess(smoothingBound, unknown, bigrams):
    bestAuthor = ""
    bestScore = float('inf')
    for (a, b) in bigrams:
        perp = b.getPerplexity(unknown)
        if perp < bestScore:
            bestAuthor = a
            bestScore = perp
    return bestAuthor

def authorPredictionValidation(smoothingBound):
     #load the train file
    authorDictionary = dict()
    with open("train.txt") as f:
        content = f.readlines()
    for line in content:
        m = re.match(r"^\S+", line)
        author = m.group(0)
        rest = (re.compile(r'^\S+').sub('',line)).strip()
        if author in authorDictionary:
            authorDictionary[author] += " " + rest
        else:
            authorDictionary[author] = rest

    bigrams = list()
    for (k, v) in authorDictionary.iteritems():
        b = Gram(2, v, smoothingBound)
        bigrams.append((k, b))

     #load the validation file
    validationList = list()
    with open("validation.txt") as f:
        content = f.readlines()
    for line in content:
        m = re.match(r"^\S+", line)
        author = m.group(0)
        rest = (re.compile(r'^\S+').sub('',line)).strip()
        validationList.append((author, rest))
    right = 0
    wrong = 0
    for (ans, unknown) in validationList:
        if ans == authorTrainPreprocess(3, unknown, bigrams):
            right += 1
        else:
            wrong += 1
    print("Right: " + str(right))
    print("Wrong: " + str(wrong))
    print("Accuracy: " + str(float(right) / (right + wrong)))

def authorPrediction():
    pass

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
'''





#ngram(int(sys.argv[1]), sentence)

#test = Gram(1, sentence, 0)
#print(test.dictionary)
#test = Gram(2, "NONE", 3)
#print(test.dictionary)
#print(test.count_list)
#print("Count 0: "+ str(getCount(ngrams, "['ate', 'apple']")))
#print("Random sentence: " + test.randomSentence())
#print("Score of a sentence: " + str(test.getPerplexity("You will rejoice to hear that no disaster has accompanied")))
#print(str(authorPredictionValidation(3)))
#print("Score of a sentence: " + str(test.getPerplexity("the bank cars firetruck.")))
#print(ngrams["[',']"])
#print(str(ngrams))

#nltkTest()
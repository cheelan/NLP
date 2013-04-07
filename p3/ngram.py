import sys, itertools, copy, random, nltk.tokenize, os, re, math

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
        #word_generator = self.text_parse(text)
        for sentence in text:
            for word in sentence:
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
        print("Current Model Completed.")
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
    def getLogProb(self, text):
        p = 1.0
        lst = list()
        #word_generator = self.text_parse(text)
        length = 0
        try:
            for word in text:
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
                p += math.log(denominator / numerator)
            return p   
        except:
            #print("Infinity")
            return 0

    #Generates a random sentence based on the current gram model.
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
            else:
                return sentence

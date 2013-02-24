import os, pickle, anydbm, time, nltk.tokenize, operator, re

class Shell:
    unigram = None
    bigram = None
    ngram = None

    def __init__(self):
        print("For a list of commands, type \"help\"")
        self.unigram = Gram(1)
        self.bigram = Gram(2)

    def text_parse(self):
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

    def create_unigram(self, args):
        print("Parsing and creating the unigram model...")
        text = self.text_parse()
        sentences = nltk.tokenize.sent_tokenize(text)
        for i in sentences:
            self.unigram.add('<S>')
            for word in nltk.tokenize.word_tokenize(i):
                self.unigram.add(word.lower())
            self.unigram.add('</S>')
        self.unigram.print_out()

    def create_bigram(self, args):
        self.bigram = self.create_ngram(2)

    def create_ngram(self, args):
        # Find the n count to generate ngram model
        self.ngram = Gram(args[1])
        smoothingBound = int(args[2]) + 1
        countList = [0] * smoothingBound
        previous = list()

        print("Parsing and creating the ngram model...")
        text = self.text_parse()
        sentences = nltk.tokenize.sent_tokenize(text)
        for i in sentences:
            for word in ['<S>'] + nltk.tokenize.word_tokenize(i) + ['</S>']:
                self.unigram.add(word.lower())      #Double in the unigram. FIX IN FUTURE!!!!!!!!!!!!!!!!!
                #Mantain queue of n most recent words
                if len(previous) >= self.ngram.n:
                    previous.pop(0)
                #Look up n-1 words + current word in HT
                previous.append(word)
                if len(previous) < self.ngram.n:
                    continue
                copycat = copy.deepcopy(previous)
                n_word = copycat.pop()
                n_prev_word = str(copycat)
                if n_prev_word in self.ngram.dictionary:
                    miniDict = self.ngram.dictionary[n_prev_word]
                    if n_word in miniDict:
                        miniDict[n_word] = miniDict.pop(n_Word) + 1
                    else:
                        miniDict[n_word] = 1
                else:
                    self.ngram.dictionary[n_prev_word] = {n_word : 1}
                count = self.ngram.dictionary[n_prev_word][n_word]
                if count > 1:
                    



        vocab = dict() # This is the unigram model.
        for w in WordPunctTokenizer().tokenize(words):
  
            temp = copy.deepcopy(prev)
            nthWord = temp.pop()
            nMinusOneKey = str(temp)
            if nMinusOneKey in ngrams:

                miniDict = ngrams[nMinusOneKey] #Copy or pointer?
                if nthWord in miniDict:
                    miniDict[nthWord] = miniDict.pop(nthWord) + 1
                else:
                    miniDict[nthWord] = 1
            else:
                ngrams[nMinusOneKey] = {nthWord : 1}
            count = ngrams[nMinusOneKey][nthWord]
            if count > 1:
                countList[count-1] -= 1
            if count <= smoothingBound:
                countList[count] += 1
        countList[0] = totalCount**n - len(ngrams)
        #print("---")
        #print(countList)
        #print("---")
        fillZeros(vocab, n)
        #print(ngrams)
        applySmoothing(countList, smoothingBound)


    def import_data(self, args):
        data = anydbm.open('data.log', 'r')
        self.unigram = pickle.loads(data['unigram'])
        self.bigram = pickle.loads(data['bigram'])
        self.ngram = pickle.loads(data['ngram'])

    def export_data(self, args):
        data = anydbm.open('data.log', 'n')
        data['unigram'] = pickle.dumps(self.unigram)
        data['bigram'] = pickle.dumps(self.bigram)
        data['ngram'] = pickle.dumps(self.ngram)

    def help(self,args):
        print("The follow are valid commands:\nimport_data\nexport_data\nparse\ntest\nhelp\nexit")

    def generate_random(self,args):
        pass

    def exit(self, args):
        print("Exiting...")
        os._exit(0)


def shellmainloop():
    while True:
        try:
            commandline = raw_input(">>")
            commandline = commandline.strip()
        except EOFError:
            shell.exit(None)
        pieces = commandline.split(" ")
        try:
            func = getattr(shell, pieces[0].lower())
        except AttributeError:
            print "Does not compute. Please try again."
            continue
        func(pieces)

shell = Shell()
if __name__ == "__main__":
    shellmainloop()


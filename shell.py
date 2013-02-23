import os, pickle, anydbm, time, nltk.tokenize, operator, re

class Gram:
    dictionary = None
    n = 0

    def __init__(self, args):
        self.n = args
        self.dictionary = {}

    def print_out(self):
        sorted_dictionary = sorted(self.dictionary.iteritems(), key= operator.itemgetter(1), reverse = True)
        print(sorted_dictionary[:100])

    def add(self, word):
        if word in self.dictionary:
            self.dictionary[word]+=1
        else:
            self.dictionary[word] = 1

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
        return text

    def create_unigram(self, args):
        print(time.time())
        text = self.text_parse()
        print(time.time())
        sentences = nltk.tokenize.sent_tokenize(text)
        print(time.time())
        for i in sentences:
            self.unigram.add('<S>')
            for word in nltk.tokenize.word_tokenize(i):
                self.unigram.add(word.lower())
            self.unigram.add('</S>')
        self.unigram.print_out()
        print(time.time())

    def bigram(self, args):
        pass

    def ngram(self, args):
        pass

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

    def lookup(self,args):
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


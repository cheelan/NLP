import os, pickle, anydbm, time, nltk.tokenize

class Gram:
    dictionary = None
    n = 0

    def __init__(self, args):
        self.n = args
        self.dictionary = {}

    def print_out(self):
        print(self.dictionary)

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

    def initialize(self, args):
        self.unigram = Gram(1)
        self.bigram = Gram(2)
        self.ngram = Gram(3)
        self.unigram.add("unigram")
        self.bigram.add("bigram")
        self.ngram.add("trigram")
        self.unigram.print_out()
        self.bigram.print_out()
        self.ngram.print_out()

    def create_unigram(self, args):
        text = ''
        print(time.time())
        for fname in os.listdir(os.getcwd()):
            if fname.endswith(".train"):
                inputFile = open(fname,'r')
                text+=inputFile.read()
                inputFile.close()
        print(time.time())
        sentences = nltk.tokenize.sent_tokenize(text)
        print(time.time())
        for i in sentences[:5]:
            for word in nltk.tokenize.word_tokenize(i):
                self.unigram.add(word.lower())
        self.unigram.print_out()

    def bigram(self, args):
        pass

    def ngram(self, args):
        pass

    def test(self, args):
        pass

    def import_data(self, args):
        data = anydbm.open('data.log', 'c')
        self.unigram = pickle.loads(data['unigram'])
        self.unigram.print_out()
        self.bigram = pickle.loads(data['bigram'])
        self.bigram.print_out()
        self.ngram = pickle.loads(data['ngram'])
        self.ngram.print_out()

    def export_data(self, args):
        data = anydbm.open('data.log', 'c')
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


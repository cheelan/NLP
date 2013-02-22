import os, pickle, anydbm

class Gram:
    dictionary = {}
    n = 0

    def __init__(self, args):
        print(args)
        self.n = args

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

    def train(self, args):
        self.unigram = Gram(1)
        self.bigram = Gram(2)
        self.ngram = Gram(3)
        self.unigram.add("unigram")
        self.bigram.add("bigram")
        self.ngram.add("trigram")
        '''
        for train_file in args[2:]:
            self.nparse(train_file)
        '''

    def unigram(shell, args):
        text = ''
        for fname in os.listdir(os.getcwd()):
            if fname.endswith(".txt"):
                inputFile = open(fname,'r')
                # Parse each order line and write to the output file
                for line in inputFile:
                    text+=line
                inputFile.close()
        for w in sentence.split(" "):
            if w in unigrams:
                unigrams[w] = unigrams.pop(w) + 1
            else:
                unigrams[w] = 1

    def nparse(self,args):
        pass

    def test(self, args):
        pass

    def import_data(self, args):
        data = anydbm.open('data.log', 'c')
        print(pickle.loads(data['unigram']))
        self.unigram = pickle.loads(data['unigram'])
        self.unigram.print_out()
        print(pickle.loads(data['bigram']))
        self.bigram = pickle.loads(data['bigram'])
        self.bigram.print_out()
        print(pickle.loads(data['ngram']))
        self.ngram = pickle.loads(data['ngram'])
        self.ngram.print_out()

    def export_data(self, args):
        data = anydbm.open('data.log', 'c')
        data['unigram'] = pickle.dumps(self.unigram)
        print(data['unigram'])
        data['bigram'] = pickle.dumps(self.bigram)
        print(data['bigram'])
        data['ngram'] = pickle.dumps(self.ngram)
        print(data['ngram'])

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


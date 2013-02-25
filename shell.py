import os, pickle, anydbm, time, nltk.tokenize, operator, re
from ngram import *

class Shell:
    unigram = None
    bigram = None
    ngram = None

    def __init__(self):
        print("For a list of commands, type \"help\"")

    # Training of the various ngram models. 
    # Constructor: n, smoothing bound
    def train(self, args):
        self.unigram = Gram(1, None, int(args[2]))
        self.bigram = Gram(2, None, int(args[2]))
        self.ngram = Gram(int(args[1]), None, int(args[2]))

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

    def help(self, args):
        print("The follow are valid commands:\nimport_data\nexport_data\ntrain\nhelp\nexit")

    def generate_random(self, args):
        pass

    def guess(self, smoothingBound, unknown, bigrams):
        bestAuthor = ""
        bestScore = float('inf')
        for (a, b) in bigrams:
            perp = b.getPerplexity(unknown)
            if perp < bestScore:
                bestAuthor = a
                bestScore = perp
        return bestAuthor

    def author_prediction(self, args):
        smoothingBound = int(args[1])
        #load the train and parse it according to the author
        authorDictionary = dict()
        content = open("train.txt").readlines()
        for line in content:
            m = re.match(r"^\S+", line)
            author = m.group(0)
            email = (re.compile(r'^\S+').sub('',line)).strip()
            if author in authorDictionary:
                authorDictionary[author] += " " + email
            else:
                authorDictionary[author] = email
        bigrams = list()
        for (k, v) in authorDictionary.iteritems():
            b = Gram(2, v, smoothingBound)
            bigrams.append((k, b))

        #load the validation file
        validationList = list()
        content = open("validation.txt").readlines()
        for line in content:
            m = re.match(r"^\S+", line)
            author = m.group(0)
            email = (re.compile(r'^\S+').sub('',line)).strip()
            validationList.append((author, email))

        #Comparing our determination with the validation set.
        right = 0
        wrong = 0
        answer_file = open("answer_file.txt", 'w')
        for (ans, unknown) in validationList:
            prediction = self.guess(3, unknown, bigrams)
            answer_file.write(prediction + '\n')
            if ans == prediction:
                right += 1
            else:
                wrong += 1
        print("Right: " + str(right))
        print("Wrong: " + str(wrong))
        print("Accuracy: " + str(float(right) / (right + wrong)))

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


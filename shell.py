import os, pickle

class Gram:
    dictionary = {}
    n = 0

    def __init__(self, args):
        n = args



class Shell:
    bigram = None
    ngram = None

    def __init__(self):
        print("For a list of commands, type \"help\"")

    def train(self, args):
        ngram = Gram(args[1])
        for train_file in args[2:]:
            self.nparse(train_file)

    def nparse(self,args):
        pass

    def test(self, args):
        pass

    def import_data(self, args):
        self.bigram, self.ngram = pickle.load(open("data.log"))

    def export_data(self, args):
        pickle.dump(self.ngram, open("data.log",'wb'))

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


import os, pickle

class Shell:
    dictionary = {}

    def __init__(self):
        self.currentDirectory = os.getcwd()
        print("For a list of commands, type \"help\"")

    def train(self, args):
        for train_file in args:
            self.ngram(train_file)

    def ngram(self,args):
        pass

    def test(self, args):
        pass

    def import_data(self, args):
        self.dictionary = pickle.load(open("data.log"))

    def export_data(self, args):
        pickle.dump(self.dictionary, open("data.log",'wb'))

    def help(self,args):
        print("The follow are valid commands:\nimport_data\nexport_data\nparse\ntest\nhelp\nexit")

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


import ngram, subprocess
class SvmLiteWrapper:
    
    '''
    SVMLite calls:
    svm_learn example1/train.dat example1/model
    svm_learn [training file] [output file]

    svm_classify example1/test.dat example1/model example1/predictions
    svm_classify [test file] [training model] [output file]
    '''


    def __init__(self, n, deceptive_list_list, truthful_list_list):
        #Generate truthful and deceptive ngrams
        self.truthful_ngrams = []
        for review in truthful_list_list:
            self.truthful_ngrams.append(ngram.Gram(n, review, 0))

        self.deceptive_ngrams = []
        for review in deceptive_list_list:
            self.deceptive_ngrams.append(ngram.Gram(n, review, 0))
        
        #Map ngrams to their ids. If this is slow, use a hashing function instead
        self.id_map = self.gen_id_map()


    
    def gen_id_map(self):
        #Start count at 1. Count = 0 implies unknown ngram
        count = 1
        id_map = dict()
        for gram in self.deceptive_ngrams:
            for k in gram.dictionary.keys():
                if id_map.has_key(k):
                    continue
                else:
                    id_map[k] = count
                    count += 1
        for gram in self.truthful_ngrams:
            for k in gram.dictionary.keys():
                if id_map.has_key(k):
                    continue
                else:
                    id_map[k] = count
                    count += 1
        return id_map

    def get_id(self, gram):
        if self.id_map.has_key(gram):
            return self.id_map[gram]
        return 0

    def learn(self, model_location="svm_model.txt"):
        #This will generate a text file learning model in SVM format
        #Check to see if model already exists before re-generating it (bool param)
        self._gen_train_file(self.deceptive_ngrams, self.truthful_ngrams)
        #Then call svm_learn.exe
        args = ['svm_learn.exe', "ngram_svm.txt", model_location]
        subprocess.call(args)
        print("Done generating SVM")
        return


    #Writes a text file that will be used for the training model
    def _gen_train_file(self, deceptive_ngrams, truthful_ngrams):
        #This will generate the training txt file
        #For each truthful example
        #target = 1
        #Feature list is list of "getid(feature):count(feature)"
        file_lines = []
        for gram in deceptive_ngrams:
            line = "0"
            for (id, count) in self._features_from_ngram(gram):
                line += (" " + str(id) + ":" + str(count))
            file_lines.append(line)
        for gram in truthful_ngrams:
            line = "1"
            for (id, count) in self._features_from_ngram(gram):
                line += (" " + str(id) + ":" + str(count))
            file_lines.append(line)
        #print(file_lines)
        
        f = open("ngram_svm.txt",'w')
        for l in file_lines:
            f.write(str(l)+'\n')
        f.close()
        
    def _features_from_ngram(self, model):
        lst = []
        for k in model.dictionary.keys():
            id = self.get_id(k)
            count = model.get_count(k)
            lst.append((id,count))
        #Sort by ids
        lst.sort(_compare)
        return lst

    def classify(self, train_model_location="train_model.txt", test_model_location="test_model.txt"):
        #Generate a test model and call svm_classify using our learned model
        pass

    def _gen_test_model(self):
        pass

def _compare(x,y):
    if x[0] > y[0]:
        return 1
    elif x[0] < y[0]:
        return -1
    return 0


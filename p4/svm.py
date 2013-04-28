from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from ngram import Gram
from nltk.stem.porter import PorterStemmer

clf = None
ps = PorterStemmer()
unit_list = None

def train(filename, unit):
    global clf, ps, unit_list
    # Reading data from the training files
    truthful_sentences = list()
    deceptive_sentences = list()
    training_data = open(str(filename)).readlines()
    for line in training_data[1:]:
        [state, sentiment, review] = line.split(",",2)
        if int(state) == 0:
            deceptive_sentences.append(review.strip().lower())
        else:
            truthful_sentences.append(review.strip().lower())
    truthful = list()
    deceptive = list()
    tvector = list()
    dvector = list()

    # Unigram Parser
    if (str(unit).lower().strip() == "unigram"):
        for sentence in truthful_sentences:
            truthful += [ps.stem(word) for word in sentence.split()]
        for sentence in deceptive_sentences:
            deceptive += [ps.stem(word) for word in sentence.split()]
        truthful = Gram(1,truthful,2)
        deceptive = Gram(1,deceptive,2)
        unit_list = set(truthful.dictionary.keys() + deceptive.dictionary.keys())
        for word in unit_list:
            tvector.append(truthful.get_count(word))
            dvector.append(deceptive.get_count(word))
    elif(str(unit).lower().strip() == "bigram"):
        pass
    # Unichar Parser
    elif(str(unit).lower().strip() == "unichar"):
        for sentence in truthful_sentences:
            truthful+= list(sentence)
        for sentence in deceptive_sentences:
            deceptive+= list(sentence)
        truthful = Gram(1,truthful,2)
        deceptive = Gram(1,deceptive,2)
        unit_list = set(truthful.dictionary.keys() + deceptive.dictionary.keys())
        #print(unit_list)
        for char in unit_list:
            tvector.append(truthful.get_count(char))
            dvector.append(deceptive.get_count(char))
    '''
    elif(str(unit).lower().strip() == "bichar"):
        pass
    elif(str(unit).lower().strip() == "pos"):
        pass
    '''
    #tvector, dvector
    vectors = [tvector, dvector]
    states = [1, 0]
    clf = svm.SVC()
    clf.fit(vectors,states)


def test(filename, unit):
    global clf, ps, unit_list
    testing_data = open("validation_test.txt").readlines()
    correct = 0
    wrong = 0
    for line in testing_data:
        [state, sentiment, review] = line.split(",",2)
        if str(unit).lower().strip() == "unigram":
            review = [ps.stem(word) for word in review.strip().split()]
            test = Gram(1,review,2)
            vector = list()
            for word in unit_list:
                vector.append(test.get_count(word))
        elif str(unit).lower().strip() == "unichar":
            test = Gram(1,list(review.lower().strip()),2)
            vector = list()
            for char in unit_list:
                vector.append(test.get_count(char))
        prediction = clf.predict(vector)
        print("State: " + str(state) + " Prediction: " + str(prediction))
        if (int(state) == prediction):
            correct+=1
        else:
            wrong+=1
    print("Correct: " + str(correct))
    print("Wrong: " + str(wrong))
    total = wrong + correct
    print(float(correct)/float(total))

train("validation_train.txt", "unichar")
test("validation_test.txt", "unichar")
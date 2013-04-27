from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from ngram import Gram
from nltk.stem.porter import PorterStemmer

truthful = list()
deceptive = list()

training_data = open("validation_train.txt").readlines()
for line in training_data[1:]:
    [state, sentiment, review] = line.split(",",2)
    if int(state) == 0:
        deceptive+= review.strip().split()
    else:
        truthful+= review.strip().split()
# Stemming
ps = PorterStemmer()
deceptive = [ps.stem(word) for word in deceptive]
truthful = [ps.stem(word) for word in truthful]
truthful = Gram(1,truthful,1)
deceptive = Gram(1,deceptive,1)
word_list = set(truthful.dictionary.keys() + deceptive.dictionary.keys())
tvector = list()
dvector = list()
for word in word_list:
    tvector.append(truthful.get_count(word))
    dvector.append(deceptive.get_count(word))
vectors = [tvector, dvector]
states = [1, 0]
clf = svm.SVC()
clf.fit(vectors,states)
testing_data = open("validation_test.txt").readlines()
correct = 0
wrong = 0
for line in testing_data:
    [state, sentiment, review] = line.split(",",2)
    review = [ps.stem(word) for word in review.strip().split()]
    test = Gram(1,review,1)
    vector = list()
    for word in word_list:
        vector.append(test.get_count(word))
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

'''
result = clf.predict([0,.99])
print("Result: " + str(result))
'''

from sklearn import svm
from ngram import Gram

truthful = list()
deceptive = list()

training_data = open("validation_train.txt").readlines()
for line in training_data[1:]:
    [state, sentiment, review] = line.split(",",2)
    if int(state) == 0:
        deceptive+= review.strip().split()
    else:
        truthful+= review.strip().split()
truthful = Gram(1,truthful,1)
deceptive = Gram(1,deceptive,1)
word_list = set(truthful.dictionary.keys() + deceptive.dictionary.keys())
tvector = list()
dvector = list()
for word in word_list:
    tvector.append(truthful.get_count(word))
    dvector.append(deceptive.get_count(word))
vectors = [dvector, tvector]
states = [0, 1]
clf = svm.SVC()
clf.fit(vectors,states)

testing_data = open("validation_test.txt").readlines()
correct = 0
wrong = 0
for line in testing_data:
    [state, sentiment, review] = line.split(",",2)
    test = Gram(1,review.strip().split(),1)
    vector = list()
    for word in word_list:
        vector.append(test.get_count(word))
    prediction = clf.predict(vector)
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

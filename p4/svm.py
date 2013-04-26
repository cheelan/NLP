from sklearn import svm
from ngram import Gram

truthful = list()
deceptive = list()

training_data = open("Train data").readlines()
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
states = [False, True]
clf = svm.SVC()
clf.fit(vectors,states)
'''
result = clf.predict([0,.99])
print("Result: " + str(result))
'''

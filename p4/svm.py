from sklearn import svm
from ngram import Gram

truthful = list()
deceptive = list()

training_data = open("Train data").readlines()
for line in training_data:
    [state, sentiment, review] = line.split(",",2)
    if state == 0:
        deceptive+= review.strip().split()
    else:
        truthful+= review.strip().split()
truthful = Gram(1,truthful,1)
deceptive = Gram(1,deceptive,1)

print "COMPLETE"
'''
vectors = [[0,0], [1,1]]
states = [False, True]
clf = svm.SVC()
clf.fit(vectors,states)
result = clf.predict([0,.99])
print("Result: " + str(result))
'''


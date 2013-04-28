from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from ngram import Gram
from nltk.stem.porter import PorterStemmer

truthful = list()
deceptive = list()
word_list=list()

training_data = open("Train data").readlines()
for line in training_data[1:]:
	[state, sentiment, review] = line.split(",",2)
	if int(state) == 0:
		deceptive+= review.strip().lower().split()
	else:
		truthful+= review.strip().lower().split()
# Stemming
ps = PorterStemmer()
deceptive = [ps.stem(word) for word in deceptive]
truthful = [ps.stem(word) for word in truthful]
truthful = Gram(1,truthful,0)
deceptive = Gram(1,deceptive,0)

for i in truthful.dictionary.keys():
	if not (i in word_list):
		word_list.append(i)
for i in deceptive.dictionary.keys():
	if not (i in word_list):
		word_list.append(i)
		'''
word_list = set(truthful.dictionary.keys() + deceptive.dictionary.keys())
'''
tvector = list()
dvector = list()
'''
for word in word_list:
	if (truthful.get_count(word)>0):
		tvector.append(1)
	else:
		tvector.append(0)
	if (deceptive.get_count(word)>0):
		dvector.append(1)
	else:
		dvector.append(0)
		'''
for word in word_list:
	tvector.append(truthful.get_count(word))
	dvector.append(deceptive.get_count(word))
vectors = [tvector, dvector]
states = [1, 0]
clf = svm.SVC()
print clf
clf.fit(vectors,states)
testing_data = open("Test data").readlines()
correct = 0
wrong = 0
for line in testing_data:
	[state, sentiment, review2] = line.split(",",2)
	#print(line.split(",",2))
	review1 = [ps.stem(word) for word in review2.strip().lower().split()]
	print review1
	test = Gram(1,review1,0)
	vector = list()
	for word in word_list:
		vector.append(test.get_count(word))
	prediction = clf.predict(vector)
	print prediction
	#print("State: " + str(state) + " Prediction: " + str(prediction))
	'''if (int(state) == prediction):
		correct+=1
	else:
		wrong+=1
print("Correct: " + str(correct))
print("Wrong: " + str(wrong))
total = wrong + correct
print(float(correct)/float(total))
'''
'''
result = clf.predict([0,.99])
print("Result: " + str(result))
'''

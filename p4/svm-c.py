from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from ngram import Gram
from nltk.stem.porter import PorterStemmer

truthful = list()
deceptive = list()
word_list=list()

x=0
training_data = open("validation_train.txt").readlines()
for line in training_data:
    if "IsTruthFul" in line:
        continue
    isTruthful = line[0]
    [state, sentiment, review] = line.split(",")
    print(isTruthful)
    if int(isTruthful) == 0:
        deceptive+= review.lower().strip().split()
    else:
        truthful+= review.lower().strip().split()
print(deceptive)
print(truthful)
		
		
# Stemming
# ps = PorterStemmer()
# deceptive = [ps.stem(word) for word in deceptive]
# truthful = [ps.stem(word) for word in truthful]
truthful1 = Gram(2,truthful,1)
deceptive1 = Gram(2,deceptive,1)
'''
for i in truthful.dictionary.keys():
	if not (i in word_list):
		word_list.append(i)
for i in deceptive.dictionary.keys():
	if not (i in word_list):
		word_list.append(i)
		'''
#word_list = set(truthful1.dictionary.keys() + deceptive1.dictionary.keys())

testing_data = open("validation_test.txt").readlines()
correct = 0
wrong = 0
what=0
svmResults = open("svmResults.csv", 'w')
for line in testing_data:
	[state, sentiment, review] = line.split(",")
	# review = [ps.stem(word) for word in review.lower().strip().split()]
	test = Gram(2,review,1)
	test_vector = list()
	tvector = list()
	dvector = list()
	tvectorcount=1.0
	dvectorcount=1.0
	vectorcount=1.0
	
	word_list=test.dictionary.keys()

	for word in word_list:
	
		# if ((truthful1.get_count(word)/float(len(truthful1.dictionary.keys())))>(deceptive1.get_count(word)/float(len(deceptive1.dictionary.keys())))):
			# tvector.append(1)
			# dvector.append(0)
		# elif ((truthful1.get_count(word)/float(len(truthful1.dictionary.keys())))<(deceptive1.get_count(word)/float(len(deceptive1.dictionary.keys())))):
			# tvector.append(0)
			# dvector.append(1)
		# else:
			# tvector.append(0)
			# dvector.append(0)
		tvectorcount+= truthful1.get_count(word)
		dvectorcount+= deceptive1.get_count(word)
		vectorcount+= test.get_count(word)
		tvector.append((truthful1.get_count(word)))
		dvector.append(deceptive1.get_count(word))
		test_vector.append(test.get_count(word))
	# print dvector
	# print tvectorcount
	# print dvectorcount
	# print vectorcount
	tvectorNew=[x/tvectorcount for x in tvector]
	dvectorNew=[x/dvectorcount for x in dvector]
	vectorNew=[x/vectorcount for x in test_vector]
	vectors = [tvectorNew, dvectorNew]
	states = [1, 0]
	clf = svm.SVC()
	clf.fit(vectors,states)
	
	# print(tvector)
	# print(dvector)
	# print(vector)
	

	prediction = clf.predict(vectorNew)
	# print(prediction)
	# print("State: " + str(state) + " Prediction: " + str(prediction))
	# svmResults.write(str(prediction[0]) + '\n')

	
	if (int(state) == prediction):
		correct+=1
	else:
		if ((int(state)==1) & (prediction==0)):
			what+=1
		wrong+=1
print("Correct: " + str(correct))
print("Wrong: " + str(wrong))
total = wrong + correct
print(float(correct)/float(total))


# result = clf.predict([0,.99])
# print("Result: " + str(result))


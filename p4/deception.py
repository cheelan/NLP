import ngram, knn, perplexity, nltk.tokenize, sys, time

#These three methods take raw text files and convert them to lists of tokens. These lists will be the inputs 
#to the ngram constructors. Chances are it would be good to use helper function so that 
#massive amounts of code aren't repeated

def parse_line(text):
    output = ""
    i = 0
    for c in text:
        if i > 3:
            output += c
        i += 1
    return output

def get_validation_data(filename):
    f = open(filename)
    ans_list = []
    for line in f:
        if "IsTruthFul" in line:
            continue
        else:
            ans_list.append(line[0])
    return ans_list

def text_to_word_list(lst):
    dword_list = []
    tword_list = []
    for line in lst:
        if "IsTruthFul" in line:
            continue
        else:
            if line[0] == "0": #If deceptive:
                dword_list.append("<r>")
                for sent in nltk.tokenize.sent_tokenize(parse_line(line)):
                    for word in (['<s>'] + nltk.tokenize.word_tokenize(sent) + ['</s>']):
                        dword_list.append(word)
                dword_list.append("</r>")
            else:
                tword_list.append("<r>")
                for sent in nltk.tokenize.sent_tokenize(parse_line(line)):
                    for word in (['<s>'] + nltk.tokenize.word_tokenize(sent) + ['</s>']):
                        tword_list.append(word)
                tword_list.append("</r>")
    return (dword_list, tword_list)

def text_to_char_list(lst):
    dchar_list = []
    tchar_list = []
    for line in lst:
        if "IsTruthFul" in line:
            continue
        else:
            if line[0] == "0": #If deceptive:
                dchar_list.append("<r>")
                for c in parse_line(line):
                    dchar_list.append(c)
                dchar_list.append("</r>")
            else:
                #If no label is present, then we are dealing with actual test data. Just throw
                #things into the true list
                tchar_list.append("<r>")
                for c in parse_line(line):
                    tchar_list.append(c)
                tchar_list.append("</r>")
    return (dchar_list, tchar_list)

def text_to_pos_list(lst):
    dpos_list = []
    tpos_list = []
    for line in lst:
        if "IsTruthFul" in line:
            continue
        else:
            if line[0] == "0": #If deceptive:
                dpos_list.append("<r>")
                for sent in nltk.tokenize.sent_tokenize(parse_line(line)):
                    dpos_list.append("<s>")
                    text = nltk.word_tokenize(sent)
                    tagged = nltk.pos_tag(text)
                    for t in tagged:
                        dpos_list.append(t)
                    dpos_list.append("</s>")
                dpos_list.append("</r>")
            else:
                tpos_list.append("<r>")
                for sent in nltk.tokenize.sent_tokenize(parse_line(line)):
                    tpos_list.append("<s>")
                    text = nltk.word_tokenize(sent)
                    tagged = nltk.pos_tag(text)
                    for t in tagged:
                        tpos_list.append(t)
                    tpos_list.append("</s>")
                tpos_list.append("</r>")
    return (dpos_list, tpos_list)

#Returns list of string-reviews
def read_file(filename):
    with open(filename) as f:
        lst = []
        for line in f:
            lst.append(line)
    return lst

def gen_test_lists(filename):
    with open(filename) as f:
        lst = []
        for line in f:
            if not "IsTruthFul" in line:
                lst.append(parse_line(line))
    return lst


#test_list is a list of reviews, where each review is a list of words/chars/pos
#Untested but I think this is done
def test_knn(k, n, deceptive_list, truthful_list, test_list):
    knn_model = knn.Knn(k, n, deceptive_list, truthful_list)
    ans = list()
    for test in test_list:
        ans.append(knn_model.classify(test))
    return ans_list

#Note that deceptive/truthful_list is not a list of lists. 
def test_perplexity(n, smoothingBound, deceptive_list, truthful_list, test_list):
    perplexity_model = perplexity.Perplexity(n, smoothingBound, deceptive_list, truthful_list)
    ans = list()
    for test in test_list:
        ans.append(perplexity_model.classify(test))
    return ans

def ros(ouranswers, rightanswers):
    assert(len(ouranswers) == len(rightanswers))
    '''
    #Not working. Check this out: https://www.kaggle.com/c/SemiSupervisedFeatureLearning/forums/t/919/auc-implementation/6136#post6136
    ros_sample = []
    for i in range(0, len(ouranswers)):
        ros_sample.append((rightanswers[i], ouranswers[i]))
    roc = ROCData(ros_sample)
    return roc.auc()
    '''




#THIS CODE ACTUALLY RUNS THE PROGRAM

#Training reviews
#train_reviews = read_file("validation_train.txt")
train_reviews = read_file("Train data")

#Test cases (in string format)
#test_cases = gen_test_lists("validation_test.txt")
test_cases = gen_test_lists("Test data")

#Generate character lists for each test case
test_char_list = []
for t in test_cases:
    temp = text_to_char_list([t])
    test_char_list.append(temp[0] + temp[1]) 

#Generate word lists for each test case
test_word_list = []
for t in test_cases:
    temp = text_to_word_list([t])
    test_word_list.append(temp[0] + temp[1]) 

test_pos_list = []
for t in test_cases:
    temp = text_to_pos_list([t])
    test_pos_list.append(temp[0] + temp[1]) 


#Deceptive and truthful lists (not n-grams)
#(dchar_list, tchar_list) = text_to_char_list(train_reviews)
#(dword_list, tword_list) = text_to_word_list(train_reviews)
(dpos_list, tpos_list) = text_to_pos_list(train_reviews)

#p_attempts = test_perplexity(2, 2, dchar_list, tchar_list, test_char_list)
#p_attempts = test_perplexity(2, 2, dword_list, tword_list, test_word_list)
p_attempts = test_perplexity(2, 2, dpos_list, tpos_list, test_pos_list)
print(str(p_attempts))


#print("ROS Score: " + str(ros(p_attempts, get_validation_data("validation_test.txt"))))
#print(str(p_attempts))


print("Done")
sys.exit()
#print text_to_char_list('test_small.txt')


import ngram, knn, perplexity
#These three methods take raw text files and convert them to lists of tokens. These lists will be the inputs 
#to the ngram constructors. Chances are it would be good to use helper function so that 
#massive amounts of code aren't repeated

def text_to_word_list(filename):
    #Should use <s> and </s> in this one only, probably
    pass

def text_to_char_list(filename):
    pass

def text_to_pos_list(filename):
    pass



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







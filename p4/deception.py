import ngram, knn, perplexity, nltk.tokenize
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

def text_to_word_list(filename):
    f = open(filename)
    word_list = []
    for line in f:
        if "IsTruthFul" in line:
            continue
        else:
            word_list.append("<r>")
            for sent in nltk.tokenize.sent_tokenize(parse_line(line)):
                for word in (['<s>'] + nltk.tokenize.word_tokenize(sent) + ['</s>']):
                    word_list.append(word)
            word_list.append("</r>")
    return word_list

def text_to_char_list(filename):
    f = open(filename)
    char_list = []
    for line in f:
        if "IsTruthFul" in line:
            continue
        else:
            char_list.append("<r>")
            for c in parse_line(line):
                char_list.append(c)
            char_list.append("</r>")
    return char_list

def text_to_pos_list(filename):
    f = open(filename)
    pos_list = []
    for line in f:
        if "IsTruthFul" in line:
            continue
        else:
            pos_list.append("<r>")
            for sent in nltk.tokenize.sent_tokenize(parse_line(line)):
                pos_list.append("<s>")
                text = nltk.word_tokenize(sent)
                tagged = nltk.pos_tag(text)
                for t in tagged:
                    pos_list.append(t)
                pos_list.append("</s>")
            pos_list.append("</r>")
    return pos_list

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

#print text_to_char_list('test_small.txt')
#print text_to_word_list('test_small.txt')
#print text_to_pos_list('test_small.txt')
print get_validation_data('Train data')

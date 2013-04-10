import sys, nltk, re, math, string, pickle, ngram
from nltk.stem.porter import PorterStemmer
from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist, GoodTuringProbDist
#from nltk.corpus import stopwords

nsize = 0
allowed_pos = ["FW", "JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
#allowed_pos = ["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]

# Converts the score number to index number
def score_to_index(score):
    return score + 2

# Filters out words that are not useful. Removes all instances of stopwords and performs Porter stemming. 
def filter(word_list):
    #return word_list        # turns off stemming
    filtered_features = list()
    # Parts of Speech filtering
    result = nltk.pos_tag(word_list)
    for i in range(len(result)):
        if str(result[i][1]) in allowed_pos:
            filtered_features.append(result[i][0])
    '''
    # Porter Stemming & Stopwords Filtering
    ps = PorterStemmer()
    for w in word_list:
        if not w in stopwords.words('english'):
            w = ps.stem(w)
            filtered_features.append(w)
    '''
    # Check to see if resulting filtered size is big enough. 
    if len(filtered_features) < nsize:
        return word_list
    else:
        return filtered_features

#This will work to calculate log(a+b+c)
#See the equation after "more generally" at
#http://en.wikipedia.org/wiki/List_of_logarithmic_identities#Summation.2Fsubtraction
def log_3sum(a, b, c):
    #print("V\t" + str(a) + "\tTrans\t" + str(b) + "\tEmit\t" + str(c))
    #return math.log(a) + math.log(1+math.exp(math.log(b)+math.log(1+math.exp(math.log(c)-math.log(b)))-math.log(a)))
    return a + b + c

# Open the training file and extract the scores of the individual sentences for testing purposes. 
def get_ans(filename):
    data = open(filename, 'r')
    scores = list()
    if (data == None):
        print("Error: Training file not found")
    else:
        # Initialize 
        data = data.readlines()
        for line in data:
            # Check to see if it is a review header
            if (line[0] == '[' or line[0] == '\n'):
                continue 
            # Check to see if it is a paragraph header
            if (line[0] == '{'):
                line = line.split(' ')
                score = int(re.findall(r'-?\d', line[-1])[0])
                scores.append(score)
            # For all other sentences
            else:
                line = line.split(' ')
                score = int(re.findall(r'-?\d', line[-1])[0])
                scores.append(score)
        return scores


class Node:
    #If we use NLTK for n-gram stuff, you can't add new training data to an existing model
    #Therefore, we'll need to keep track of a list of sentences, and append to that throughout
    #the training process. When that's done, generate an nltk ngram model. In order to go with this,
    #we need to first come up with a reliable way to determine the exact probability from the perplexity
    #of a sentence.

    def __init__(self, score, n, num_states):
        self.n = n
        self.id = score
        self.count = 0
        self.sentence_list = []
        self.transition_counts = [0]*num_states
        self.paragraph_count = 0

    #Get the probability of transitioning from current score to next score
    def get_transition_probability(self, next_score):
        new_index = score_to_index(next_score)
        total_transitions = 0
        for i in self.transition_counts:
            total_transitions += i
        return float(self.transition_counts[new_index]) / float(total_transitions) 

class HMM:

    author = ""
    nodes = None
    prev_score = 0
    num_sentences = 0
    num_paragraphs = 0
    n = -1

    def __init__(self, states, author, n):
        self.n = n
        self.nodes = [Node(score, n, len(states)) for score in range(-2,3)]
        self.prev_score = self.gen_initial_state()       
        self.author = author

    #For picking the first state of a paragraph. For now, start at 0, but try fancy things later
    def gen_initial_state(self):
        return 0

    #Given a training file, train the hidden markov model.
    def train(self, filename):
        data = open(filename, 'r')
        if (data == None):
            print("Error: Training file not found")
        else:
            # Initialize 
            data = data.readlines()
            for line in data:
                # Check to see if it is a review header or empty line
                if (line[0] == '[' or line[0] == '\n'):
                    continue
                # Increment total number of sentences parsed.
                self.num_sentences += 1                
                # Check to see if it is a paragraph header
                if (line[0] == '{'):
                    self.num_paragraphs += 1
                    line = line.split()
                    score = int(re.findall(r'-?\d', line[-1])[0])
                    self.nodes[score_to_index(score)].sentence_list.append(filter(line[1:-1]))
                    self.nodes[score_to_index(score)].paragraph_count += 1
                # For all other sentences
                else:
                    line = line.split()
                    score = int(re.findall(r'-?\d', line[-1])[0])
                    self.nodes[score_to_index(score)].sentence_list.append(filter(line[:-1]))
                self.nodes[score_to_index(self.prev_score)].transition_counts[score_to_index(score)] += 1
                self.nodes[score_to_index(score)].count += 1
                self.prev_score = score
            #print("Finished generating training data")
            est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
            for node in self.nodes:
                node.ngram_model = NgramModel(self.n, node.sentence_list, estimator=est)

    def test(self, filename):
        data = open(filename, 'r')
        l = list()
        ans = list()
        if (data == None):
            print("Error: Training file not found")
        else:
            # Initialize 
            data = data.readlines()
            for line in data:
                # Check to see if it is a review header
                if (line[0] == '[' or line[0] == '\n'):
                    if len(l) > 0:
                        t = self.viterbi(l)
                        assert len(t) == len(l)
                        ans += t
                        #print(ans)
                    l = list()
                    continue
                # Check to see if it is a paragraph header
                if (line[0] == '{'):
                    l.append(line)
                # For all other sentences
                else:
                    l.append(line)
            #print("Finished parsing test data")
            return ans
            return self.viterbi(l)

    def get_initial_prob(self, state):
        return float(self.nodes[score_to_index(state)].paragraph_count) / float(self.num_paragraphs)

    #Returns an approximation of the log probability of a sentence appearing in the specified state
    def get_log_prob(self, sentence, state):
        split_sentence = sentence.split(" ")[0:-1]
        if split_sentence[0] == '{}':
            split_sentence = split_sentence[1:]
        split_sentence = filter(split_sentence)
        p = self.nodes[score_to_index(state)].ngram_model.entropy(split_sentence) * (len(split_sentence) - (self.n - 1))
        return p

    #Outputs a sequence of sentiments using the viterbi algorithm
    def viterbi(self, sentence_list):
        V = [{}]
        path = {}
        # Initialize base cases (t == 0)
        for y in self.nodes:
            V[0][score_to_index(y.id)] = (-1 * math.log(self.get_initial_prob(y.id))) + self.get_log_prob(sentence_list[0], y.id)
            path[score_to_index(y.id)] = [y.id]

        # Run Viterbi for t > 0
        for t in range(1,len(sentence_list)):
            V.append({})
            newpath = {}
            for y in self.nodes:
                id = y.id
                #Double check that transition_prob gets y.id and not y0.id
                (prob, state) = min([(log_3sum(V[t-1][score_to_index(y0.id)], (-1 * math.log(y0.get_transition_probability(y.id))), (self.get_log_prob(sentence_list[t], y.id))), y0.id) for y0 in self.nodes])
                V[t][score_to_index(y.id)] = prob
                #newpath[score_to_index(y.id)] = path[score_to_index(state)] + [score_to_index(y.id)]   # corresponds to p=p-2 in the end, but gives -4 as a guess
                newpath[score_to_index(y.id)] = path[score_to_index(state)] + [y.id]
            # Don't need to remember the old paths
            path = newpath
        (prob, state) = min([(V[len(sentence_list) - 1][score_to_index(y.id)], y.id) for y in self.nodes])
        return path[score_to_index(state)]



for num in range(4,11):
    print("N=" + str(num))
    nsize=num
    testhmm = HMM([-2, -1, 0, 1, 2], "Testing", nsize)
    testhmm.train("ds_val_train.txt")
    attempts = testhmm.test("ds_val_test.txt")
    ans = get_ans("ds_val_test.txt")
    # Calculate our accuracy score.
    i = 0
    correct = 0
    for p in attempts:
        #p=p-2   # corresponds to score_to_index(y.id)
        if ans[i] == p:
            correct += 1
        #else:
            #print("Attempt: " + str(p) + " Ans: " + str(ans[i]))
        i += 1
    print("Accuracy: " + str(float(correct) / float(i)))
    countForRMS=0
    squareSum=0.
    for p in attempts:
        diffSq= (float(ans[countForRMS])-p)**2
        squareSum += diffSq
        countForRMS += 1
    RMS=(squareSum/len(attempts))**(0.5)
    print("RMS: " + str(RMS))
###########################################################################################

'''
### KAGGLE stuff ###
testhmm = HMM([-2, -1, 0, 1, 2], "Testing", 6)
testhmm.train("DennisSchwartz_train.txt")
attempts = testhmm.test("DennisSchwartz_test.txt")
'''
'''
testhmm.train("ScottRenshaw_train.txt")
attempts = testhmm.test("ScottRenshaw_test.txt")
'''
'''
hmmResults = open("HMMResults.csv", 'w')
for p in attempts:
    hmmResults.write(str(p) + '\n')
'''


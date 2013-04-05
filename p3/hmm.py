import sys, nltk, re, math, string, pickle
from nltk.stem.porter import PorterStemmer
from nltk.corpus import brown
from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist

def score_to_index(score):
    return score + 2

class Node:
    node_id = 0 #Also known as score
    n = -1 #n in n-gram
    count = 0
    transition_counts = []
    sentence_list = list()
    ngram_model = None 

    #If we use NLTK for n-gram stuff, you can't add new training data to an existing model
    #Therefore, we'll need to keep track of a list of sentences, and append to that throughout
    #the training process. When that's done, generate an nltk ngram model. In order to go with this,
    #we need to first come up with a reliable way to determine the exact probability from the perplexity
    #of a sentence.

    def __init__(self, score, n, num_states):
        self.n = n
        self.score = score
        self.transition_counts = [0]*num_states

    #Get the probability of transitioning from the previous score to the current score
    def get_transition_probability(self, prev_score):
        new_index = score_to_index(prev_score)
        total_transitions = 0
        for i in self.transition_counts:
            total_transitions += i
        return float(self.transition_counts[new_index]) / float(total_transitions) 

    #Add this sentence's n-grams to the bucket
    #Update transition counts
    def train_sentence(self, sentence, prev):
        pass

    #Given a sentence, return the a score (proportional to probability) for this model
    def get_sentence_score(self, sentence, prev):
        pass

class HMM:

    author = ""
    nodes = []
    prev_score = 0
    num_sentences = 0
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
                # Check to see if it is a review header
                if (line[0] == '['):
                    continue
                # Increment total number of sentences parsed.
                self.num_sentences += 1
                
                # Check to see if it is a paragraph header
                if (line[0] == '{'):
                    line = line.split(' ')
                    score = int(re.findall(r'-?\d', line[-1])[0])
                    #score = int(line[-1][1:-1])
                    #par_score = int(line[0][1:-1])
                    #par_score = re.findall(r'\b\d+\b', line[0])[0]
                    self.nodes[score_to_index(score)].sentence_list.append(line[1:-1])
                # For all other sentences
                else:
                    line = line.split(' ')
                    score = int(re.findall(r'-?\d', line[-1])[0])
                    index = score_to_index(score)
                    self.nodes[score_to_index(score)].sentence_list.append(line)
                self.nodes[score_to_index(self.prev_score)].transition_counts[score_to_index(score)] += 1
                self.nodes[score_to_index(score)].count += 1
                self.prev_score = score
            print("Finished generating training data")
            for node in self.nodes:
                node.ngram_model = NgramModel(self.n, node.sentence_list)
            #with open('supervised_training.pickle', 'wb') as f: 
            #    pickle.dump(self.wsd, f)
            #    print("Done pickling")

    def get_initial_prob(self, state):
        return float(self.nodes[score_to_index(state)].count) / float(self.num_sentences)

    #Returns an approximation of the log probability of a sentence appearing in the specified state
    def get_log_prob_from_entropy(self, sentence, state):
        split_sentence = sentence.split(" ")
        return self.nodes[get_index_from_score(state)].entropy(split_sentence) * len(split_sentences)

    #Outputs a sequence of sentiments using the viterbi algorithm
    def viterbi(self, sentence_list):
        V = [{}]
        path = {}
        # Initialize base cases (t == 0)
        for y in self.nodes:
            V[0][y.id] = math.log(init_prob) + self.get_log_prob_from_entropy(sentence_list[0], y.id)
            path[y.id] = [y.id]

        # Run Viterbi for t > 0
        for t in range(1,len(sentence_list)):
            V.append({})
            newpath = {}
 
            for y in self.nodes:
                id = y.id
                #Double check that transition_prob gets y.id and not y0.id
                (prob, state) = max([(V[t-1][y0.id] + y0.get_transition_probability(y.id) + self.get_lob_prob(sentence_list[t], y.id), y0.id) for y0 in self.nodes])
                V[t][y] = prob
                newpath[y] = path[state] + [y]
 
            # Don't need to remember the old paths
            path = newpath
        (prob, state) = max([(V[len(sentence_list) - 1][y.id], y.id) for y in self.nodes])
        return path[state]

testhmm = HMM([-2, -1, 0, 1, 2], "Testing", 2)
testhmm.train("testcases/test1.txt")
print(str(testhmm.nodes[1].transition_counts))
'''
est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
lm = NgramModel(2, brown.words(categories='news'), estimator=est)
#lm1 = NgramModel(2, ["apple", "ate", "an", "apple"], estimator=est)
#lm2 = NgramModel(2, ["nlp", "ran", "cat", "dog"], estimator=est)

sen = "as a coincidence he gave frank some kind of a stress relieving pill the previous night which frank took in a moment of weakness and desperation as he followed mary to this drug pad concerned that she couldnt handle the strain any longer of learning about her fathers death especially when she wasnt able to put a closure on their stormy relationship by having one last chance to talk to him she hasnt even seen her father for the last three years due to an argument"
sen2 = "askddfesf adsafe asdfhjkbeew jbdajse joiuewoeuih hgjd jgbna jkasdaf"
sen3 = "We congratulate the entire membership on its record of good legislation"



split_sentence = sen.split(" ")
logprob = lm.entropy(split_sentence) + math.log(len(split_sentence))

perplexity = math.exp(-1. * lm.entropy(sen.split(" ")))
perplexity2 = math.exp(-1. * lm.entropy(sen2.split(" ")))
perplexity3 = math.exp(-1. * lm.entropy(sen3.split(" ")))
#print("Words " + str(sen.count(" ")))
#probability = 1. / float((perplexity ** (sen.count(" "))))
print(str(perplexity))
print(str(perplexity2))
print(str(perplexity3))
#print(str(probability))
'''
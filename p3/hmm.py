import sys, nltk, re, math, string, pickle
from nltk.stem.porter import PorterStemmer
from nltk.corpus import brown
from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist

def score_to_index(score):
    return score + 2

class Node:
    id = 0 #Also known as score
    n = -1 #n in n-gram
    emission_probability = 0.
    transition_counts = []

    def __init__(self, score, n, num_states):
        self.n = n
        self.score = score
        self.transition_probabilities = [0]*num_states

    #Get the probability of transitioning from the previous score to the current score
    def _get_transition_probability(self, prev_score):
        new_index = score_to_index(prev_score)
        sum = 0
        for i in self.transition_counts:
            sum += i
        return float(self.transition_counts[new_index]) / float(sum) 

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

    def __init__(self, states, author):
        self.nodes = []*len(states)
        i = 0
        score = -2
        for node in self.nodes:
            self.nodes[i] = Node(score, len(self.nodes))
            score += 1
            i += 1
            
        self.author = author

    #Given a parsed sentence and its sentiment score, train it
    def train_sentence(self, sentence, score):
        index = score_to_index(score)
        self.nodes[index].train_sentence(sentence)

    #Outputs a sequence of sentiments using the viterbi algorithm
    def viterbi(self, sentence_list):
        pass



est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
#lm = NgramModel(2, brown.words(categories='news'), estimator=est)
lm1 = NgramModel(2, ["apple", "ate", "an", "apple"], estimator=est)
lm2 = NgramModel(2, ["nlp", "ran", "cat", "dog"], estimator=est)


print(len(brown.words(categories='news')))

#print(str(lm.perplexity(["apple", "ate", "an", "apple"])))
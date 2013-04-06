import unittest
import hmm

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.hmm = hmm.HMM([-2, -1, 0, 1, 2], "author", 2)
        self.hmm.train("testcases/test1.txt")

    '''
    The probability of transitioning from a to b is equal to (number of times a -> b / number of times 
    a appears) 
    '''
    def test_transition_prob(self):
        self.assertEqual(0., self.hmm.nodes[2].get_transition_probability(-2)) 
        self.assertEqual(0.8, self.hmm.nodes[2].get_transition_probability(0)) 
        self.assertEqual(0.2, self.hmm.nodes[2].get_transition_probability(1))
        self.assertEqual(1., self.hmm.nodes[1].get_transition_probability(0))

    '''
    Initial prob should probably be the number of times the first sentence in a paragraph has state x
    divided by the number of paragraphs.
    '''
    def test_initial_prob(self):
        self.assertEqual(0., self.hmm.get_initial_prob(1))
        self.assertEqual(1., self.hmm.get_initial_prob(0))


if __name__ == '__main__':
    unittest.main()

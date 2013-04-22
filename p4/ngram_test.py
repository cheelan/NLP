import unittest
import ngram

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        
        self.apple_gram = ngram.Gram(2, ["apple", "ate", "an", "apple", "ate"], 1)
        print(str(self.apple_gram.getPerplexity(["apple", "ate", "a", "cat"])))
        print(str(self.apple_gram.getPerplexity(["orange", "grape", "lemon", "tomato"])))

    def test_count(self):
        self.assertEqual(2, self.apple_gram.get_count(["apple", "ate"]))
        self.assertEqual(0, self.apple_gram.get_count(["apple", "asdf"]))  


if __name__ == '__main__':
    unittest.main()

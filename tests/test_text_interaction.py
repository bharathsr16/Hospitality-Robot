import unittest
import nltk
from hospitality_robot.text_interaction import handle_text_input, get_intent

class TestTextInteraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        try:
            nltk.data.find('chunkers/maxent_ne_chunker')
        except LookupError:
            nltk.download('maxent_ne_chunker')
        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words')


    def test_handle_text_input(self):
        self.assertEqual(handle_text_input("hello"), "Hello! How can I help you today?")
        self.assertEqual(handle_text_input("goodbye"), "I'm sorry, I don't understand. Please try again.")

    def test_get_intent(self):
        self.assertEqual(get_intent("where is the event hall"), ("find_location", "the"))
        self.assertEqual(get_intent("where is the restroom"), ("find_location", "the"))
        self.assertEqual(get_intent("what is your name"), ("unknown", None))


if __name__ == '__main__':
    unittest.main()

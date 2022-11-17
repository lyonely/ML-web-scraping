import unittest

from transformers import pipeline

from backend.nlp_model import NLPModel

nlp_model = NLPModel(pipeline("question-answering", model="deepset/roberta-base-squad2"))

class TestGetKeywords(unittest.TestCase):
    """ Tests model's ability to get keywords"""

    def test_single_word(self):
        """ Tests a single word """
        self.assertEqual('fat', nlp_model.get_keywords('fat', 1)[0])
        self.assertEqual('palantir', nlp_model.get_keywords('palantir', 1)[0])

    def test_simple_questions(self):
        """ Tests simple questions """
        self.assertEqual('fat', nlp_model.get_keywords('What is fat?', 1)[0])
        self.assertEqual(set(['much', 'sugar']), set(nlp_model.get_keywords('How much sugar?', 2)))

    def test_complex_questions(self):
        """ Tests simple questions """
        self.assertEqual(set(['cheapest', 'red', 'shirt']),
            set(nlp_model.get_keywords('What is the cheapest red shirt?',3)))
        self.assertEqual(set(['protein', 'chicken', 'breast']),
            set(nlp_model.get_keywords('What is the chicken breast with the most protein?',3)))


class TestCorrection(unittest.TestCase):
    """ Tests corrections """
    def test_correction(self):
        """ Tests correction """
        return

class TestProductQuestionAccuracy(unittest.TestCase):
    """ Tests product question accuracy """
    def test_simple_question(self):
        """ Test simple questions """
        return

class TestProductQuestionDistilAccuracy(unittest.TestCase):
    """ Test product question distilled accuracy """
    def test_simple_question(self):
        """ Test simple question """
        return

class TestProductQuestionCaching(unittest.TestCase):
    """ Test cachin capabilities """
    def asdf(self):
        """ Calls the same thing twice, checks that its the same result"""
        return

if __name__ == '__main__':
    unittest.main()

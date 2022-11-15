import unittest
from unittest.mock import MagicMock


from macro_nlp import get_keywords, product_question, correction
from pipeline import product_question


class TestGetKeywords(unittest.TestCase):

    def test_single_word(self):
        self.assertEqual('fat', get_keywords('fat', 1)[0])
        self.assertEqual('palantir', get_keywords('palantir', 1)[0])
    
    def test_simple_questions(self):
        self.assertEqual('fat', get_keywords('What is fat?', 1)[0])
        self.assertEqual(set(['much', 'sugar']), set(get_keywords('How much sugar?', 2)))
    
    def test_complex_questions(self):
        self.assertEqual(set(['cheapest', 'red', 'shirt']), set(get_keywords('What is the cheapest red shirt?',3)))
        self.assertEqual(set(['protein', 'chicken', 'breast']), set(get_keywords('What is the chicken breast with the most protein?',3)))


class TestCorrection(unittest.TestCase):
    def test_correction(self):
        return 

"""
websites to test: 

"""

TESCO_CHICKEN_BREAST = "https://www.tesco.com/groceries/en-GB/shop/fresh-food/fresh-meat-and-poultry/fresh-chicken/chicken-breast"
COINDESK_FTX_ARTICLE = "https://www.coindesk.com/policy/2022/11/14/ftxs-failure-is-sparking-a-massive-regulatory-response/"
RALPH_LAUREN_SHIRTS = "https://www.ralphlauren.co.uk/en/men/clothing/casual-shirts/10202"
SAINSBURY_BIRTHDAY_CAKE = "https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/gb/groceries/bakery/birthday-and-party-cakes?storeId=10151&langId=44&krypto=jEX9d9HSjnYMPacveOtMiSpWjHBza6wYss%2FSTRit4YXzQHspyRQIT9g8yaoy6BJBrHqHxSlw3SbpA%2FKmMHmXsLKOle%2FVwjFEOUcbn3JrW7vPOfPl36tJw%2BG8pCFFWuc3hw%2Fjvd8s1LfIa0jmIEZheiATnz1o23fJY3qko6Y7%2FZ0%3D&ddkey=https%3Agb%2Fgroceries%2Fbakery%2Fbirthday-and-party-cakes#langId=44&storeId=10151&catalogId=10241&categoryId=340928&parent_category_rn=12320&top_category=12320&pageSize=60&orderBy=FAVOURITES_ONLY%7CSEQUENCING%7CTOP_SELLERS&searchTerm=&beginIndex=0&hideFilters=true&facet="


class TestProductQuestionAccuracy(unittest.TestCase):
    def test_simple_question(self):
        return


class TestProductQuestionDistilAccuracy(unittest.TestCase):
    def test_simple_question(self):
        return



class TestProductQuestionCaching(unittest.TestCase):
    def asdf(self):
        return
    #call the same thing twice, check that its the same result + faster
    


if __name__ == '__main__':
    unittest.main()
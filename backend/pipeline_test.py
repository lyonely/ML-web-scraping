import unittest
from unittest.mock import MagicMock
import unittest.mock
from pipeline import products_to_question




class TestProductsToQuestion():
    @unittest.mock.patch('macro_nlp.product_question', return_value = "")
    def test_products_to_question(self, mock_product_question):
        with unittest.mock.patch('macro_nlp.product_question', return_value = ""):
            print("hel")
            print(products_to_question(set("1", "2", "3")))
            print("hello")
            self.assertEqual("", products_to_question(set("1", "2", "3")))
    #mock product_question to return something, then should be quite straightforward


class TestGetProductUrls():
    print(" test get products")
    def a():
        return

class TestGetTagsFromProduct():
    print(" test get tags")
    def a():
        return

if __name__ == '__main__':
    unittest.main()
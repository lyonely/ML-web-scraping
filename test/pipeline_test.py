import unittest
import unittest.mock
from backend.pipeline import Pipeline

class PipelineTest(unittest.TestCase):
    """ Class to test pipelines"""
    @unittest.mock.patch('macro_nlp.product_question', return_value = "")
    def test_products_to_question(self):
        """ Tests getting products to questions"""
        pipeline = Pipeline()
        with unittest.mock.patch('macro_nlp.product_question', return_value = ""):
            self.assertEqual("", pipeline.products_to_question(set("1", "2", "3")))

    def get_product_urls(self):
        """ Tests getting product urls"""
        return

    def get_tags(self):
        """ Tests getting tags from products """
        return

if __name__ == '__main__':
    unittest.main()

import sys
from typing import Set
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

from transformers import pipeline
from selenium import webdriver
#pylint: disable-next=unused-import, import-error
import chromedriver_binary

from backend.db_connection import db_product_urls, db_send, db_products_to_keyword
from backend.webscraper import soup
from backend.nlp_model import NLPModel

class Pipeline:
    """ Orchestrates the entire flow of data from query to output"""

    def __init__(self):
        """ Initializes the Pipeline object """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1400,2100")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.url = ""
        self.question = ""
        self.model = NLPModel(pipeline("question-answering",
                                       model="deepset/roberta-base-squad2"))

    def get_product_urls(self):
        """ Get the urls for the product page """
        product_urls = db_product_urls(self.url)
        # If product_urls don't exist, run through algorithm
        if product_urls is None:
            page = soup(self.driver, self.url)
            domain = urlparse(self.url).netloc
            products = set()
            links = set(page.select('a'))
            for link in links:
                to_scrape: str = "https://" + \
                    str(domain) + \
                    str(link.get('href'))
                if '/products/' in to_scrape:
                    products.add(to_scrape)

            db_send({"url": self.url, "products": list(products)}, "urls")

        else:
            products = product_urls["products"]
        return products

    def products_to_question(self, products: Set[str]):
        """ Runs the ML pipeline to get macro for products """
        products_to_question = {}
        while len(products) > 0:
            product = products.pop()
            try:
                page = soup(self.driver, product).find_all()
                tags = [str(tag).strip().lower() for tag in page]
                answer = self.model.product_question(tags, str(self.question).strip().lower())
                products_to_question[product] = answer
            except (HTTPError, URLError):
                continue

        return {"search_query": self.url,
                "question": self.question,
                "products_to_question": products_to_question}

    def main(self, url, keyword):
        """ Find the product and its relevant macro information and stores it in a database """
        self.url = str(url)
        self.question = keyword

        # rudimentary caching for questions

        cached_result = db_products_to_keyword(self.url, keyword)
        if cached_result is not None:
            return cached_result

        product_urls: set = self.get_product_urls()
        res: dict = self.products_to_question(product_urls)
        db_send(res, "ml_results")
        res.pop("_id", None)
        return res

    def one_product_main(self, url, question):
        """ Find the product and its relevant macro information and stores it in a database """
        self.url = str(url)
        self.question = question

        question_keyword = "fat"

        # rudimentary caching for questions
        cached_result = db_products_to_keyword(self.url, question_keyword)
        if cached_result is not None:
            return cached_result
        product_urls = set()
        product_urls.add(url)
        res: dict = self.products_to_question(product_urls)
        db_send(res, "single_result")
        res.pop("_id", None)
        return res


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.one_product_main(sys.argv[1], sys.argv[2])
    # pipeline.main(sys.argv[1], sys.argv[2])

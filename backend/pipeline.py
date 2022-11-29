import sys
from typing import Set
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
# pylint: disable-next=unused-import, import-error
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
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        chrome_options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.url = ""
        self.question = ""
        self.html = ""
        self.model = NLPModel()

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
                page = soup(self.driver, product)
                tags = [str(tag).strip().lower() for tag in page.find_all()]
                # alternate = self.model.alternate_algorithm(str(page), self.question)
                answer = self.model.product_question(tags, str(self.question).strip().lower())
                products_to_question[product] = answer
            except (HTTPError, URLError):
                continue

        return {"search_query": self.url,
                "question": self.question,
                "products_to_question": products_to_question}

    def html_answer(self):
        """ Uses html code to find relevant information """
        products_to_question = {}

        tags = BeautifulSoup(self.html, 'html.parser').find_all()
        tags = [str(tag).strip().lower() for tag in tags.find_all()]

        answer = self.model.product_question(tags, str(self.question).strip().lower())
        products_to_question[self.url] = answer

        return {"search_query": self.url,
                "question": self.question,
                "products_to_question": products_to_question}

    def multiple_products(self, url, keyword):
        """ Find the product and its relevant macro information and stores it in a database """
        self.url = str(url)
        self.question = keyword

        cached_result = db_products_to_keyword(self.url, keyword, is_multiple=True)
        if cached_result is not None:
            return cached_result

        product_urls: set = self.get_product_urls()
        res: dict = self.products_to_question(product_urls)
        db_send(res, is_multiple=True)
        res.pop("_id", None)
        return res

    def single_product(self, url, question):
        """ Find the product and its relevant macro information and stores it in a database """
        self.url = str(url)
        self.question = str(question).strip().lower()

        cached_result = db_products_to_keyword(self.url, question)
        if cached_result is not None:
            return cached_result

        product_urls = set()
        product_urls.add(url)
        res: dict = self.products_to_question(product_urls)
        db_send(res)
        return res

    def single_product_html(self, url, question, html):
        """ Find the product and its relevant macro information and stores it in a database """
        self.url = str(url)
        self.question = str(question).strip().lower()
        self.html = str(html).strip()

        cached_result = db_products_to_keyword(self.url, question)
        if cached_result is not None:
            print("Cache Hit!!")
            return cached_result

        res: dict = self.html_answer()
        db_send(res)
        res.pop("_id", None)
        return res


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.single_product(sys.argv[1], sys.argv[2])

from typing import Set
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from selenium import webdriver
# pylint: disable-next=unused-import, import-error
import chromedriver_binary
from backend.db_connection import *
from backend.webscraper import soup, soup_without_driver
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

    """ This is for a regular POST Request for multiple products (i.e. in a product grid) """
    def multiple_products(self, url, question):
        """ Find the product and its relevant macro information and stores it in a database """
        self.url = str(url)
        self.question = question

        cached_result = db_products_to_keyword(self.url, question)
        if cached_result is not None:
            return cached_result

        product_urls: set = self.get_product_urls()
        res: dict = self.multiple_products_answer(product_urls)
        db_send_results(res)
        res.pop("_id", None)
        return res

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

            db_send_url({"url": self.url, "products": list(products)})
        else:
            products = product_urls["products"]

        return products

    def multiple_products_answer(self, products: Set[str]):
        """ Runs the ML pipeline to get macro for products """
        answers: list = []
        while len(products) > 0:
            product = products.pop()
            try:
                # find the html source of the page if it has already been scraped
                page = db_product_html_source(product)
                if page is None:
                    page = soup(self.driver, product)
                    db_send_html({"url": product, "html": str(page)})
                else:
                    page = soup_without_driver(page["html"])

                tags = [str(tag).strip().lower() for tag in page.find_all()]
                answer = self.model.product_question(tags, str(self.question).strip().lower())
                answers.append((product, answer))
            except (HTTPError, URLError):
                continue

        return {"url": self.url,
                "question": self.question,
                "answer": answers}

    """ This is for a regular POST Request for a single product """
    def single_product(self, url, question):
        self.url = str(url)
        self.question = str(question).strip().lower()

        cached_result = db_products_to_keyword(self.url, self.question)
        if cached_result is not None:
            return cached_result

        res: dict = self.single_product_answer(url)
        db_send_results(res)
        res.pop("_id", None)
        return res

    def single_product_answer(self, product: str):
        """ Runs the ML pipeline to get macro for a single product """
        try:
            page = soup(self.driver, product)
            tags = [str(tag).strip().lower() for tag in page.find_all()]
            answer = self.model.product_question(tags, str(self.question).strip().lower())
            return {"url": self.url,
                    "question": self.question,
                    "answer": answer}

        except (HTTPError, URLError):
            return {}

    """ This is for when the frontend sends the page source in the POST Request """
    def single_product_html(self, url, question, html):
        self.url = str(url)
        self.question = str(question).strip().lower()
        self.html = str(html).strip()

        cached_result = db_products_to_keyword(self.url, self.question)
        if cached_result is not None:
            return cached_result

        res: dict = self.single_product_answer_html()
        db_send_results(res)
        res.pop("_id", None)
        return res

    def single_product_answer_html(self):
        """ Uses html code to find relevant information """
        tags = soup_without_driver(self.html).find_all()
        tags = [str(tag).strip().lower() for tag in tags]

        answer = self.model.product_question(tags, str(self.question).strip().lower())

        return {"url": self.url,
                "question": self.question,
                "answer": answer}


from db_connection import db_product_urls, db_send, db_products_to_keyword
from webscraper import soup
from macro_nlp import MacroNLP
from transformers import pipeline
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from selenium import webdriver
import sys
from typing import Set
from typing import List

class Pipeline:

    def __init__(self) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1400,2100")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')  # will need a random one in the future

        self.DRIVER = webdriver.Chrome(chrome_options=chrome_options)
        # self.DRIVER = None
        self.URL = ""
        self.QUESTION = ""
        self.macroNLP = MacroNLP(pipeline("question-answering",
                                model="deepset/roberta-base-squad2"))


    def get_product_urls(self):
        product_urls = db_product_urls(self.URL)
        # If product_urls don't exist, run through algorithm
        if product_urls is None:
            page = soup(self.DRIVER, self.URL)
            domain = urlparse(self.URL).netloc
            products = set()
            links = set(page.select('a'))
            for link in links:
                to_scrape: str = "https://" + str(domain) + str(link.get('href'))
                if '/products/' in to_scrape:
                    products.add(to_scrape)

            db_send({"url": self.URL, "products": list(products)}, "urls")

        else:
            products = product_urls["products"]
        return products

    # def get_tags_from_product(self, product):
    #     page = soup(self.DRIVER, product).find_all()
    #     return [str(tag).strip().lower() for tag in page]

    def products_to_question(self, products: Set[str]):
        """ Runs the ML pipeline to get macro for products """
        products_to_question = {}

        while len(products) > 0:
            product = products.pop()
            try:
                page = soup(self.DRIVER, product).find_all()
                tags = [str(tag).strip().lower() for tag in page]
                # tags = self.get_tags_form_product(product)
                answer = self.macroNLP.product_question(tags, str(self.QUESTION).strip().lower())
                #answer = product_question_distil(tags, str(QUESTION).strip().lower())
                products_to_question[product] = answer
            except (HTTPError, URLError):
                continue

        return {"search_query": self.URL, "question": self.QUESTION, "products_to_question": products_to_question}




    def main(self, url, question):
        """ Find the product and its relevant macro information and stores it in a database """
        #pylint: disable-next=global-statement
        #flobal URL, QUESTION, DRIVER
        self.URL = str(url)
        self.QUESTION = question

        # Find result in MongoDB / Cached
        #cached_result = db_products_to_keyword(URL, QUESTION)

        #rudimentary caching for questions
        question_keyword = self.macroNLP.get_keywords(self.QUESTION, 1)[0]

        cached_result = db_products_to_keyword(self.URL, question_keyword)

        if cached_result is not None:
            return cached_result

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("window-size=1400,2100")
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        #     (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        # chrome_options.add_argument(f'user-agent={user_agent}')  # will need a random one in the future

        # self.DRIVER = webdriver.Chrome(chrome_options=chrome_options)
        try:
            product_urls: set = self.get_product_urls()
            res: dict = self.products_to_question(product_urls)
            db_send(res, "ml_results")
            res.pop("_id", None)
            return res
        finally:
            self.DRIVER.quit()

if __name__ == "__main__":
    pipeline = Pipeline()
    print(pipeline.main(sys.argv[1], sys.argv[2]))

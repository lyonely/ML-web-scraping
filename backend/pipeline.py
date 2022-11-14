import sys
import os

from typing import Set
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
#pylint: disable-next=unused-import, import-error
import chromedriver_binary
from selenium import webdriver

from webscraper import soup
from macro_nlp import product_question, get_keywords
from db_connection import db_product_urls, db_send, db_products_to_keyword


os.environ["TOKENIZERS_PARALLELISM"] = "false"

DRIVER = None
URL = ""
KEYWORD = ""
QUESTION = ""


def get_product_urls():
    """ Look for product urls in MongoDB """

    product_urls = db_product_urls(URL)
    # If product_urls don't exist, run through algorithm
    if product_urls is None:
        page = soup(DRIVER, URL)
        domain = urlparse(URL).netloc
        products = set()
        links = set(page.select('a'))
        for link in links:
            to_scrape: str = "https://" + str(domain) + str(link.get('href'))
            if '/products/' in to_scrape:
                products.add(to_scrape)

        db_send({"url": URL, "products": list(products)}, "urls")

    else:
        products = product_urls["products"]
    return products


def products_to_question(products: Set[str]):
    """ Runs the ML pipeline to get macro for products """
    products_to_keyword = {}

    while len(products) > 0:
        product = products.pop()
        try:
            page = soup(DRIVER, product).find_all()
            tags = [str(tag).strip().lower() for tag in page]
            answer = product_question(tags, str(QUESTION).strip().lower())
            products_to_keyword[product] = answer
        except (HTTPError, URLError):
            continue

    return {"search_query": URL, "keyword": KEYWORD, "products_to_keyword": products_to_keyword}


def main(url, question):
    """ Find the product and its relevant macro information and stores it in a database """
    #pylint: disable-next=global-statement
    global URL, QUESTION, DRIVER
    URL = str(url)
    QUESTION = question

    # Find result in MongoDB / Cached
    #cached_result = db_products_to_keyword(URL, QUESTION)

    #rudimentary caching for questions
    question_keyword = get_keywords(QUESTION, 1)[0]

    cached_result = db_products_to_keyword(URL, question_keyword)

    if cached_result is not None:
        return cached_result

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')  # will need a random one in the future

    DRIVER = webdriver.Chrome(chrome_options=chrome_options)
    try:
        product_urls: set = get_product_urls()
        res: dict = products_to_question(product_urls)
        db_send(res, "ml_results")
        res.pop("_id", None)
        return res
    finally:
        DRIVER.quit()


if __name__ == "__main__":
    print(main(sys.argv[1], sys.argv[2]))

import sys
import os

from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from backend.webscraper import *
from backend.macro_nlp import product_macro
from backend.db_connection import *

# pylint: disable-next=unused-import, import-error
os.environ["TOKENIZERS_PARALLELISM"] = "false"

DRIVER = None
URL = ""
KEYWORD = ""


def get_product_urls():
    """ Retrieves products and their relevant macro information """
    page = soup(DRIVER, URL)
    domain = urlparse(URL).netloc
    products = set()
    links = set(page.select('a'))
    for link in links:
        to_scrape: str = "https://" + str(domain) + str(link.get('href'))
        if '/products/' in to_scrape:
            products.add(to_scrape)

    return products


def products_to_macro(products: set[str]):
    products_to_keyword = {}

    while len(products) > 0:
        product = products.pop()
        try:
            page = soup(DRIVER, product).find_all()
            tags = [str(tag).strip().lower() for tag in page]
            answer = product_macro(tags, str(KEYWORD).strip().lower())
            products_to_keyword[product] = answer
        except Exception:
            continue

    return {"search_query": URL, "keyword": KEYWORD, "products_to_keyword": products_to_keyword}


def main(url, keyword, amount):
    # supported keywords: [fat, protein, carbohydrate, price]
    """ Find the product and its relevant macro information and stores it in a database """
    global URL, KEYWORD, DRIVER
    URL = str(url)
    KEYWORD = keyword

    # """ Find result in MongoDB / Cached """
    cached_result = db_products_to_keyword(URL, KEYWORD)
    if cached_result is not None:
        return cached_result

    """ Look for product urls in MongoDB """
    product_urls = set(db_product_urls(URL)["products"])
    DRIVER = webdriver.Chrome(service=Service("./backend/drivers/chromedriver"))

    """ If product_urls don't exist, run through algorithm """
    if product_urls is None:
        product_urls: set = get_product_urls()
        db_send({"url": URL, "products": list(product_urls)}, "urls")

    try:
        res: dict = products_to_macro(product_urls)
        db_send(res, "ml_results")
        return res
    finally:
        DRIVER.quit()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

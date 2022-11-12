import sys
import os

from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from backend.webscraper import get_soup
from backend.macro_nlp import product_macro
from backend.db_connection import *

# pylint: disable-next=unused-import, import-error
os.environ["TOKENIZERS_PARALLELISM"] = "false"

DRIVER = webdriver.Chrome(service=Service("./backend/drivers/chromedriver"))
URL = ""
KEYWORD = ""
MAX_AMT = 0

def get_product_urls():
    """ Retrieves products and their relevant macro information """
    soup = get_soup(DRIVER, URL)
    domain = urlparse(URL).netloc
    products = set()
    try:
        links = set(soup.select('a'))
        for link in links:
            if len(products) == MAX_AMT:
                break
            to_scrape = "https://" + str(domain) + str(link.get('href'))
            if '/products/' in to_scrape:
                products.add(to_scrape)

    except Exception as exc:
        raise Exception("Error while reading CSS selector") from exc

    finally:
        return products


def products_to_macro_json(products: set):
    product_to_macro = {}

    while len(products) > 0:
        product = products.pop()
        try:
            soup = get_soup(DRIVER, product).find_all()
            tags = [str(tag).strip().lower() for tag in soup]
            answer = product_macro(tags, str(KEYWORD).strip().lower())
            product_to_macro[product] = answer
        except Exception:
            continue

    return {"search_query": URL, "products_to_macro": product_to_macro}


def main(url, keyword, amount):
    """ Find the product and its relevant macro information and stores it in a database """
    global URL, KEYWORD, MAX_AMT
    URL = str(url)

    """ Find result in MongoDB / Cached """
    cached_result = get_result(URL)
    if cached_result is not None:
        DRIVER.quit()
        return cached_result

    """ If not in DB, run through algorithm. """
    KEYWORD = keyword
    MAX_AMT = int(amount)
    res = {}
    try:
        product_urls = get_product_urls()
        res = products_to_macro_json(product_urls)
        return res
    except Exception or FloatingPointError:
        pass
    finally:
        DRIVER.quit()
        send_json_to_database(res)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

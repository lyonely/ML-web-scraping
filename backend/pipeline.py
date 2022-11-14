import sys
import os

from typing import Set
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
#pylint: disable-next=unused-import, import-error
import chromedriver_binary
from backend.webscraper import get_soup
from backend.macro_nlp import product_question

os.environ["TOKENIZERS_PARALLELISM"] = "false"

DRIVER = None
URL = ""
KEYWORD = ""

def products_to_question_json(driver, url: str, question: str, requested_amt: int):
    """ Retrieves products and their relevant macro information """
    soup = get_soup(driver, url)
    products_url = []
    try:
        links = soup.select('a')
        for link in links:
            to_scrape = 'https://www.tesco.com' + str(link.get('href'))
            if '/products/' in to_scrape:
                products_url.append(to_scrape)

def get_product_urls():
    """ Look for product urls in MongoDB """

    product_to_question = {}
    for product in products_url:
        soup = get_soup(driver, product).find_all()
        tags: List[str] = [str(tag).strip().lower() for tag in soup]
        question = str(question).strip().lower()

        answer = product_question(tags, question)
        product_to_question[product] = answer

        if len(product_to_question) == requested_amt:
            break

    json_object = json.dumps({
        "search_query": url,
        "products_to_macro": product_to_question
    })

def products_to_macro(products: Set[str]):
    """ Runs the ML pipeline to get macro for products """
    products_to_keyword = {}

    while len(products) > 0:
        product = products.pop()
        try:
            page = soup(DRIVER, product).find_all()
            tags = [str(tag).strip().lower() for tag in page]
            answer = product_macro(tags, str(KEYWORD).strip().lower())
            products_to_keyword[product] = answer
        except (HTTPError, URLError):
            continue

    return {"search_query": URL, "keyword": KEYWORD, "products_to_keyword": products_to_keyword}


def main(url, question, requested_amt):
    """ Find the product and its relevant macro information and stores it in a database """
    #pylint: disable-next=global-statement
    global URL, KEYWORD, DRIVER
    URL = str(url)
    KEYWORD = keyword

    # Find result in MongoDB / Cached
    cached_result = db_products_to_keyword(URL, KEYWORD)
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
        res = products_to_question_json(driver, url, question, int(requested_amt))
    finally:
        DRIVER.quit()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

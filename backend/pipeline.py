import json
import sys
import os
from typing import List
from selenium import webdriver
from backend.webscraper import get_soup
from backend.macro_nlp import product_macro
os.environ["TOKENIZERS_PARALLELISM"] = "false"



def products_to_macro_json(driver, url: str, macro: str):
    """ Retrieves products and their relevant macro information """
    soup = get_soup(driver, url)
    products_url = set()

    try:
        links = soup.select('a')
        for link in links:
            to_scrape = 'https://www.tesco.com' + str(link.get('href'))
            if '/products/' in to_scrape:
                products_url.add(to_scrape)

    except Exception as exc:
        raise Exception("Error while reading CSS selector") from exc

    product_to_macro = {}
    for product in products_url:
        soup = get_soup(driver, product).find_all()
        tags: List[str] = [str(tag).strip().lower() for tag in soup]
        macro = str(macro).strip().lower()

        answer = product_macro(tags, macro)
        product_to_macro[product] = answer

    json_object = json.dumps({
        "search_query": url,
        "products_to_macro": product_to_macro
    })

    return json_object


# pylint: disable-next=fixme
# TODO: Create function to send results to database
# def send_to_database(json_result):
#     pass


def main(url, macro):
    """ Find the product and its relevant macro information and stores it in a database """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
        res = products_to_macro_json(driver, url, macro)
    finally:
        driver.quit()

    return res
    # send res to database
    # send_to_database(res)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

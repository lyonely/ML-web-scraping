import json
import sys
import os
from typing import List
from selenium import webdriver
#pylint: disable-next=unused-import, import-error
import chromedriver_binary
from backend.webscraper import get_soup
from backend.macro_nlp import product_question

os.environ["TOKENIZERS_PARALLELISM"] = "false"


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

    except Exception as exc:
        raise Exception("Error while reading CSS selector") from exc

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

    return json_object


# pylint: disable-next=fixme
# TODO: Create function to send results to database
# def send_to_database(json_result):
#     pass


def main(url, question, requested_amt):
    """ Find the product and its relevant macro information and stores it in a database """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')  # will need a random one in the future

    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        res = products_to_question_json(driver, url, question, int(requested_amt))
    finally:
        driver.quit()

    return res
    # send res to database
    # send_to_database(res)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1], sys.argv[2])

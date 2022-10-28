import json
import sys
from webscraper import get_soup
from macro_nlp import product_macro

def products_to_macro_json(url, macro):
    soup = get_soup(url)
    products_url = set()

    try:
        links = soup.select('a')
        for link in links:
            to_scrape = 'https://www.tesco.com' + str(link.get('href'))
            if '/products/' in to_scrape:
                products_url.add(to_scrape)

    except Exception:
        raise Exception("Error while reading CSS selector")


    product_to_macro = {}
    for product in products_url:
        answer = product_macro(product, macro)
        product_to_macro[product] = answer

    json_object = json.dumps({
        "search_query" : url,
        "products_to_macro": product_to_macro
    })

    return json_object


def send_to_database(json_result):
    pass


def main(url, macro):
    res = products_to_macro_json(url, macro)
    # send res to database
    send_to_database(res)
    # print(product_macro("https://www.tesco.com/groceries/en-GB/products/293133930", "fat"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
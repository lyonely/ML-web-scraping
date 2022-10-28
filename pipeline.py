import json
import sys
from webscraper import get_soup
from macro_nlp import product_macro

def products_to_macro_json(url, macro):
    """ Retrieves products and their relevant macro information """
    soup = get_soup(url)
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
        answer = product_macro(product, macro)
        product_to_macro[product] = answer

    json_object = json.dumps({
        "search_query" : url,
        "products_to_macro": product_to_macro
    })

    return json_object

# pylint: disable-next=fixme
# TODO: Create function to send results to database
# def send_to_database(json_result):
#     pass


def main(url, macro):
    """ Find the product and its relevant macro information and stores it in a database """
    res = products_to_macro_json(url, macro)
    return res
    # send res to database
    # send_to_database(res)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

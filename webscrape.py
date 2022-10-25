import json
import sys
from util import get_soup
from transformers import pipeline
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

def create_json(url, macro):
    soup = get_soup(url)
    # try:
    links = soup.select('a')
    products = set()
    i = 0
    for link in links:
        to_scrape = 'https://www.tesco.com' + str(link.get('href'))

        if '/products/' in to_scrape:
            i+=1
            products.add(to_scrape)
            if i == 1:
                break
    print(products)
    product_to_macro = {}
    for product in products:
        print("")
        # result = question_answerer(question=q, context=c)
        # print(result)
    #     product_to_macro[product] = 0
    #

    json_object = json.dumps({
        "search_query" : url,
        "products_to_macro": product_to_macro
    })

    return json_object

def helper(product_url, macro):
    gs = get_soup(product_url)
    i = 0
    results = []
    for tag in gs.find_all():
        context = str(tag)
        if "Fat" in context:
            print(context)
            i += 1
            q = "what is " + macro
            # result = question_answerer(question=q, context=context)
            # results.append(result)
            if i == 2:
                break



    print(i)
    # for tag in gs.find_all():
    #     print(str(tag))
    #     i += 1
    #     if macro in tag:
    #         l.append(str(tag))
    #     # find the value of the macro, store it in some set()
    #     # n = valueOfMacro(macro, soup)
    #     q = "what is " + macro
    # c = str(gs)
    # print([])
    # print(c)
    # return c

def main(url, macro):
    print(helper("https://www.tesco.com/groceries/en-GB/products/277043162", macro))
    # print(create_json(url, macro))

if __name__ == "__main__":
    # python3 webscrape.py "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all" "fat"
    main(sys.argv[1], sys.argv[2])
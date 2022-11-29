from pymongo import MongoClient

CLIENT_URL = "mongodb+srv://nasty:palantir@mlscraper.mkyk7w5.mongodb.net/" + \
    "?retryWrites=true&w=majority"

try:
    conn = MongoClient(CLIENT_URL)
    db = conn["MLScraper"]
    urls = db["urls"]
    ml_results = db["ml_results"]
except ConnectionError:
    print("Could not connect to MongoDB")


def db_send(data: dict, is_multiple=False):
    """ Sends data to MongoDB. Need to add functionality to update it."""
    if is_multiple:
        ml_results.insert_one(data)
    else:
        urls.insert_one(data)


def db_products_to_keyword(url: str, question: str, is_multiple=False):
    """ Retrieves object associated with url and keyword"""
    if is_multiple:
        result = ml_results.find_one({"search_query": url, "question": question}, {"_id": 0, "products_to_question": 1})
    else:
        result = urls.find_one({"search_query": url, "question": question}, {"_id": 0, "products_to_question": 1})

    return result


def db_product_urls(url: str):
    """ Retrieves object associated with url"""
    result = urls.find_one({"url": url}, {"_id": 0, "products": 1})
    return result

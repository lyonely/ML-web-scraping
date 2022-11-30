from backend.timer import timed
from pymongo import MongoClient

CLIENT_URL = "mongodb+srv://nasty:palantir@mlscraper.mkyk7w5.mongodb.net/" + \
    "?retryWrites=true&w=majority"

try:
    conn = MongoClient(CLIENT_URL)
    db = conn["MLScraper"]
    ml_results = db["ml_results"]
    urls = db["urls"]
except ConnectionError:
    print("Could not connect to MongoDB")

@timed
def db_send(data: dict, collection: str):
    """ Sends data to MongoDB. Need to add functionality to update it."""
    if collection == "ml_results":
        ml_results.insert_one(data)
    else:
        urls.insert_one(data)

@timed
def db_products_to_keyword(url: str, keyword: str):
    """ Retrieves object associated with url and keyword"""
    result = ml_results.find_one({"search_query": url, "keyword": keyword}, \
        {"products_to_keyword": 1})

    if result:
        result.pop('_id', None)

    return result

@timed
def db_product_urls(url: str):
    """ Retrieves object associated with url"""
    result = urls.find_one({"url": url}, {"products": 1})

    if result:
        result.pop('_id', None)

    return result

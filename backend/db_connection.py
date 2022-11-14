from pymongo import MongoClient

CLIENT_URL = "mongodb+srv://nasty:palantir@mlscraper.mkyk7w5.mongodb.net/?retryWrites=true&w=majority"

try:
    conn = MongoClient(CLIENT_URL)
    db = conn["MLScraper"]
    ml_results = db["ml_results"]
    urls = db["urls"]
except ConnectionError:
    print("Could not connect to MongoDB")


def db_send(data: dict, collection: str):
    # add functionality to update result
    if collection == "ml_results":
        ml_results.insert_one(data)
    else:
        urls.insert_one(data)


def db_products_to_keyword(url: str, keyword: str):
    return ml_results.find_one({"search_query": url, "keyword": keyword}, {"products_to_keyword": 1})


def db_product_urls(url: str):
    return urls.find_one({"url": url}, {"products": 1})

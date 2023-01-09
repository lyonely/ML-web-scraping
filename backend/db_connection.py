from pymongo import MongoClient

CLIENT_URL = "mongodb+srv://nasty:palantir@mlscraper.mkyk7w5.mongodb.net/" + \
             "?retryWrites=true&w=majority"

try:
    conn = MongoClient(CLIENT_URL)
    db = conn["MLScraper"]
    urls = db["urls"]
    htmls = db["htmls"]
    ml_results = db["ml_results"]
except ConnectionError:
    print("Could not connect to MongoDB")


def db_send_url(data: dict):
    """ Sends urls to MongoDB """
    urls.insert_one(data)


def db_send_html(data: dict):
    """ Sends html page sources to MongoDB """
    htmls.insert_one(data)


def db_send_results(data: dict):
    """ Sends results to MongoDB """
    ml_results.insert_one(data)


def db_products_to_keyword(url: str, question: str):
    """ Retrieves object associated with url and keyword"""
    result = ml_results.find_one({"url": url, "question": question}, {"_id": 0, "answer": 1})
    return result


def db_product_urls(url: str):
    """ Retrieves object associated with url"""
    result = urls.find_one({"url": url}, {"_id": 0, "products": 1})
    return result


def db_product_html_source(url: str):
    result = htmls.find_one({"url": url}, {"_id": 0, "html": 1})
    return result

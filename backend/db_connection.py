from pymongo import MongoClient

CLIENT_URL = "mongodb+srv://nasty:palantir@mlscraper.mkyk7w5.mongodb.net/?retryWrites=true&w=majority"

try:
    conn = MongoClient(CLIENT_URL)
    db = conn["MLScraper"]
    collection = db["data"]
except ConnectionError:
    print("Could not connect to MongoDB")


def send_json_to_database(data):
    collection.insert_one(data)


def get_result(url: str):
    return collection.find_one({"search_query": url}, {"products_to_macro": 1})

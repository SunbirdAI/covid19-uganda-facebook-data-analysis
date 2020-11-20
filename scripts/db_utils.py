from pymongo import MongoClient


def get_db_collection(db_name, collection_name):
    client = MongoClient()
    db = client[db_name]
    return db[collection_name]

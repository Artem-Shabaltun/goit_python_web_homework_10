from pymongo import MongoClient
from pymongo.server_api import ServerApi


def get_mongodb():
    uri = "mongodb+srv://ArtemShabaltun:567432@cluster0.mu1oyrf.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client["hw"]
    return db
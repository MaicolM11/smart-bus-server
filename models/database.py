from flask_pymongo import PyMongo
from pymongo import MongoClient

class Database:
    
    _instance = None
    
    def __init__(self):
        raise Error('call instance()')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = MongoClient('mongodb+srv://root:root@cluster.tg7qi.mongodb.net/?retryWrites=true&w=majority')['smart-bus']
        return cls._instance

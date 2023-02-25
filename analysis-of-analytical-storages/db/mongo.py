from pymongo import MongoClient
import pandas as pd
from db.base import BaseStorage
import json


class MongoStorage(BaseStorage):

    def __init__(self):
        self._conn = MongoClient("localhost", 27017)
        db = self._conn["test_db"]
        collection = db["test_collection"]
        collection

    def _execute(self, *args):
        pass

    def _execute_many(self, *args):
        pass

    def create(self):
        pass

    def insert_many(self):
        self._conn = MongoClient("localhost", 27017)
        db = self._conn["test_db"]
        collection = db["test_collection"]
        collection
        df = pd.read_csv("./test.csv", delimiter=",", encoding="utf-8", low_memory=False)
        payload = json.loads(df.to_json(orient='records'))
        result = collection.insert_many(payload)
        len(result.inserted_ids)


    def drop(self):
        self._conn = MongoClient("localhost", 27017)
        self._conn.drop_database("test_db")

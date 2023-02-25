from pymongo import MongoClient
import pandas as pd
from db.base import BaseStorage


class MongoStorage(BaseStorage):

    def __init__(self):
        self._conn = MongoClient("localhost", 27017)
        db = self._conn["test_db"]
        collection = db["test_collection"]
        collection

    def _execute(self, *args):
        pass

    def create(self):
        pass

    def _execute_many(self, *args):
        pass
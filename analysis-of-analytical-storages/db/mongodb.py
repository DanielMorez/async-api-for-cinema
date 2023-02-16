from pymongo import MongoClient

from db.base import BaseStorage


class MongoDBStorage(BaseStorage):

    db = self._conn["test_db"]
    collection = db["test_collection"]

    def __init__(self):
        self._conn = MongoClient("localhost", 27017)

    def _execute(self, *args):
        self._conn.execute(*args)

    def _execute_many(self, *args):
        return self._execute(*args)

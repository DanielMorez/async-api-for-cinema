from pymongo import MongoClient, collection

from db.base import BaseStorage


class MongoDBStorage(BaseStorage):
    CREATE_QUERY = """
            CREATE TABLE  IF NOT EXISTS  views
                (
                    id UInt64,
                    user_id String,
                    movie_id String,
                    likes boolean,
                    stars smallint,
                    viewed_frame UInt64,
                    event_time DateTime
                )
        """

    def __init__(self):
        self._client = MongoClient("localhost", 27017)
        self._db = self._client['mongo_db']
        self.collection = self._db['mongo_collection']
        collection

    def _execute(self, *args):
        self._conn.execute(*args)

    def _execute_many(self, *args):
        return self._execute(*args)

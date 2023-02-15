from pymongo import MongoClient

from db.base import BaseStorage


class MongoDBStorage(BaseStorage):
    CREATE_QUERY = """
            CREATE TABLE  IF NOT EXISTS  views
                (
                    id UInt64,
                    user_id String,
                    movie_id String,
                    viewed_frame UInt64,
                    event_time DateTime
                )

        """

    def __init__(self):
        self._conn = MongoClient("localhost", 27017)

    def _execute(self, *args):
        self._conn.execute(*args)

    def _execute_many(self, *args):
        return self._execute(*args)

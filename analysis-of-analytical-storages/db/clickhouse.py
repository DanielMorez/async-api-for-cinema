from clickhouse_driver import Client
from db.base import BaseStorage


class ClickHouseStorage(BaseStorage):
    CREATE_QUERY = """
            CREATE TABLE  IF NOT EXISTS  views
                (
                    id Int64,
                    user_id Int64,
                    movie_id Int64,
                    stars Int64,
                    viewed_frame Int64,
                    likes Int64,
                    event_time DateTime
                )
            ENGINE = MergeTree
            ORDER BY id;
        """

    def __init__(self):
        self._conn = Client(host="localhost")

    def _execute(self, *args):
        self._conn.execute(*args)

    def create(self):
        self._execute(self.CREATE_QUERY)

    def drop(self):
        self._execute(self.DROP_QUERY)

    def _execute_many(self, *args):
        return self._execute(*args)
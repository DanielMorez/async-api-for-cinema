from clickhouse_driver import Client

from db.base import BaseStorage


class ClickHouseStorage(BaseStorage):
    CREATE_QUERY = """
            CREATE TABLE  IF NOT EXISTS  views
                (
                    id UInt64,
                    user_id String,
                    movie_id String,
                    viewed_frame UInt64,
                    event_time DateTime
                )
            ENGINE = MergeTree
            ORDER BY id;
        """

    def __init__(self):
        self._conn = Client(host="localhost")

    def _execute(self, *args):
        self._conn.execute(*args)

    def _execute_many(self, *args):
        return self._execute(*args)

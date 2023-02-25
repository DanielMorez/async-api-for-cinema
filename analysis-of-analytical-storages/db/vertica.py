from vertica_python import connect

from db.base import BaseStorage


class VerticaStorage(BaseStorage):
    CREATE_QUERY = """
        CREATE TABLE views (
            id INTEGER NOT NULL,
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        );
        """

    def __init__(self):
        self._conn = connect(
            host="127.0.0.1",
            port=5433,
            user="dbadmin",
            password="",
            database="docker",
            autocommit=True,
        )
        self._cursor = self._conn.cursor()

    def _execute(self, *args):
        self._cursor.execute(*args)

    def _execute_many(self, *args):
        self._cursor.executemany(*args)

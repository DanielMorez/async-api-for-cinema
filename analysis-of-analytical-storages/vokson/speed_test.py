import time
from abc import ABC, abstractmethod


class SpeedTest(ABC):
    @abstractmethod
    def test_insert_data(self, query, data):
        ...

    @abstractmethod
    def test_get_data(self, query):
        ...


class DBSpeedTest(SpeedTest):
    def __init__(self, db_connection):
        self.db = db_connection

    def test_insert_data(self, query, rows_gen):
        start_time = time.time()

        for rows in rows_gen:
            self.db.execute(query, rows)
            
        end_time = time.time()
        return end_time - start_time

    def test_get_data(self, query):
        start_time = time.time()
        self.db.execute(query)
        end_time = time.time()
        return end_time - start_time


class VerticaSpeedTest(SpeedTest):
    def __init__(self, cursor):
        self.cursor = cursor

    def test_insert_data(self, query, rows_gen):
        start_time = time.time()

        for rows in rows_gen:
            self.cursor.executemany(query, rows)

        end_time = time.time()
        return end_time - start_time

    def test_get_data(self, query):
        start_time = time.time()
        self.cursor.execute(query)
        end_time = time.time()
        return end_time - start_time

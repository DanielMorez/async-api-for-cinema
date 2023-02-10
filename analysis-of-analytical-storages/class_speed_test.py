import time
from abc import ABC, abstractmethod


class SpeedTest(ABC):

    def test_insert_data(self, query, data):
        pass

    @abstractmethod
    def test_get_data(self, query):
        pass


class ClickHouseSpeedTest(SpeedTest):
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
        self.cursor = cursor.cursor()


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

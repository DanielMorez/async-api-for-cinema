import time
from abc import ABC, abstractmethod
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        return end_time - start_time

    return timeit_wrapper


class BaseStorage(ABC):
    DROP_QUERY = "DROP TABLE  IF EXISTS  views;"

    @abstractmethod
    def _execute(self, *args):
        pass

    @abstractmethod
    def _execute_many(self, *args):
        pass

    def create(self):
        self._execute(self.CREATE_QUERY)

    def drop(self):
        self._execute(self.DROP_QUERY)

    @timeit
    def insert(self, query, data_generator):
        for data in data_generator:
            self._execute_many(query, data)

    @timeit
    def select(self, query):
        self._execute(query)

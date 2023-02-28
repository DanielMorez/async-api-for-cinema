import time

from functools import wraps
from mongo_vs_clickhouse.core.stats import STATS


def timeit(func):
    @wraps(func)
    def inner(instance, table, *args, **kwargs):
        start_time = time.perf_counter()
        response = func(instance, table, *args, **kwargs)
        end_time = time.perf_counter()
        delta = end_time - start_time

        STATS[str(instance)][f"{table}_{func.__name__}"].append(delta)

        return response

    return inner

from data.generate import create_fake_data, generate_data_from_file
from db.clickhouse import ClickHouseStorage
from db.mongo import MongoStorage
from pymongo import MongoClient
import pandas as pd
import time
import json


click_db = ClickHouseStorage()
mongo_db = MongoStorage()


def print_time(sec, db_name=""):
    print(f"{db_name} Time: {sec:.4f} sec")


def prepare_fake_data():
    print(f"*** Write 10 000 000 CSV on hard drive ***")
    create_fake_data()


def create():
    click_db.create()
    mongo_db.create()


def drop():
    click_db.drop()
    mongo_db.drop()


def execute_query(execute_method, times, *args):
    t = 0
    for _ in range(times):
        t += execute_method(*args)
    return t/times


def get_time_of_query(execute_method_name, times, query, data=None):
    click_execute_method = getattr(click_db, execute_method_name)

    print(f"*** {query} ***")

    args = (
        (
            query,
            data,
        )
        if data
        else (query,)
    )

    print_time(execute_query(click_execute_method, times, *args), "CLICKHOUSE")

    print("")


def insert():
    print(f"*** INSERT 10 000 000 rows ***")

    print_time(
        execute_query(
            click_db.insert,
            1,
            "INSERT INTO views VALUES",
            generate_data_from_file(True),
        ),
        "CLICKHOUSE",
    )

    start = time.time()
    mongo_db.insert_many()
    end = time.time()
    print(f"Elapsed: {(end - start) * 1000} ms")


def select():
    for query in [
        "SELECT COUNT(*) FROM views",
        "SELECT count(DISTINCT movie_id) FROM views",
        "SELECT movie_id, count(distinct likes) FROM views GROUP by movie_id",
        """
        SELECT 
            movie_id, 
            sum(stars),
            max(stars) 
        FROM views
        GROUP by movie_id
        """,
    ]:
        get_time_of_query("select", 3, query)

    _conn = MongoClient("localhost", 27017)
    db = _conn["test_db"]
    collection = db["test_collection"]
    collection
    start = time.time()
    db.collection.count()
    end = time.time()
    print(f"Elapsed: {(end - start) * 1000} ms")

    start = time.time()
    mongo_db.collection.find({"Id": "234000"})
    end = time.time()
    print(f"Elapsed: {(end - start) * 1000} ms")


if __name__ == "__main__":
    create_fake_data()
    drop()
    create()
    insert()
    select()

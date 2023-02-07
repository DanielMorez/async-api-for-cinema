import random
import time
from datetime import datetime
import vertica_python
from tqdm.contrib.concurrent import process_map

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': False,
    'use_prepared_statements': True,
}

user_ids = [str(x) for x in range(10000)]
movie_ids = [str(x) for x in range(10000)]


def create_database(connection_info):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE views (
            id IDENTITY,
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        );
        """)


def generate_row() -> tuple:
    row = (random.choice(user_ids), random.choice(movie_ids), random.randint(1, 180), datetime.now())
    return row


def insert_1000_rows(x):
    connection = vertica_python.connect(**connection_info)
    cursor = connection.cursor()
    values = [generate_row() for i in range(1000)]
    start = time.time()
    try:
        cursor.executemany(
            'INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)', values)
    except Exception as e:
        raise e
    cursor.close()
    connection.commit()
    connection.close()
    end = time.time()
    print(end - start)


def generate_data():

    _max = 10000
    process_map(insert_1000_rows, range(0, _max), max_workers=4, chunksize=1)


    # for _ in tqdm(range(_max)):
    #     insert_1000_rows(cursor)


if __name__ == '__main__':
    # create_database(connection_info)
    generate_data()

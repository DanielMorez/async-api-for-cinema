import time
from functools import wraps

import vertica_python

from OLAP_research.vertica.data_generator import generate_row

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'use_prepared_statements': True,
}


def measure(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            print(end - start)
            print('\n')

    return inner


@measure
def insert_n_rows(connection, n):
    query = 'INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)'
    print('Executing insert query. Rows:', n)
    print(query)
    cursor = connection.cursor()
    values = [generate_row() for i in range(n)]
    try:
        cursor.executemany(query, values)
    except Exception as e:
        raise e
    cursor.close()


@measure
def execute_query(connection, query: str, show_result: bool = True):
    print('Executing query')
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    if show_result:
        for row in cursor.iterate():
            print(row)
    cursor.close()
    print('Query execution took: ')


if __name__ == '__main__':
    connection = vertica_python.connect(**connection_info)

    select_count = 'SELECT COUNT(*) FROM views'
    execute_query(connection, select_count)

    select_unique_movie_id = 'SELECT count(DISTINCT movie_id) FROM views'
    execute_query(connection, select_unique_movie_id)

    select_unique_user_id = 'SELECT count(DISTINCT user_id) FROM views'
    execute_query(connection, select_unique_user_id)

    select_group_by = """
    SELECT
        user_id,
        count(movie_id)
    FROM views
    GROUP by user_id
    """
    execute_query(connection, select_group_by, show_result=False)

    select_aggregated = """
    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    GROUP by user_id
    """
    execute_query(connection, select_aggregated, show_result=False)

    select_where = """
    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    WHERE event_time > '2021-04-13 23:09:02'
    GROUP by user_id
    """
    execute_query(connection, select_where, show_result=False)

    insert_n_rows(connection, 10)
    insert_n_rows(connection, 100)
    insert_n_rows(connection, 1000)

    execute_query(connection, select_count)

    connection.commit()
    connection.close()

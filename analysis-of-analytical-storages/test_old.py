from data.generate import create_fake_data, generate_data_from_file
from db.clickhouse import ClickHouseStorage
from db.vertica import VerticaStorage

click_db = ClickHouseStorage()
vertica_db = VerticaStorage()


def print_time(sec, db_name=""):
    print(f"{db_name} Time: {sec:.4f} sec")


def prepare_fake_data():
    print(f"*** Write 10 000 000 CSV on hard drive ***")
    create_fake_data()


def create():
    click_db.create()
    vertica_db.create()


def drop():
    click_db.drop()
    vertica_db.drop()


def execute_query(execute_method, times, *args):
    t = 0
    for _ in range(times):
        t += execute_method(*args)
    return t/times


def get_time_of_query(execute_method_name, times, query, data=None):
    click_execute_method = getattr(click_db, execute_method_name)
    vertica_execute_method = getattr(vertica_db, execute_method_name)

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
    print_time(execute_query(vertica_execute_method, times, *args), "VERTICA")

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

    print_time(
        execute_query(
            vertica_db.insert,
            1,
            """
                INSERT INTO views (id, user_id, movie_id, viewed_frame, event_time) 
                VALUES (%s,%s,%s,%s,%s)
            """,
            generate_data_from_file(False),
        ),
        "VERTICA",
    )

    print("")


def select():
    for query in [
        "SELECT COUNT(*) FROM views",
        "SELECT count(DISTINCT movie_id) FROM views",
        "SELECT count(DISTINCT user_id) FROM views",
        "SELECT user_id, count(distinct movie_id) FROM views GROUP by user_id",
        """
        SELECT 
            user_id, 
            sum(viewed_frame),
            max(viewed_frame) 
        FROM views
        GROUP by user_id
        """,
        """
        SELECT 
            user_id, 
            sum(viewed_frame),
            max(viewed_frame) 
        FROM views
        WHERE event_time > '2021-04-13 23:09:02'
        GROUP by user_id
        """,
    ]:
        get_time_of_query("select", 3, query)


if __name__ == "__main__":
    create_fake_data()
    drop()
    create()
    insert()
    select()
from db.clickhouse.clickhouse_client import ch_client
from db.vertica.vertica_client import vt_client
from class_speed_test import ClickHouseSpeedTest, VerticaSpeedTest
from test_data.fake_data import data_generator

ch_speed_test = ClickHouseSpeedTest(ch_client)
vertica_speed_test = VerticaSpeedTest(vt_client)


def execute_query(times, query, speed_test):
    t = 0
    for _ in range(times):
        t += speed_test.test_get_data(query)
    return t
def test_read_query(query, times=3):
    print(f'*** {query} ***')
    t = execute_query(times, query, ch_speed_test)
    print(f"CLICK HOUSE - {t/times:.4f} sec")

    t = execute_query(times, query, vertica_speed_test)
    print(f"VERTICA - {t/times:.4f} sec")

    print("")

def test_read():
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
        """
    ]:
        test_read_query(query)


if __name__ == "__main__":
    test_read()

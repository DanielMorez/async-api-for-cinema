from db.clickhouse.clickhouse_client import ch_client
from db.clickhouse.data_scheme import flush_ch, init_ch
from db.vertica.data_scheme import flush_vertica, init_vertica
from db.vertica.vertica_client import vt_client
from speed_test import DBSpeedTest, VerticaSpeedTest
from test_data.fake_data import data_generator

ch_speed_test = DBSpeedTest(ch_client)
flush_ch(ch_client)
init_ch(ch_client)

vertica_speed_test = VerticaSpeedTest(vt_client.cursor())
flush_vertica(vt_client.cursor())
init_vertica(vt_client.cursor())


def test_insert():
    a = ch_speed_test.test_insert_data(
        "INSERT INTO views VALUES",
        data_generator(True)
    )
    print(f"Write ClickHouse - {a}sec")

    b = vertica_speed_test.test_insert_data(
        'INSERT INTO views (id, user_id, movie_id, viewed_frame, event_time) VALUES (%s,%s,%s,%s,%s)',
        data_generator(False)
    )
    print(f"Write Vertica - {b}sec")

test_insert()

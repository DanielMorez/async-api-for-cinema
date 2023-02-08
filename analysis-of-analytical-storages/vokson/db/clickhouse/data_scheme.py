from clickhouse_driver import Client


def init_ch(client: Client):
    client.execute(
        """
            CREATE TABLE  IF NOT EXISTS  views
                (
                    id UInt64,
                    user_id String,
                    movie_id String,
                    viewed_frame UInt64,
                    event_time DateTime
                )
            ENGINE = MergeTree
            ORDER BY id;
        """
    )


def flush_ch(client: Client):
    client.execute("""DROP TABLE  IF EXISTS  views;""")

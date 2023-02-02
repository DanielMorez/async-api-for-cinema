from clickhouse_driver import Client

from src.core.config import settings

#  Это работает, но если добавляю ON CLUSTER company_cluster
#  таблицы создаются на всех нодах, но чтение из kafka прекращается
#  Пока не понял почему


def create_db(client: Client):
    client.execute("CREATE DATABASE IF NOT EXISTS ugc;")


def create_watch_event_kafka_table(client: Client):
    client.execute(
        """
            CREATE TABLE ugc.watch_events_kafka
                (
                    user_id String,
                    movie_id String,
                    start Datetime,
                    finish Datetime
                )
            ENGINE = Kafka
            SETTINGS
            kafka_broker_list = 'broker:9192',
            kafka_topic_list = '{0}',
            kafka_group_name = 'cluster_events',
            kafka_format = 'JSONEachRow';
        """.format(
            settings.broker.topic
        )
    )


def create_watch_event_target_table(client: Client):
    client.execute(
        """
            CREATE TABLE ugc.watch_events
                    (
                        user_id String,
                        movie_id String,
                        start Datetime,
                        finish Datetime
                    )
                ENGINE = MergeTree() PARTITION BY toYYYYMMDD(start)
                ORDER BY (user_id, movie_id);
        """
    )


def create_watch_event_view(client: Client):
    client.execute(
        """
        CREATE MATERIALIZED VIEW ugc.watch_events_view
        TO ugc.watch_events AS SELECT * FROM ugc.watch_events_kafka;
        """
    )


def drop_tables(client: Client):
    client.execute("DETACH TABLE IF EXISTS ugc.watch_events_kafka;")
    client.execute("DROP TABLE IF EXISTS ugc.watch_events_kafka;")
    client.execute("DROP TABLE IF EXISTS ugc.watch_events;")
    client.execute("DROP TABLE IF EXISTS ugc.watch_events_view;")


if __name__ == "__main__":
    client = Client(host=settings.clickhouse.host)

    drop_tables(client)
    create_db(client)
    create_watch_event_target_table(client)
    create_watch_event_kafka_table(client)
    create_watch_event_view(client)

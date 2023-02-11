import os
import sys

from clickhouse_driver import Client

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from ugc.core.config import settings


def create_db(client: Client):
    client.execute("CREATE DATABASE IF NOT EXISTS ugc;")


def create_watch_event_kafka_table(client: Client):
    client.execute(
        """
            CREATE TABLE ugc.watch_events_kafka
                (
                    user_id String,
                    film_id String,
                    timestamp Datetime
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
                        film_id String,
                        timestamp Datetime
                    )
                ENGINE = MergeTree() PARTITION BY toYYYYMMDD(timestamp)
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


if __name__ == "__main__":
    client = Client(
        host=settings.clickhouse.host,
        port=settings.clickhouse.port,
        user="admin",
        password=settings.clickhouse.password,
    )

    create_db(client)
    create_watch_event_target_table(client)
    create_watch_event_kafka_table(client)
    create_watch_event_view(client)

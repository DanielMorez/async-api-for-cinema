#!/bin/bash
set -e

clickhouse client -n <<-EOSQL

  CREATE DATABASE IF NOT EXISTS shard;

  CREATE DATABASE IF NOT EXISTS replica;

  CREATE TABLE IF NOT EXISTS shard.kafka_progress (
      user_id UUID,
      film_id UUID,
      sec Int32,
      watched Boolean
    ) ENGINE = Kafka SETTINGS kafka_broker_list = 'kafka:29092',
                              kafka_topic_list = 'progress',
                              kafka_group_name = 'group1',
                              kafka_format = 'JSONEachRow';

  CREATE TABLE IF NOT EXISTS shard.progress_store(
      user_id UUID,
      film_id UUID,
      sec Int32,
      watched Boolean
    ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/progress_store', 'replica_progress_1')
    ORDER BY user_id;

  CREATE TABLE IF NOT EXISTS replica.progress_store(
      user_id UUID,
      film_id UUID,
      sec Int32,
      watched Boolean
    ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/progress_store', 'replica_progress_2')
    ORDER BY user_id;

  CREATE TABLE IF NOT EXISTS default.progress_store (
      user_id UUID,
      film_id UUID,
      sec Int32,
      watched Boolean
    ) ENGINE = Distributed('company_cluster', shard, progress_store, rand());

  CREATE MATERIALIZED VIEW IF NOT EXISTS shard.materialized_view_progress_store TO default.progress_store AS
    SELECT user_id, film_id, sec, watched FROM shard.kafka_progress;




CREATE TABLE IF NOT EXISTS shard.kafka_ratings (
    user_id UUID,
    film_id UUID,
    rating Float32,
    deleted Boolean
  ) ENGINE = Kafka SETTINGS kafka_broker_list = 'kafka:29092',
                            kafka_topic_list = 'ratings',
                            kafka_group_name = 'group1',
                            kafka_format = 'JSONEachRow',
                            kafka_max_block_size = 1048576;

CREATE TABLE IF NOT EXISTS shard.ratings_store(
    user_id UUID,
    film_id UUID,
    rating Float32,
    deleted Boolean
  ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/ratings_store', 'replica_ratings_1')
  ORDER BY user_id;


  CREATE TABLE IF NOT EXISTS replica.ratings_store(
      user_id UUID,
      film_id UUID,
      rating Float32,
      deleted Boolean
    ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/ratings_store', 'replica_ratings_2')
    ORDER BY user_id;

  CREATE TABLE IF NOT EXISTS default.ratings_store (
      user_id UUID,
      film_id UUID,
      rating Float32,
      deleted Boolean
    ) ENGINE = Distributed('company_cluster', shard, ratings_store, rand());


CREATE MATERIALIZED VIEW IF NOT EXISTS shard.materialized_view_ratings_store TO default.ratings_store AS
  SELECT user_id, film_id, rating, deleted FROM shard.kafka_ratings;




CREATE TABLE IF NOT EXISTS shard.kafka_bookmarks (
    user_id UUID,
    film_id UUID,
    added Boolean
  ) ENGINE = Kafka SETTINGS kafka_broker_list = 'kafka:29092',
                            kafka_topic_list = 'bookmarks',
                            kafka_group_name = 'group1',
                            kafka_format = 'JSONEachRow';

CREATE TABLE IF NOT EXISTS shard.bookmarks_store(
    user_id UUID,
    film_id UUID,
    added Boolean
  ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/bookmarks_store', 'replica_bookmarks_1')
  ORDER BY user_id;

  CREATE TABLE IF NOT EXISTS replica.bookmarks_store(
    user_id UUID,
    film_id UUID,
    added Boolean
    ) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/bookmarks_store', 'replica_bookmarks_2')
    ORDER BY user_id;

  CREATE TABLE IF NOT EXISTS default.bookmarks_store (
    user_id UUID,
    film_id UUID,
    added Boolean
    ) ENGINE = Distributed('company_cluster', shard, bookmarks_store, rand());

CREATE MATERIALIZED VIEW IF NOT EXISTS shard.materialized_view_bookmarks_store TO default.bookmarks_store AS
  SELECT user_id, film_id, added FROM shard.kafka_bookmarks;


EOSQL

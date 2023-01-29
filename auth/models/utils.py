def create_partition_login_histories(target, connection, **kwargs) -> None:
    """creating partition for login_histories"""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth"."login_histories_2022" PARTITION OF "auth"."login_histories" FOR VALUES FROM (
        '2022-1-1 00:00:00') TO ('2023-1-1 00:00:00') """
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth"."login_histories_2023" PARTITION OF "auth"."login_histories" FOR VALUES FROM (
        '2023-1-1 00:00:00') TO ('2024-1-1 00:00:00') """
    )
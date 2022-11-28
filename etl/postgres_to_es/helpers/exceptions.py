class ElasticsearchNotConnectedError(ConnectionError):
    """ELK client is lazy, throw this `e` if connection was not established."""
    pass


class RedisNotConnectedError(ConnectionError):
    """Redis client is lazy, throw this `e` if connection was not established."""
    pass
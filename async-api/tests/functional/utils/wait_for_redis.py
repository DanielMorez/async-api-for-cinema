import logging

from redis import Redis
from pydantic import RedisDsn

from utils.helpers.backoff import backoff

logger = logging.getLogger()


@backoff()
def health_check_redis(redis_dsn: RedisDsn):
    redis_client = Redis(host=redis_dsn.host)
    logger.info(f"Trying connect to Redis ({redis_dsn})")
    if not redis_client.ping():
        raise Exception("No connection to Redis")

import time
import logging

from redis import Redis
from pydantic import RedisDsn

logger = logging.getLogger(__name__)


def health_check_redis(redis_dsn: RedisDsn):
    redis_client = Redis(host=redis_dsn.host)
    while True:
        logger.info(f"Trying connect to Redis ({redis_dsn})")
        if redis_client.ping():
            break
        time.sleep(1)

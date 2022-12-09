import time
import logging

from redis import Redis

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    redis_client = Redis(
        host='redis_tests'
    )
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
        logger.debug("Trying connect to ES...")

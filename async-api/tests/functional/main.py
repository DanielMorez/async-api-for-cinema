import pytest
import logging

from utils.wait_for_es import health_check_es
from utils.wait_for_redis import health_check_redis

from settings import test_settings


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    health_check_es(test_settings.es_dsn)
    health_check_redis(test_settings.redis_dsn)

    plugins = ("pytest_asyncio", "plugins.common")

    pytest.main(["-x", "src"], plugins=plugins)

import redis
import logging

from pydantic import RedisDsn
from redis import Redis
from redis.typing import KeyT, EncodableT

from helpers.backoff import backoff, reconnect as storage_reconnect
from helpers.exceptions import RedisNotConnectedError
from storage_clients.base_client import BaseClient

logger = logging.getLogger(__name__)


class RedisClient(BaseClient):
    _connection: Redis

    def __init__(self, dsn: RedisDsn, *args, **kwargs):
        super().__init__(dsn, *args, **kwargs)

    @property
    def is_connected(self) -> bool:
        result = True
        try:
            # ping is unsafe
            self._connection and self._connection.ping()
        except redis.exceptions.ConnectionError:
            result = False

        return result

    @backoff()
    def connect(self) -> None:
        self._connection = Redis(
            host=self.dsn.host,
            port=int(self.dsn.port),
            db=self.dsn.path[1:],
            username=self.dsn.user,
            password=self.dsn.password,
            *self.args,
            **self.kwargs,
        )

        if not self.is_connected:
            # client is lazy, need to check it
            raise RedisNotConnectedError(
                f"Connection is not properly established for: `{self.__repr__()}`"
            )

        logger.info(f"Established new connection for: {self}.")

    def reconnect(self) -> None:
        super().reconnect()

    @backoff()
    def close(self) -> None:
        super().close()

    @backoff()
    @storage_reconnect
    def keys(self, pattern, **kwargs) -> list[str]:
        return self._connection.keys(pattern, **kwargs)

    @backoff()
    @storage_reconnect
    def exists(self, *names: KeyT) -> int:
        return self._connection.exists(*names)

    @backoff()
    @storage_reconnect
    def get(self, name: KeyT) -> bytes | None:
        return self._connection.get(name)

    @backoff()
    @storage_reconnect
    def set(self, name: KeyT, value: EncodableT, *args, **kwargs) -> None:
        return self._connection.set(name, value, *args, **kwargs)


if __name__ == '__main__':
    from datetime import datetime
    from contextlib import closing
    from pydantic import BaseSettings
    url = 'redis://127.0.0.1:6379/1'

    class Settings(BaseSettings):
        redis: RedisDsn = url

    settings = Settings()

    with closing(RedisClient(settings.redis)) as r:
        if not r.exists('modified'):
            r.set('modified', datetime.min.strftime('%Y-%m-%d %H:%M:%S.%f'))
        modified_exists = r.exists('modified')
        modified_val = r.get('modified')

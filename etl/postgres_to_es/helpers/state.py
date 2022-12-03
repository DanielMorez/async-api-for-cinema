import abc
import json

from typing import Any

from storage_clients.redis_client import RedisClient


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass

    @abc.abstractmethod
    def is_state_exists(self, key: str) -> None:
        """Проверить наличие состояния в постоянное хранилище"""
        pass


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def exists(self, key: str):
        """Проверить наличие определённого ключа"""
        return self.storage.is_state_exists(key)

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state(key, value)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        return self.storage.retrieve_state(key)


class RedisStorage(BaseStorage):
    def __init__(self, redis_adapter: RedisClient):
        self.redis_adapter = redis_adapter

    def is_state_exists(self, key: str) -> int:
        return self.redis_adapter.exists(key)

    def save_state(self, key, value) -> None:
        self.redis_adapter.set(key, json.dumps(value))

    def retrieve_state(self, key: str) -> dict | None:
        result = self.redis_adapter.get(key)

        if result:
            return json.loads(result)

        return result

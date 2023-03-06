from typing import Any, Dict

import backoff as backoff
import requests as requests

from config import config
from .publisher_abstract import PublisherAbstract


class PublisherApi(PublisherAbstract):
    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError,
                          max_time=config.NOTIFICATION_API_BACKOFF_MAX_TIME)
    def __send_event(self, data):
        response = requests.post(config.NOTIFICATION_API_URL, json=data)
        response.raise_for_status()

    def publish(self, data: Dict[Any, Any]):
        self.__send_event({'event': data})

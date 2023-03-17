from pydantic import AnyUrl
from requests import post
from models.task import Notification


class Publisher:
    def __init__(self, dsn: AnyUrl):
        self._dsn = dsn

    def send_notifications(self, data: Notification) -> bool:
        response = post(self._dsn + "/notifications/send", json=data.dict())
        return response.status_code == 201

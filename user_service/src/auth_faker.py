import http
import json
import logging
from random import choice
from time import sleep

import requests
from core.config import NOTIFICATION_API_REGISTRATION_EVENT_URL

logger = logging.getLogger(__name__)


def send_new_user_id(user_id):
    params = {
        'user_id': user_id,
    }

    response = requests.post(NOTIFICATION_API_REGISTRATION_EVENT_URL, params=params)

    if response.status_code == http.HTTPStatus.CREATED:
        logger.info(f'User {user_id} registered in FakeNetflix')
    else:
        logger.error('Natasha, we broke everything!')


class FakeNewUser:
    raw_user_data = 'fixtures/users.json'
    user_uuids = []

    def get_uuids(self):
        with open(self.raw_user_data, 'r') as file:
            data = json.load(file)
            for user in data['users']:
                self.user_uuids.append(user.get('id'))

    def get_random_uuid(self):
        return choice(self.user_uuids)

    def get_uuid_and_send_event(self):
        self.get_uuids()

        while True:
            user_id = self.get_random_uuid()
            send_new_user_id(user_id)
            sleep(100)


if __name__ == '__main__':
    service = FakeNewUser()
    service.get_uuid_and_send_event()

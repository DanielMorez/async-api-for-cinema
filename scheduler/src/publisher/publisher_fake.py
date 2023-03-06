import json
from pathlib import Path
from pprint import pprint
from typing import Any, Dict

from .publisher_abstract import PublisherAbstract


class PublisherFake(PublisherAbstract):
    def __init__(self):
        self.filename = Path('fixtures') / 'publish_data.json'
        self.data = {
            'items': []
        }
        with open(self.filename, 'w+') as file:
            json.dump(self.data, file)

    def publish(self, data: Dict[Any, Any]):
        print('-' * 60)
        pprint(data)

        self.data['items'].append(data)
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

import logging

from etl.extractors.base import BaseExtractor
from models import Movies

logger = logging.getLogger(__name__)


class PersonExtractor(BaseExtractor):
    def extract(self) -> list[Person]:
        persons: list[Person] = []
        while content := self.get_content():
            persons += [Person(**data) for data in content]
        logger.info(f'Finished extracting persons.')
        return persons

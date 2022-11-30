import logging

from etl.extractors.base import BaseExtractor
from models.person import Person

logger = logging.getLogger(__name__)


class PersonExtractor(BaseExtractor):
    def extract(self) -> list[Person]:
        persons = [Person(**data) for data in self.get_content()]
        logger.info(f'Finished extracting persons.')
        return persons

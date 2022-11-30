import logging

from etl.extractors.base import BaseExtractor
from models.genre import Genre

logger = logging.getLogger(__name__)


class GenreExtractor(BaseExtractor):
    def extract(self) -> list[Genre]:
        genres = [Genre(**data) for data in self.get_content()]
        logger.info(f'Finished extracting genres.')
        return genres

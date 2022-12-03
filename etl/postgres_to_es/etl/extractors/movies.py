import logging

from etl.extractors.base import BaseExtractor
from models.movie import Movie

logger = logging.getLogger(__name__)


class FilmworkExtractor(BaseExtractor):
    def extract(self) -> list[Movie]:
        movies = [Movie(**data) for data in self.get_content()]
        logger.info(f'Finished extracting movies.')
        return movies

import logging

from etl.extractors.base import BaseExtractor
from models import Movie

logger = logging.getLogger(__name__)


class FilmworkExtractor(BaseExtractor):
    def extract(self) -> list[Movie]:
        movies: list[Movie] = []
        while content := self.get_content():
            movies += [Movie(**data) for data in content]
        logger.info(f'Finished extracting movies.')
        return movies

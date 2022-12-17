import logging
from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.queries_params.films import FilmListParams, FilmQueryParams
from db.cache_base import AsyncCacheStorage
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.base_service import BaseService

logger = logging.getLogger(__name__)


class FilmService(BaseService):
    index = "movies"

    async def search(self, params: FilmQueryParams) -> list[Film] | None:
        films = await self._get_films_from_elastic(params)
        return films

    async def get_list(self, params: FilmListParams) -> list[Film] | None:
        films = await self._get_films_from_elastic(params)
        return films

    async def get_by_id(self, film_id: str) -> Film | None:
        film = await self._get_film_from_elastic(film_id)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Film | None:
        try:
            doc = await self.elastic.get(index=self.index, id=film_id)
        except NotFoundError:
            logger.debug(
                f"An error occurred while trying to find film in ES (id: {film_id})"
            )
            return None
        genres = doc["_source"].get("genres")
        if genres and isinstance(genres, str):
            doc["_source"]["genre"] = [
                {"id": item, "name": item} for item in genres.split(" ")
            ]
        return Film(id=doc["_id"], **doc["_source"])

    def _get_body(self, params: FilmListParams | FilmQueryParams) -> dict | None:
        if isinstance(params, FilmListParams):
            body = {"query": {"bool": {"must": []}}}
            if params.genre_id:
                body["query"]["bool"]["must"].append(
                    {
                        "nested": {
                            "path": "genres",
                            "query": {"match": {"genres.id": params.genre_id}},
                        }
                    }
                )
                return body
        elif isinstance(params, FilmQueryParams):
            if params.query:
                body = {"query": {"query_string": {"query": params.query}}}
                return body

    async def _get_films_from_elastic(
        self, params: FilmListParams | FilmQueryParams
    ) -> list[Film] | None:
        try:
            body = self._get_body(params)
            docs = await self.elastic.search(
                index=self.index,
                from_=params.page_size * params.page_number,
                size=params.page_size,
                sort=params.sort,
                body=body,
            )
        except NotFoundError:
            logger.debug("An error occurred while trying to get films in ES)")
            return None
        return [Film(id=doc["_id"], **doc["_source"]) for doc in docs["hits"]["hits"]]


@lru_cache()
def get_film_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(cache, elastic)

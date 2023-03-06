from uuid import UUID

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1.bookmarks.models import Bookmark
from api.v1.rating.models import Rate, UserFilmRating
from api.v1.reviews.models import Review, ReviewLike
from services.base_service import BaseService


class MongoService(BaseService):
    def __init__(self, client: AsyncIOMotorClient, db: str = "ugc", *args, **kwargs):
        super().__init__(client, *args, **kwargs)
        self._db = self._conn[db]

    async def add_bookmark(self, user_id: UUID, film_id: UUID) -> dict:
        collections = self._db["bookmarks"]
        bookmark = Bookmark(user_id=user_id, film_id=film_id).dict()
        doc = collections.find_one(bookmark)
        if doc:
            raise HTTPException(status_code=400, detail="User already added the film to bookmarks")
        bookmark["_id"] = bookmark["id"]
        del bookmark["id"]
        await collections.insert_one(bookmark)
        return bookmark

    async def remove_bookmark(self, user_id: UUID, bookmark_id: UUID) -> None:
        collections = self._db["bookmarks"]
        await collections.delete_one({"_id": bookmark_id, "user_id": user_id})

    async def user_bookmarks(self, user_id) -> list[dict]:
        collections = self._db["bookmarks"]
        cursor = collections.find({"user_id": user_id})
        bookmarks = [doc for doc in await cursor.to_list(100)]
        return bookmarks

    async def rate_film(self, film_id: UUID, user_id: UUID, stars: int):
        collections = self._db["rates"]
        rate = await collections.find_one({"film_id": film_id, "user_id": user_id})
        if rate:
            if rate["stars"] == stars:
                raise HTTPException(status_code=400, detail="User already rated the film")
            new_rate = 0
            previous_stars = rate["stars"]
            rate_id = rate.pop("_id")
            rate["stars"] = stars
            await collections.replace_one({"_id": rate_id}, rate)
        else:
            new_rate = 1
            rate = Rate(film_id=film_id, user_id=user_id, stars=stars).dict()
            previous_stars = 0
            del rate["id"]
            await collections.insert_one(rate)

        # Recalculate user film rating
        collections = self._db["user_film_rating"]
        user_rating = await collections.find_one({"film_id": film_id})
        if not user_rating:
            user_rating = UserFilmRating(film_id=film_id, stars_avg=stars, count=1, stars=stars).dict()
            del user_rating["id"]
            await collections.insert_one(user_rating)
        else:
            user_rating["count"] += new_rate
            user_rating["stars"] += stars - previous_stars
            user_rating["stars_avg"] = user_rating["stars"] / user_rating["count"]
            user_rating_id = user_rating.pop("_id")
            await collections.replace_one({"_id": user_rating_id}, user_rating)

    async def film_rating(self, film_id):
        collections = self._db["user_film_rating"]
        user_rating_film: UserFilmRating = await collections.find_one({"film_id": film_id})
        if not user_rating_film:
            raise HTTPException(status_code=400, detail="The film has not yet received user ratings")
        return user_rating_film

    async def add_review(self, film_id: UUID, user_id: UUID, text: str) -> str:
        collections = self._db["reviews"]
        review = Review(film_id=film_id, user_id=user_id, text=text).dict()
        del review["id"]
        response = await collections.insert_one(review)
        return str(response.inserted_id)

    async def remove_review(self, review_id: str, user_id: UUID) -> None:
        collections = self._db["reviews"]
        if not collections.find_one({"_id": review_id, "user_id": user_id}):
            raise HTTPException(status_code=400, detail="The review does not exist")

        await collections.delete_one({"_id": review_id})

    async def _change_mark_on_review(self, review_id: str, plus: str = "likes", minus: str = "dislikes") -> None:
        collections = self._db["reviews"]
        review = await collections.find_one({"_id": ObjectId(review_id)})
        del review["_id"]
        review[plus] += 1
        review[minus] -= 1
        await collections.replace_one({"_id": ObjectId(review_id)}, review)

    async def _add_mark_on_review(self, review_id: str, field: str = "likes") -> None:
        collections = self._db["reviews"]
        review = await collections.find_one({"_id": ObjectId(review_id)})
        del review["_id"]
        review[field] += 1
        await collections.replace_one({"_id": ObjectId(review_id)}, review)

    async def like_review(self, review_id: str, user_id: UUID) -> None:
        collections = self._db["review_likes"]
        if doc := await collections.find_one({"review_id": review_id, "user_id": user_id}):
            if doc["type"] == "like":
                return
            elif doc["type"] == "dislike":
                doc_id = doc.pop("_id")
                doc["type"] = "like"
                await collections.replace_one({"_id": doc_id}, doc)
                await self._change_mark_on_review(review_id, "likes", "dislikes")
        else:
            await self._add_mark_on_review(review_id, "likes")
            like = ReviewLike(review_id=review_id, user_id=user_id, type="like").dict()
            await collections.insert_one(like)

    async def dislike_review(self, review_id: str, user_id: UUID) -> None:
        collections = self._db["review_likes"]
        if doc := await collections.find_one({"review_id": review_id, "user_id": user_id}):
            if doc["type"] == "dislike":
                return
            elif doc["type"] == "like":
                doc_id = doc.pop("_id")
                doc["type"] = "dislike"
                await collections.replace_one({"_id": doc_id}, doc)
                await self._change_mark_on_review(review_id, "dislikes", "likes")
        else:
            await self._add_mark_on_review(review_id, "dislikes")
            like = ReviewLike(review_id=review_id, user_id=user_id, type="like").dict()
            await collections.insert_one(like)

    async def reviews(self, film_id: UUID, sort: str = "created_at") -> list[dict]:
        collections = self._db["reviews"]
        cursor = collections.find({"film_id": film_id})
        reviews = [r for r in await cursor.to_list(100)]
        return reviews

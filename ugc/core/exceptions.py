from abc import ABC, abstractmethod
from http import HTTPStatus

from fastapi import HTTPException


class APIException(HTTPException, ABC):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, status_code: int = status_code):
        super(APIException, self).__init__(status_code, self.detail)

    @property
    @abstractmethod
    def detail(self):
        pass


class UserAlreadyRated(APIException):
    detail = "User already rated the film"


class NoFilmRating(APIException):
    detail = "The film has not yet received user ratings"


class ReviewDoesntExist(APIException):
    detail = "The review does not exist"

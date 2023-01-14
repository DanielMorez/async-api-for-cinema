import time
from functools import wraps
from http import HTTPStatus

from flask import jsonify
from flask_jwt_extended import get_jwt

from db import cache_storage

pipeline = cache_storage.pipeline()


def block_token(token: str, expire_time: int) -> None:
    left_time = int(expire_time - time.time())
    if left_time > 0:
        pipeline.set(token, "", ex=left_time)
        pipeline.execute()


def check_if_token_in_blacklist():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            payload = get_jwt()
            token = payload["jti"]
            if cache_storage.get(token):
                response = jsonify({"msg": "Invalid token"})
                response.status = HTTPStatus.FORBIDDEN
                return response
            return func(*args, **kwargs)

        return decorator

    return wrapper

from functools import wraps
from http import HTTPStatus

from flask import abort
from flask_jwt_extended import get_jwt, get_jwt_identity

from db import cache_storage
from models.user import User


def roles_required(*roles):
    def wrapper(view_function):
        @wraps(view_function)
        def decorator(*args, **kwargs):
            payload = get_jwt()
            token = payload["jti"]
            is_block_token = cache_storage.get(token)

            user_id = get_jwt_identity()
            user = User.find_by_id(user_id)

            # including JWT blacklist verification
            if is_block_token or not user:
                abort(HTTPStatus.FORBIDDEN, {"msg": "Invalid token"})

            if user.is_superuser:
                return view_function(*args, **kwargs)

            if user.has_roles(*roles):
                return view_function(*args, **kwargs)

            abort(HTTPStatus.FORBIDDEN, {"msg": "No access permissions"})

        return decorator

    return wrapper

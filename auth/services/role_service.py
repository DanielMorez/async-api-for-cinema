import logging

from http import HTTPStatus
from sqlalchemy.exc import DataError
from flask import abort

from models.role import Role
from utils.models import get_or_create

logger = logging.getLogger(__name__)


def get_role_or_error(role_id):
    try:
        role = Role.find_by_id(role_id)
    except DataError:
        abort(HTTPStatus.BAD_REQUEST, "Invalid id")
    else:
        if not role:
            abort(HTTPStatus.BAD_REQUEST, f"Role with id {role_id} does not exist")
        return role


class RoleService:
    @classmethod
    def create_role(cls, name) -> (Role, bool):
        instance, created = get_or_create(Role, name=name)
        return instance, created

    @classmethod
    def get_roles(cls) -> (str,):
        roles = tuple(role.as_dict for role in Role.query.all())
        return roles

    @classmethod
    def update(cls, role_id, name) -> None:
        role = get_role_or_error(role_id)
        role.name = name
        role.save()

    @classmethod
    def delete(cls, role_id) -> None:
        role = get_role_or_error(role_id)
        role.delete()

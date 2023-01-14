import logging
from http import HTTPStatus
from uuid import UUID

from models.role import Role
from utils.models import get_or_create

logger = logging.getLogger(__name__)


class RoleService:
    @classmethod
    def create_role(cls, name: str) -> (Role, bool):
        instance, created = get_or_create(Role, name=name)
        return instance, created

    @classmethod
    def update_role(cls, role_id: UUID, name: str) -> (dict, HTTPStatus):
        role = Role.find_by_id(role_id)
        role.update(Role.id, name)
        return {"msg": "Role was successfully updated"}, HTTPStatus.OK

    @classmethod
    def remove_role(cls, role_id: UUID) -> (dict, HTTPStatus):
        role = Role.find_by_id(role_id)
        role.delete(Role.id)
        return {"msg": "Role was successfully deleted"}, HTTPStatus.OK

import logging
from http import HTTPStatus
from uuid import UUID

from models.role import Role
from utils.models import get_or_create

logger = logging.getLogger(__name__)


class RoleService:
    @classmethod
    def create_role(
        cls, name: str, can_create_update: bool, can_read: bool, can_delete: bool
    ) -> (Role, bool):
        instance, created = get_or_create(
            Role,
            name=name,
            can_create_update=can_create_update,
            can_read=can_read,
            can_delete=can_delete,
        )
        return instance, created

    @classmethod
    def get_role(cls, name):
        instance = Role.query.filter_by(name=name).first()
        if not instance:
            return instance, False
        return instance, True

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

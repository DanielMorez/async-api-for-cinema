from http import HTTPStatus
from uuid import UUID

from models.role import UserRoles
from utils.models import get_or_create


class UserRoleService:
    @classmethod
    def remove_users_role(cls, user_id: UUID, role_id: UUID) -> (dict, HTTPStatus):
        userRoles = UserRoles.find_by_ids(user_id, role_id)
        userRoles.delete(userRoles.id)
        return {"msg": "Role was successfully deleted from user"}, HTTPStatus.OK

    @classmethod
    def create_user_roles(cls, user_id: UUID, role_id: UUID) -> (UserRoles, bool):
        instance, created = get_or_create(UserRoles, user_id=user_id, role_id=role_id)
        return instance, created

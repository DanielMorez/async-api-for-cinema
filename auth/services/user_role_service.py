from http import HTTPStatus
from uuid import UUID

from flask import abort

from services.user_service import get_user_or_error
from services.role_service import get_role_or_error


class UserRoleService:
    @classmethod
    def set_user_role(cls, user_id: UUID, role_id: UUID) -> list:
        user = get_user_or_error(user_id)
        role = get_role_or_error(role_id)

        if role not in user.roles:
            user.roles.append(role)
            user.save()
        return [r.as_dict for r in user.roles]

    @classmethod
    def remove_user_role(cls, user_id: UUID, role_id: UUID) -> dict:
        user = get_user_or_error(user_id)
        role = get_role_or_error(role_id)
        if role in user.roles:
            user.roles.remove(role)
            user.save()
            return role.as_dict
        else:
            abort(HTTPStatus.BAD_REQUEST, "User already does not have the role")

    @classmethod
    def get_user_roles(cls, user_id: UUID) -> list:
        user = get_user_or_error(user_id)
        roles = [role.as_dict for role in user.roles]
        return roles

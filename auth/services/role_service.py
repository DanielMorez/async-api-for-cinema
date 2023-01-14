import logging

from models.role import Role
from utils.models import get_or_create

logger = logging.getLogger(__name__)


class RoleService:
    @classmethod
    def create_role(cls, name) -> (Role, bool):
        instance, created = get_or_create(Role, name=name)
        return instance, created


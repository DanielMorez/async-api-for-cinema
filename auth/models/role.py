import uuid

from sqlalchemy.dialects.postgresql import UUID
from db import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name: str):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        "user_id", UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE")
    )
    role_id = db.Column(
        "role_id", UUID(as_uuid=True), db.ForeignKey("roles.id", ondelete="CASCADE")
    )

    def __init__(self, user_id: UUID, role_id: UUID):
        self.user_id = user_id
        self.role_id = role_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, user_roles_id: UUID) -> None:
        return cls.query.filter_by(id=user_roles_id).delete()

    @classmethod
    def find_by_ids(cls, user_id: UUID, role_id: UUID) -> "user_roles":
        return cls.query.filter_by(user_id=user_id, role_id=role_id).first()


class RolesRequirements(db.Model):
    __tablename__ = "roles_requirements"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    role_id = db.Column(
        "role_id", UUID(as_uuid=True), db.ForeignKey("roles.id", ondelete="CASCADE")
    )
    can_create = db.Column(db.Boolean(), default=False)
    can_read = db.Column(db.Boolean(), default=False)
    can_update = db.Column(db.Boolean(), default=False)
    can_delete = db.Column(db.Boolean(), default=False)

    def __init__(self, role_id: UUID):
        self.role_id = role_id

    def save(self):
        db.session.add(self)
        db.session.commit()

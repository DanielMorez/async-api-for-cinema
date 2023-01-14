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

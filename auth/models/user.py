import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType
from werkzeug.security import (
    generate_password_hash
)

from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = db.Column(EmailType, unique=True, nullable=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, login, password, email=None):
        self.login = login
        self.password = password
        self.email = email

    def save(self):
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.login or self.email}>"

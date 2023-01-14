import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import EmailType
from werkzeug.security import check_password_hash, generate_password_hash

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

    def save(self) -> None:
        self.password = generate_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    def set_password(self, password: str) -> None:
        self.password = password
        self.save()

    def set_login(self, login: str) -> None:
        self.login = login
        db.session.commit()

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, user_id: UUID) -> "User":
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_login(cls, login) -> "User":
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_email(cls, email) -> "User":
        return cls.query.filter_by(email=email).first()

    def __repr__(self):
        return f"<User {self.login or self.email}>"

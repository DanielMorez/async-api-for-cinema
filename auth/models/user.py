import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import EmailType
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.mixins import ModelMixin


class User(db.Model, ModelMixin):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    email = db.Column(EmailType, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)

    active = db.Column(db.Boolean(), default=False)
    is_superuser = db.Column(db.Boolean(), default=False)

    roles = db.relationship("Role", secondary=f"{db.metadata.schema}.user_roles")

    def __init__(self, login, password, email=None):
        self.login = login
        self.password = password
        self.email = email

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        new_password_hash = generate_password_hash(password)
        self._password = new_password_hash

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def set_password(self, password: str) -> None:
        self.password = password
        self.save()

    def set_login(self, login: str) -> None:
        self.login = login
        db.session.commit()

    def verify_password(self, password) -> bool:
        return check_password_hash(self._password, password)

    def get_roles_names(self) -> tuple:
        roles_names = tuple(role.name for role in self.roles)
        return roles_names

    def has_roles(self, *requirements):
        roles_names = self.get_roles_names()
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                for role_name in roles_names:
                    if role_name in requirement:
                        return True
            else:
                if requirement in roles_names:
                    return True
        return False

    @classmethod
    def find_by_id(cls, user_id: UUID) -> "User":
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def find_by_login(cls, login) -> "User":
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_email(cls, email) -> "User":
        return cls.query.filter_by(email=email).first()

    @property
    def as_dict(self):
        data = super().as_dict
        del data["password"]
        del data["is_superuser"]
        del data["active"]
        return data

    def __repr__(self):
        return f"<User {self.login or self.email}>"

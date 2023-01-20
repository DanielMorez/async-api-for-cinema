import uuid
import datetime

from flask_sqlalchemy.query import Query
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref

from db import db
from models.mixins import ModelMixin


class LoginHistory(ModelMixin, db.Model):
    __tablename__ = "login_histories"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_agent = db.Column(db.String, nullable=True)
    device = db.Column(db.String, nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False
    )

    user = db.relationship("User", backref=backref("login_histories", uselist=False))

    def __init__(self, user_id: UUID, user_agent=None, device=None):
        self.user_id = user_id
        self.user_agent = user_agent
        self.device = device

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_sessions(cls, user_id: UUID) -> Query:
        return cls.query.filter_by(user_id=user_id)

    def __repr__(self):
        return f"<Login at {self.created_at.strftime('%d/%m/%Y, %H:%M:%S')}>"

import uuid
import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref

from config import settings
from db import db


class LoginHistory(db.Model):
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
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    token_updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    jti_access_token = db.Column(UUID(as_uuid=True), nullable=False)
    jti_refresh_token = db.Column(UUID(as_uuid=True), nullable=False)

    user = db.relationship("User", backref=backref("login_histories", uselist=False))

    def __init__(
        self,
        user_id: UUID,
        jti_access_token: UUID,
        jti_refresh_token: UUID,
        user_agent=None,
        device=None,
    ):
        self.user_id = user_id
        self.user_agent = user_agent
        self.device = device
        self.jti_access_token = jti_access_token
        self.jti_refresh_token = jti_refresh_token

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_sessions(cls, user_id: UUID):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def save_token_updated_at(cls, token: UUID):
        login_histories = cls.query.filter_by(jti_refresh_token=token).first()
        if login_histories:
            login_histories.token_updated_at = datetime.datetime.utcnow()
            login_histories.save()
        return

    @classmethod
    def get_sessions_with_date(cls, user_id: UUID):
        return cls.query.filter(
            cls.user_id == user_id,
            cls.token_updated_at
            >= datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.jwt_refresh_token_expires),
        )

    def serialize(self):
        return {
            "user_agent": self.user_agent,
            "device": self.device,
            "created_at": self.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
        }

    def __repr__(self):
        return f"<Login at {self.created_at.strftime('%d/%m/%Y, %H:%M:%S')}>"

import uuid

from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.mixins import ModelMixin


class SocialAccount(ModelMixin, db.Model):
    __tablename__ = "social_accounts"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("social_accounts", lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint("social_id", "social_name", name="social_pk"),)

    def __init__(self, user_id: UUID, social_id=str, social_name=str):
        self.user_id = user_id
        self.social_id = social_id
        self.social_name = social_name

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, social_id: str) -> "SocialAccount":
        return cls.query.filter_by(social_id=social_id).first()

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"

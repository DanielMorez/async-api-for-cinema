from sqlalchemy.orm import declared_attr


class ModelMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

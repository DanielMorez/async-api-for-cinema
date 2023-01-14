import abc

from flask_sqlalchemy.model import DefaultMeta


class AbstractModel(DefaultMeta):
    @abc.abstractmethod
    def save(self) -> None:
        pass


def get_or_create(model_class: AbstractModel, **kwargs) -> (AbstractModel, bool):
    if instance := model_class.query.filter_by(**kwargs).first():
        return instance, False
    instance = model_class(**kwargs)
    instance.save()
    return instance, True

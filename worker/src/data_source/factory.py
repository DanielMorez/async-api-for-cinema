from .abstract import DataSourceAbstract
from .fake import DataSourceFake
from .rabbitmq import DataSourceRabbitMQ


class InvalidEmailSenderType(Exception):
    """Invalid email sender type in factory."""


class DataSourceFactory:
    @staticmethod
    def get(object_type: str) -> DataSourceAbstract:
        if object_type == 'fake':
            return DataSourceFake()
        elif object_type == 'rabbitmq':
            return DataSourceRabbitMQ()
        raise InvalidEmailSenderType(f'Invalid data source type {object_type}')

import typing


class NotFoundError(Exception):
    def __init__(self, error: typing.Optional[str] = None):
        self.error = error

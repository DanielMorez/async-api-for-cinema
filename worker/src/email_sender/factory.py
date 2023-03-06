from .abstract import EmailSenderAbstract
from .fake import EmailSenderFake
from .sendgrid import EmailSenderSendgrid


class InvalidEmailSenderType(Exception):
    """Invalid email sender type in factory."""


class EmailSenderFactory:
    @staticmethod
    def get_sender(sender_type: str) -> EmailSenderAbstract:
        if sender_type == 'fake':
            return EmailSenderFake()
        elif sender_type == 'sendgrid':
            return EmailSenderSendgrid()
        raise InvalidEmailSenderType(f'Invalid email sender type {sender_type}')

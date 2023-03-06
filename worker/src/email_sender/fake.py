import time

from .abstract import EmailSenderAbstract


class EmailSenderFake(EmailSenderAbstract):
    def send(self, address: str, subject: str, data: str):
        print('-' * 60)
        print(f'New email to {address}')
        print(f'Subject: {subject}')
        print(f'{data}')
        print()
        time.sleep(0.5)

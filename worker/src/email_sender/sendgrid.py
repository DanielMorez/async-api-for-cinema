import logging

from config import config
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .abstract import EmailSenderAbstract


class EmailSenderSendgrid(EmailSenderAbstract):
    def send(self, address: str, subject: str, data: str):
        message = Mail(
            from_email=config.SENDGRID_FROM_EMAIL,
            to_emails=address,
            subject=subject,
            plain_text_content=data)
        try:
            sg = SendGridAPIClient(config.SENDGRID_API_KEY)
            response = sg.send(message)

        except HTTPError:
            logging.exception('Error send email')
        else:
            if response.status_code != 202:
                logging.error(f'Error send email, {response}')

import ssl
import smtplib

from storage.models import Template
from config import settings
from email.message import EmailMessage


def send_common_email(emails: list[str], template: Template):
    smtp = settings.smtp

    context = ssl._create_unverified_context()

    message = EmailMessage()
    message["From"] = smtp.email
    message["To"] = ",".join(emails)
    message["Subject"] = template.subject
    message.set_content(template.content)

    with smtplib.SMTP_SSL(smtp.server, smtp.port, context=context) as server:
        server.login(smtp.email, smtp.password)
        server.sendmail(message["From"], emails, message.as_string())

    return True

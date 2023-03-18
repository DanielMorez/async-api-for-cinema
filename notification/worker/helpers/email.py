import ssl
import smtplib

from jinja2 import Template, Environment

from auth.models import User
from storage.models import Template
from config import settings
from email.message import EmailMessage


context = ssl._create_unverified_context()
smtp = settings.smtp


def send_personal_email(user: User, template: Template):
    message = EmailMessage()
    message["From"] = smtp.email
    message["To"] = user.email
    message["Subject"] = template.subject
    environment = Environment()
    content = template.content
    content = environment.from_string(content)
    username = user.first_name or user.login
    message.set_content(content.render(username=username))

    with smtplib.SMTP_SSL(smtp.server, smtp.port, context=context) as server:
        server.login(smtp.email, smtp.password)
        server.sendmail(message["From"], user.email, message.as_string())

    return True


def send_common_email(emails: list[str], template: Template):
    message = EmailMessage()
    message["From"] = smtp.email
    message["To"] = ",".join(emails)
    message["Subject"] = template.subject
    message.set_content(template.content)

    with smtplib.SMTP_SSL(smtp.server, smtp.port, context=context) as server:
        server.login(smtp.email, smtp.password)
        server.sendmail(message["From"], emails, message.as_string())

    return True

import smtplib
from email.message import EmailMessage

from config import config

smtp_class = smtplib.SMTP_SSL if config.SMTP_PORT == 465 else smtplib.SMTP


def send_mail(to, subject, content):
    try:
        with smtp_class(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)

            message = EmailMessage()
            message[
                "From"
            ] = (
                config.SMTP_USER
            )  # Вне зависимости от того, что вы укажете в этом поле, Gmail подставит ваши данные
            message["To"] = ",".join([to])  # Попробуйте отправить письмо самому себе
            message["Subject"] = subject

            # Для отправки HTML-письма нужно вместо метода `set_content` использовать `add_alternative` с subtype "html",
            # Иначе пользователю придёт набор тегов вместо красивого письма
            message.add_alternative(content, subtype="html")
            server.sendmail(config.SMTP_USER, [to], message.as_string())
    except Exception:
        return False, "exception"
    else:
        return True, "ok"

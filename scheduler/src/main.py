"""
Этот сервис вычитывает уведомления из базы, рендерит шаблон
и отправляет сообщение по указанному каналу.
"""

import logging
from time import sleep
from typing import Optional

import db
import email_sender
from config import config
from jinja2 import Environment, FileSystemLoader, Template

logging.basicConfig(level="DEBUG" if config.DEBUG else "INFO")
logger = logging.getLogger(__name__)

email_api = None


def send_email(target, subject, body):
    return email_sender.send_mail(target, subject, body)


channel_to_sender = {"email": send_email}


def send_notification(
    target: str, channel: str, subject: str, body: str
) -> tuple[bool, str]:
    logger.debug(f"sending notification to {target=}, {channel=} with {subject=}")
    sender = channel_to_sender[channel]
    logger.debug(f"{sender=}")
    return sender(target, subject, body)


def init_scheduler():
    global email_api
    db.init()


def render_template(template_string: str, template_data: dict) -> str:
    logger.debug(
        f"render_template: got {template_string=} with params: {template_data=}"
    )
    template = Template(template_string)
    rendered = template.render(template_data)
    logger.debug(f"rendered: {rendered}")
    return rendered


def drop_or_resend_notification(notification):
    logger.debug(f"drop or resend: {notification=}")
    raise NotImplementedError


def main():
    init_scheduler()
    logger.debug(f"Scheduler started")
    while True:
        chunk = db.read_notifications_chunk()
        logger.debug(f"Read {len(chunk)} notifications from db")
        logger.debug(f"received chunk: {chunk=}")
        for notification in chunk:
            logger.debug(f"{notification=} from chunk")
            logger.debug(
                f"Processing notification {notification['scheduled_datetime']}:{notification['id']}"
                f" to {notification['email']}"
                # f" via {notification['channel']}"
            )

            template = db.get_template_by_id(notification["template_id"])
            rendered_body = render_template(
                template["html"], notification["template_data"]
            )
            rendered_subject = render_template(
                template["subject"], notification["template_data"]
            )
            ok, status = send_notification(
                notification["email"], "email", rendered_subject, rendered_body
            )
            if not ok:
                db.drop_or_resend_notification(notification["id"])
            else:
                db.mark_notification_as_sent(notification["id"])
        sleep(config.POLL_INTERVAL)


if __name__ == "__main__":
    main()

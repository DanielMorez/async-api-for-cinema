import logging
from typing import Any, Dict, Optional

from jinja2 import Environment
from psycopg2 import sql

from context_collector.factory import ContextCollectorFactory, NotFoundException
from db.postgres import Postgres
from email_sender.abstract import EmailSenderAbstract
from models import Template, Event
from user_service_client.client_abstract import UserInfo, UserServiceClientAbstract


class Worker:
    def __init__(self, postgres: Postgres,
                 user_service_client: UserServiceClientAbstract,
                 email_sender: EmailSenderAbstract):
        self.postgres = postgres
        self.user_service_client = user_service_client
        self.email_sender = email_sender

    def __get_template(self, template_id: int) -> Optional[Template]:
        query = sql.SQL("""
        select title, code, template, subject from notification_templates where id = %(id)s
                           """)

        items = self.postgres.exec(query, {'id': template_id})
        if len(items) != 1:
            logging.error(f'Error get template with id={template_id}')
            return None

        return Template(**items[0])

    def __gather_context(self, user_id: str, template_code: str) -> Dict[Any, Any]:
        context_collector_factory = ContextCollectorFactory(self.user_service_client)
        try:
            context_collector = context_collector_factory.create(template_code)
        except NotFoundException:
            # no context collector for this template type. Skip
            return {}
        return context_collector.collect(user_id)

    def __build_from_template(self, template: Template, user_info: UserInfo, context: Dict[Any, Any]) -> str:
        user_context = user_info.dict(include={'first_name', 'last_name'})
        context.update(user_context)

        env = Environment(autoescape=True)
        template_obj = env.from_string(template.template)
        return template_obj.render(**context)

    def is_can_send_promo(self, event: Event, user_info: UserInfo) -> bool:
        """Проверяет, можем ли мы отсылать это сообщение пользователю."""
        if event.is_promo and not user_info.promo_agree:
            return False
        return True

    def handle_user(self, user_info: UserInfo, event: Event, template: Template):
        """Готовит сообщение для пользователя и отправляет его."""
        if not self.is_can_send_promo(event, user_info):
            logging.info('User is not agreed to receive promo messages. Skip')
            return

        context = self.__gather_context(user_info.id, template.code)
        context.update(event.context)

        item_to_send = self.__build_from_template(template, user_info, context)
        self.email_sender.send(user_info.email, template.subject, item_to_send)

    def do(self, event: Event):
        """Обрабатывает задание на отправку уведомлений пользователям."""
        logging.debug('Do work')

        template = self.__get_template(event.template_id)
        if not template:
            return
        for user_id in event.user_ids:
            user_info = self.user_service_client.get_user(user_id)
            if not user_info:
                logging.error(f'User {user_id} not found')
                continue

            self.handle_user(user_info, event, template)

        logging.info(f'Handled {len(event.user_ids)} notifications')

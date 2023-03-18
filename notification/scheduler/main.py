import time
from contextlib import closing

from psycopg2.extras import RealDictCursor

from auth.client import AuthClient
from config import settings
from etl.extractor import TaskExtractor
from models.task import Notification
from publisher.client import Publisher
from storage.postgres import PostgresClient


def scheduler() -> None:
    with closing(PostgresClient(settings.pg_dsn, cursor_factory=RealDictCursor)) as pg_conn:
        pg_conn: PostgresClient

        task_extractor = TaskExtractor(pg_conn)
        data_enrichment = AuthClient(settings.auth_api)
        notification_loader = Publisher(settings.notification_api)

        while True:
            tasks = task_extractor.extract_tasks(settings.extract_chunk)
            for task in tasks:
                notification = Notification(
                    type=task.type,
                    template_id=task.template_id,
                    user_ids=[],
                    context=task.context
                )

                if user_ids := task.context.get("user_ids"):
                    if isinstance(user_ids, list):
                        notification.user_ids += user_ids

                if user_filters := task.context.get("user_filters"):
                    user_ids = data_enrichment.get_users_with_filter(user_filters)
                    notification.user_ids += user_ids

                if notification.user_ids:
                    is_sent = notification_loader.send_notifications(
                        notification
                    )

                    status = "done" if is_sent else "canceled"
                    task_extractor.set_task_status(task.id, status)
                else:
                    task_extractor.set_task_status(task.id, "canceled")

            time.sleep(settings.time_interval)


if __name__ == "__main__":
    scheduler()

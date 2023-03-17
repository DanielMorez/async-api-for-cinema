from uuid import UUID

from models.task import Task
from storage.postgres import PostgresClient
from queries import change_task_status, extract_tasks


class TaskExtractor:
    def __init__(self, pg_conn: PostgresClient):
        self._conn = pg_conn

    def extract_tasks(self, extract_chunk) -> list[Task]:
        with self._conn.cursor() as cursor:
            cursor.execute(
                extract_tasks.QUERY.format(
                    extract_chunk=extract_chunk
                )
            )
            data = [Task(**i) for i in cursor.fetchmany(extract_chunk)]
        return data

    def set_task_status(self, task_id: UUID, status: str) -> None:
        with self._conn.cursor() as cursor:
            cursor.execute(
                change_task_status.QUERY.format(
                    status=status,
                    task_id=str(task_id)
                )
            )

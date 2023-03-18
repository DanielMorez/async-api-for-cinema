from storage.models import Template
from storage.postgres import PostgresClient
from storage.postgres_queries import template


class PostgresService:
    def __init__(self, pg_conn: PostgresClient):
        self._conn = pg_conn

    def get_template_by_id(self, template_id: int) -> Template:
        with self._conn.cursor() as cursor:
            cursor.execute(
                template.QUERY.format(
                    template_id=template_id
                )
            )
            row = cursor.fetchmany(1)
            if row:
                template_instance = Template(**row[0])
            else:
                template_instance = None
        return template_instance

from typing import Any, Dict, Optional

import backoff as backoff
import psycopg2
from config import config
from psycopg2 import sql
from psycopg2.extras import DictCursor


class Postgres():
    @backoff.on_exception(backoff.expo, psycopg2.OperationalError, max_time=config.POSTGRES_BACKOFF_MAX_TIME)
    def exec(self, template: sql.SQL, args: Dict[str, Any]) -> Optional[Dict]:
        """Выполнить запрос в базу и вернуть результат, если возможно."""
        with psycopg2.connect(dsn=config.postgres_dsn, cursor_factory=DictCursor) as connection:
            with connection.cursor() as cursor:
                cursor.execute(template, args)
                try:
                    results = [dict(item) for item in cursor.fetchall()]
                except psycopg2.ProgrammingError:
                    results = None

        return results

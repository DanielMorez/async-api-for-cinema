DROP_ALL_TABLES = """
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
"""

INSERT = """
    INSERT INTO public.{table}{columns} VALUES
"""

SELECT_WHERE = """
    SELECT * FROM public.{table} WHERE 
"""

DELETE_WHERE = """
    DELETE FROM public.{table} WHERE 
"""

PUBLIC = "CREATE SCHEMA IF NOT EXISTS public;"

BOOKMARKS = """
    CREATE TABLE IF NOT EXISTS bookmarks(
        id uuid NOT NULL,
        user_id uuid NOT NULL,
        film_id uuid NOT NULL,
        PRIMARY KEY (id)
    );
"""

CREATE_TABLES = [PUBLIC, BOOKMARKS]

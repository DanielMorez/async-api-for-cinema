def init_vertica(cursor):
    cursor.execute(
        """
        CREATE TABLE views (
            id INTEGER NOT NULL,
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        );
        """
    )


def flush_vertica(cursor):
    cursor.execute(
        """
            DROP TABLE IF EXISTS views;
            """
    )

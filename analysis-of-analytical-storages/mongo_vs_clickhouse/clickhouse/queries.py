DROP_DB = "DROP DATABASE IF EXISTS ugc_db"

CREATE_DB = "CREATE DATABASE IF NOT EXISTS ugc_db"

BOOKMARKS = """
    CREATE TABLE IF NOT EXISTS ugc_db.bookmarks
        (
            id UUID,
            user_id UUID,
            film_id UUID
        )
    ENGINE = MergeTree
    PRIMARY KEY id
"""

LIKES = """
    CREATE TABLE IF NOT EXISTS ugc_db.likes
        (
            id UUID,
            user_id UUID,
            film_id UUID,
            stars UInt8
        )
    ENGINE = MergeTree
    PRIMARY KEY id
"""

INSERT_BOOKMARKS = """
    INSERT INTO ugc_db.bookmarks (id, user_id, film_id)
    VALUES
"""

INSERT_LIKES = "INSERT INTO ugc_db.likes (id, user_id, film_id, stars) VALUES"

SELECT_BOOKMARKS = "SELECT (id, user_id, film_id) FROM ugc_db.bookmarks WHERE user_id = %(user_id)s"

SELECT_USERS = "SELECT DISTINCT user_id FROM ugc_db.{table}"

SELECT_FILMS = "SELECT user_id, film_id FROM ugc_db.{table}"

DELETE_BOOKMARKS = """
    ALTER TABLE ugc_db.bookmarks
    DELETE
    WHERE (user_id = %(user_id)s) AND (film_id = %(film_id)s)
"""

AGGREGATE = """
    SELECT {group_field}, avg({aggregate_field}) as avg_val
    FROM ugc_db.{table} 
    GROUP BY {group_field}
    ORDER BY avg_val DESC
    LIMIT {limit}
"""

INSERT_QUERIES = {
    "bookmarks": INSERT_BOOKMARKS,
    "likes": INSERT_LIKES,
}

FIND_QUERIES = {
    "bookmarks": SELECT_BOOKMARKS,
}

DELETE_QUERIES = {
    "bookmarks": DELETE_BOOKMARKS,
}

SELECT_QUERIES = {
    "bookmarks": SELECT_USERS,
}
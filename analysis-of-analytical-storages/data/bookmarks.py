import uuid
import logging

from random import choice

from data.common import random_users, random_films, read_csv

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def random_bookmarks(users: list[str], films: list[str], amount: int) -> list[tuple[str, str, str]]:
    return [(str(uuid.uuid4()), choice(users), choice(films)) for _ in range(amount)]


def create_test_bookmark_csv(file_name: str, row_amount: int, batch_count: int = 50_000) -> None:
    users = random_users(100_000)
    films = random_films(10_000)

    with open(file_name, "w") as file:
        file.write("_id,user_id,film_id")
        for _ in range(0, row_amount, batch_count):
            bookmarks = random_bookmarks(users, films, batch_count)
            rows = "\n" + "\n".join(",".join(i) for i in bookmarks)
            file.write(rows)
            logger.info(f"Successful inserted {batch_count} of bookmark")


if __name__ == "__main__":
    from os.path import isfile

    COUNT = 100_000
    CSV_FILE = "bookmarks.csv"

    if not isfile(CSV_FILE):
        create_test_bookmark_csv(CSV_FILE, COUNT)

    for batch in read_csv(CSV_FILE):
        logger.info(f"Read {len(batch)} of rows. Example of row: {choice(batch)}.")

import csv
import uuid
from typing import Iterable


USERS = []
FILMS = []


def random_users(amount: int) -> list[str]:
    return [str(uuid.uuid4()) for _ in range(amount)]


def random_films(amount: int) -> list[str]:
    return [str(uuid.uuid4()) for _ in range(amount)]


def read_csv(file_name: str, dict_reader: bool = False, batch_count: int = 250_000) -> Iterable[list]:
    with open(file_name) as file_csv:
        if dict_reader:
            csv_reader = csv.DictReader(file_csv)
        else:
            csv_reader = csv.reader(file_csv)
            csv_reader.__next__()  # escape header columns

        temp_batch = []
        for line in csv_reader:
            row = line
            if isinstance(row, dict):
                for key in row.keys():
                    if row[key].isdigit():
                        row[key] = int(row[key])
            if isinstance(row, list):
                for i in range(len(row)):
                    if row[i].isdigit():
                        row[i] = int(row[i])

            temp_batch.append(row)

            if len(temp_batch) >= batch_count:
                yield temp_batch
                temp_batch = []

        if len(temp_batch) > 0:
            yield temp_batch

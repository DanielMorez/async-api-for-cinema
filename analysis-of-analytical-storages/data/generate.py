import csv
import random
from datetime import datetime

COUNT = 1000000
CSV_FILE = "test.csv"


#user_ids = [str(x) for x in range(10000)]
#movie_ids = [str(x) for x in range(10000)]


def generate_data_from_file(convert=True, batch_count=50000):
    with open(CSV_FILE) as test_csv:
        batch = []
        for line in csv.reader(test_csv):
            row = (
                [
                    int(line[0]),
                    int(line[1]),
                    int(line[2]),
                    int(line[3]),
                    int(line[4]),
                    int(line[5]),
                    datetime.strptime(line[6], "%Y-%m-%d %H:%M:%S"),
                ]
                if convert
                else line
            )

            batch.append(row)

            if len(batch) >= batch_count:
                yield batch
                batch = []

        if len(batch) > 0:
            yield batch


def generate_row() -> tuple:
    return (
        random.randint(1, 10000),
        random.randint(1, 10000),
        random.randint(0, 10),
        random.randint(0, 180),
        random.randint(0, 1),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


def create_fake_data():
    with open(CSV_FILE, mode="w") as f:
#        f.write("Id,user_id,movie_id,stars,viewed_frame,likes,event_time\n")
        for i in range(COUNT):
            f.write("{},{},{},{},{},{},{}\n".format(i + 1, *generate_row()))


if __name__ == "__main__":
    create_fake_data()
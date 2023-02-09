import os
import csv
import random
from datetime import datetime


COUNT = 100000
CSV_FILE="test.csv"
user_ids = [str(x) for x in range(10000)]
movie_ids = [str(x) for x in range(10000)]


def data_generator(convert=True, batch_count=50000):
    with open(os.path.join("test_data", CSV_FILE)) as test_csv:
        batch = []
        for line in csv.reader(test_csv):

            row =  [
                int(line[0]),
                line[1],
                line[2],
                int(line[3]),
                datetime.strptime(line[4],'%Y-%m-%d %H:%M:%S')
            ] if convert else line

            batch.append(row)

            if len(batch) >= batch_count:
                yield batch
                batch = []
        
        if len(batch) > 0:
            yield batch


def generate_row() -> tuple:
    return (
        random.choice(user_ids),
        random.choice(movie_ids),
        random.randint(1, 180),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


def generate_file():
    with open(os.path.join("test_data", CSV_FILE), mode='w') as f:
        for i in range(COUNT):
            f.write('{},{},{},{},{}\n'.format(i+1, *generate_row()))

if __name__ == "__main__":
    generate_file()

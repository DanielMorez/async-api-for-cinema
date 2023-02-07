import random
import clickhouse_driver
from datetime import datetime


client = clickhouse_driver.Client(host='localhost')

# params: id, user_id, movie_id, viewed_frame, event_time
SQL = 'INSERT INTO analysis.viewed_progress VALUES'

user_ids = [str(x) for x in range(10000)]
movie_ids = [str(x) for x in range(10000)]


def main():
    values: list = []
    for i in range(1, 10000001):
        data = {
            'id': i,
            'user_id': random.choice(user_ids),
            'movie_id': random.choice(movie_ids),
            'viewed_frame': random.randint(1, 180),
            'event_time': datetime.now(),
        }
        values.append(data)

        if len(values) >= 1000:
            try:
                client.execute('INSERT INTO analysis.viewed_progress VALUES', values)
            except clickhouse_driver.errors.Error as e:
                print(f'Ошибка при записи в КХ: ({e.code}) {e.message}')
            finally:
                values = []


if __name__ == '__main__':
    main()

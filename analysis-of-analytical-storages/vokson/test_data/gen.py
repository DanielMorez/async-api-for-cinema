import random
from datetime import datetime


COUNT = 10000000
user_ids = [str(x) for x in range(10000)]
movie_ids = [str(x) for x in range(10000)]

def generate_row() -> tuple:
    return (
        random.choice(user_ids),
        random.choice(movie_ids),
        random.randint(1, 180),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

with open('test.csv', mode='w') as f:
    for i in range(COUNT):
        f.write('{},{},{},{},{}\n'.format(i+1, *generate_row()))

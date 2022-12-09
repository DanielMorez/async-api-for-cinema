import time

from redis import Redis

if __name__ == '__main__':
    redis_client = Redis()
    while True:
        if redis_client.ping():
            break
        time.sleep(1)

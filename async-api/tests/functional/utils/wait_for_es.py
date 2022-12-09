import time

from elasticsearch import Elasticsearch

if __name__ == '__main__':
    es_client = Elasticsearch(hosts='http://localhost:9200', validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)

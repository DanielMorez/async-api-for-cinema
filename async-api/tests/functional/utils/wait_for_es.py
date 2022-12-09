import time
import logging
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    es_client = Elasticsearch(hosts="http://elasticsearch_tests:9200")
    while True:
        if es_client.ping():
            break
        time.sleep(1)
        logger.debug("Trying connect to ES...")

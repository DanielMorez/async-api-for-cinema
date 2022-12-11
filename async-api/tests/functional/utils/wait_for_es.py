import time
import logging

from elasticsearch import Elasticsearch
from pydantic import AnyUrl

logger = logging.getLogger(__name__)


def health_check_es(es_dsn: AnyUrl):
    es_client = Elasticsearch(hosts=[es_dsn])
    while True:
        logger.info(f"Trying connect to ES ({es_dsn})")
        if es_client.ping():
            break
        time.sleep(1)

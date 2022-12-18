import logging

from elasticsearch import Elasticsearch
from pydantic import AnyUrl

from utils.helpers.backoff import backoff

logger = logging.getLogger(__name__)


@backoff()
def health_check_es(es_dsn: AnyUrl):
    es_client = Elasticsearch(hosts=[es_dsn])
    logger.info(f"Trying connect to ES ({es_dsn})")
    if not es_client.ping():
        raise Exception("No connection to ES")

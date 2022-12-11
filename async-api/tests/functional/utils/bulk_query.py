import json
import logging


def get_es_bulk_query(data: list[dict], index: str, field: str):
    bulk_query = []
    for row in data:
        row_id = row.pop(field)
        bulk_query.extend([
            json.dumps({'index': {'_index': index, '_id': row_id}}),
            json.dumps(row)
        ])
    logging.info(f"Prepared bulk query for index `{index}`")
    return bulk_query

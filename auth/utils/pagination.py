from http import HTTPStatus

from flask import abort, request
from flask_sqlalchemy.query import Query


def paginate(query: Query, page: int = 1, page_size: int = 10) -> dict:
    """Important notice:
    query have to implement property `as_dict` that helps serialize db.Model objects
    """
    if page < 1 or page_size < 1:
        abort(HTTPStatus.BAD_REQUEST, "Page and page size are positive integer values")
    if page_size > 30:
        abort(HTTPStatus.BAD_REQUEST, "Page size can be from 1 to 30")
    page = query.paginate(page=page, per_page=page_size)
    data = {
        "count": query.count(),
        "prev": None,
        "next": None,
        "results": [p.as_dict for p in page.items],
    }
    if page.has_next:
        data["next"] = request.path + f"?page={page.next_num}&page_size={page_size}"
    if page.has_prev:
        data["prev"] = request.path + f"?page={page.prev_num}&page_size={page_size}"
    return data

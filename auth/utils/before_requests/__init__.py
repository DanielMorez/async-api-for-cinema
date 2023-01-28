from flask import Blueprint

from utils.before_requests.request_id import before_request

before_requests_bp = Blueprint("before_request", __name__)

before_requests_bp.before_app_request(before_request)

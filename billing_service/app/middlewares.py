from contextvars import ContextVar


x_request_id: ContextVar[str] = ContextVar("x_request_id", default="")


def request_id_middleware(get_response):
    def middleware(request):
        request_id = request.META.get("HTTP_X_REQUEST_ID")
        x_request_id.set(request_id)
        response = get_response(request)
        return response

    return middleware

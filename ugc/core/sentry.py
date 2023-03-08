def traces_sampler(sampling_context) -> float:
    transaction_sampling_mapper = {
        "rating": 0.2,
        "reviews": 0.3,
        "bookmarks": 0.1,
        "film-views": 0.1,
    }
    asgi_scope = sampling_context["asgi_scope"]
    if path := asgi_scope.get("path"):
        app_path = path.split("/")[1]
        return transaction_sampling_mapper.get(app_path, 1.0)

    return 0.5

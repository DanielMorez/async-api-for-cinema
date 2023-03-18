from workers.email.handlers.general import handlers as general_handlers
from workers.email.handlers.ugc import handlers as ugc_handlers

handlers = {**general_handlers, **ugc_handlers}

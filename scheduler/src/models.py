from enum import Enum


class NotificationStatuses(str, Enum):
    to_send = "to_send"
    in_process = "in_process"
    done = "done"
    cancelled = "cancelled"
    failed = "failed"

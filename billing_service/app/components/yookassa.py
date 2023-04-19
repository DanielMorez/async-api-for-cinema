import os

PAYMENT_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
PAYMENT_ALIVE = int(os.getenv("PAYMENT_ALIVE", 300))
HOST = os.getenv("HOST")
MIN_PAYMENT = int(os.getenv("MIN_PAYMENT"))
REFUND_AVAILABLE = int(os.getenv("REFUND_AVAILABLE"))  # in days

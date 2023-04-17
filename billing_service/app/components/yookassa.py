import os

PAYMENT_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
PAYMENT_ALIVE = int(os.getenv("PAYMENT_ALIVE", 300))
HOST = os.getenv("HOST")

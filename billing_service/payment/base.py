from abc import ABC, abstractmethod

from billing.models import Subscription, Bill


class BasePayment(ABC):
    @staticmethod
    @abstractmethod
    def create_payment_url(amount: float, description: str, user_id: str) -> str:
        """:return payment url"""
        pass

    @staticmethod
    @abstractmethod
    def check_payment_method(idempotency_key: str) -> str:
        """:return payment id"""
        pass

    @staticmethod
    @abstractmethod
    def auto_payment(subscription: Subscription) -> str:
        """:return payment id"""
        pass

    @staticmethod
    @abstractmethod
    def check_payment(idempotency_key: str) -> str:
        """:return status"""
        pass

    @staticmethod
    @abstractmethod
    def cancel_payment(bill: Bill) -> None:
        pass

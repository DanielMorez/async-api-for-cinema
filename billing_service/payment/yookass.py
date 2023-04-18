import uuid

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from yookassa import Configuration, Payment, Refund
from yookassa.domain.exceptions import bad_request_error

from billing.models import PaymentMethod, Bill, Subscription
from payment.base import BasePayment
from payment import exceptions

Configuration.account_id = settings.SHOP_ID
Configuration.secret_key = settings.PAYMENT_SECRET_KEY


class YooKassa(BasePayment):
    @staticmethod
    def create_payment_url(amount: float, description: str, user_id: str) -> str:
        idempotency_key = str(uuid.uuid4())
        expires_at = timezone.now() + timezone.timedelta(seconds=settings.PAYMENT_ALIVE)
        payment = Payment.create(
            {
                "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
                "confirmation": {
                    "type": "redirect",
                    "return_url": f"{settings.HOST}/api/v1/billing/approve-payment-method/{idempotency_key}",
                },
                "save_payment_method": True,
                "metadata": {
                    "user_id": user_id,  # necessary field or payment method doesn't link to user account !
                },
                "expires_at": expires_at,
                "capture": False,
                "description": description,
            },
            idempotency_key,
        )
        cache.set(idempotency_key, payment.id, timeout=settings.PAYMENT_ALIVE)
        return payment.confirmation.confirmation_url

    @staticmethod
    def check_payment_method(idempotency_key: str) -> str:
        if payment_id := cache.get(idempotency_key):
            payment = Payment.find_one(payment_id)
            if payment.status == "waiting_for_capture":
                Payment.cancel(payment_id, idempotency_key)
                cache.delete(idempotency_key)
                if payment.payment_method.saved:
                    if user_id := payment.metadata.get("user_id"):
                        card = payment.payment_method.card
                        payment_method = PaymentMethod(
                            user_id=user_id,
                            card_type=card.card_type,
                            expire=f"{card.expiry_month}/{card.expiry_year}",
                            last4=card.last4,
                            first6=card.first6,
                            payment_method_id=payment.payment_method.id,
                            provider="yookassa",
                        )
                        payment_method.save()
                        return payment_method.id
                    else:
                        raise exceptions.PaymentNotSaved
                else:
                    raise exceptions.PaymentNotSaved
            elif payment.status == "canceled":
                cache.delete(idempotency_key)
                raise exceptions.PaymentCanceled
        raise exceptions.PaymentNotAvailable

    @staticmethod
    def auto_payment(subscription: Subscription) -> str:
        idempotency_key = str(uuid.uuid4())
        payment = Payment.create({
            "amount": {
                "value": f"{subscription.tariff.cost:.2f}",
                "currency": "RUB"
            },
            "capture": True,
            "payment_method_id": subscription.payment_method.payment_method_id,
            "description": subscription.tariff.title,
            "metadata": {
                "user_id": str(subscription.user.id),
                "subscription_id": str(subscription.id),
                "tariff_id": str(subscription.tariff.id)
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"{settings.HOST}/api/v1/billing/approve-payment/{idempotency_key}",
            },
        }, idempotency_key)
        if payment.cancellation_details:
            Bill.objects.create(
                subscription_id=subscription.id,
                payment_method_id=subscription.payment_method.id,
                idempotency_key=idempotency_key,
                payment_id=payment.id,
                status=payment.cancellation_details.reason,
                value=subscription.tariff.cost
            )
            subscription.payment_method.delete()
            raise exceptions.PaymentDisable
        if payment.status == "pending":
            cache.set(idempotency_key, payment.id, timeout=settings.PAYMENT_ALIVE)
            return payment.confirmation.confirmation_url

        subscription.save()
        Bill.objects.create(
            subscription_id=subscription.id,
            payment_method_id=subscription.payment_method_id,
            idempotency_key=idempotency_key,
            payment_id=payment.id,
            value=subscription.tariff.cost
        )

    @staticmethod
    def check_payment(idempotency_key: str) -> dict:
        if payment_id := cache.get(idempotency_key):
            payment = Payment.find_one(payment_id)
            if payment.status == "succeeded":
                payment_method = PaymentMethod.objects.get(payment_method_id=payment.payment_method.id)
                if sub := Subscription.objects.filter(
                        id=payment.metadata["subscription_id"]
                ).first():
                    sub.status = "active"
                    sub.renew()
                else:
                    sub = Subscription.objects.create(
                        id=payment.metadata["subscription_id"],
                        user_id=payment.metadata["user_id"],
                        payment_method=payment_method,
                        tariff_id=payment.metadata["tariff_id"]
                    )
                Bill.objects.create(
                    subscription_id=payment.metadata["subscription_id"],
                    payment_method=payment_method,
                    idempotency_key=idempotency_key,
                    payment_id=payment_id,
                    value=sub.tariff.cost
                )
                cache.delete(idempotency_key)
                return payment
            elif payment.status == "canceled":
                cache.delete(idempotency_key)
                raise exceptions.PaymentCanceled
        raise exceptions.PaymentNotAvailable

    @staticmethod
    def cancel_payment(bill: Bill) -> None:
        try:
            payment = Refund.create({
                "amount": {
                    "value": f"{bill.value:.2f}",
                    "currency": "RUB"
                },
                "payment_id": str(bill.payment_id)
            })
            if payment.status != "succeeded":
                raise exceptions.RefundDisable
        except bad_request_error.BadRequestError as error:
            error = error.args[0]
            if "already completely refunded" in error["description"]:
                return
            raise exceptions.APIException(detail=error["description"])

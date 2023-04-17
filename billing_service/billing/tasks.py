from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import APIException

from app.celery import app
from authentication.client import AuthClient
from billing.models import Subscription, Tariff
from payment.yookass import YooKassa
from yookassa.domain.exceptions.api_error import ApiError

client: AuthClient = settings.AUTH_CLIENT


@app.task
def auto_payment():
    today = timezone.now()
    subscriptions = Subscription.objects.filter(
        ended_at__lte=today, status__in=("active", "waiting")
    )
    for subscription in subscriptions:
        if not subscription.tariff.is_active:
            if subscription.tariff.next_tariff:
                tariff = Tariff.objects.filter(
                    id=subscription.tariff.next_tariff
                ).first()
                if tariff:
                    subscription.tariff = tariff
                    subscription.save()
            else:
                subscription.status = "canceled"
                subscription.save()
                client.remove_subscriber_role(subscription.user_id)

        if subscription.status == "waiting":
            delta = timezone.now() - subscription.modified_at
            if delta.days > 7:
                subscription.status = "canceled"
                subscription.save()
                client.remove_subscriber_role(subscription.user_id)

        try:
            confirmation_url = YooKassa.auto_payment(subscription)

            if confirmation_url:
                # TODO: send notification to approve payment with 3DS
                subscription.status = "waiting"
                subscription.save()
                client.remove_subscriber_role(subscription.user_id)
            else:
                subscription.renew()
        except APIException:
            subscription.status = "canceled"
            subscription.save()
            client.remove_subscriber_role(subscription.user_id)
        except ApiError:
            subscription.status = "waiting"
            subscription.save()
            client.remove_subscriber_role(subscription.user_id)


@app.task
def remove_subscribe_role():
    today = timezone.now()
    subscriptions = Subscription.objects.filter(
        ended_at__lte=today, status="no_auto_payment"
    )
    for subscription in subscriptions:
        subscription.status = "canceled"
        subscription.save()
        client.remove_subscriber_role(subscription.user_id)

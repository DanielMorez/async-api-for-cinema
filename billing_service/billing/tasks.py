from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import APIException

from app.celery import app
from authentication.client import AuthClient
from billing.models import Subscription, Tariff, SubscriptionType
from payment.yookass import YooKassa
from yookassa.domain.exceptions.api_error import ApiError

client: AuthClient = settings.AUTH_CLIENT


@app.task
def auto_payment():
    today = timezone.now()
    subscriptions = Subscription.objects.filter(
        ended_at__lte=today,
        status__in=(
            SubscriptionType.ACTIVE,
            SubscriptionType.WAITING_FOR_PAYMENT
        )
    )
    for subscription in subscriptions:
        if not subscription.tariff.is_active:
            if subscription.tariff.next_tariff_id:
                tariff = Tariff.objects.filter(
                    id=subscription.tariff.next_tariff_id
                ).first()
                if tariff:
                    subscription.tariff = tariff
                    subscription.save()
            else:
                is_success = client.remove_subscriber_role(subscription.user_id)
                if is_success:
                    subscription.status = SubscriptionType.CANCELED
                    subscription.save()

        if subscription.status == SubscriptionType.WAITING_FOR_PAYMENT:
            delta = timezone.now() - subscription.modified_at
            if delta.days > 7:
                is_success = client.remove_subscriber_role(subscription.user_id)
                if is_success:
                    subscription.status = SubscriptionType.CANCELED
                    subscription.save()

        try:
            confirmation_url = YooKassa.auto_payment(subscription)

            if confirmation_url:
                # TODO: send notification to approve payment with 3DS
                is_success = client.remove_subscriber_role(subscription.user_id)
                if is_success:
                    subscription.status = SubscriptionType.WAITING_FOR_PAYMENT
                    subscription.save()
            else:
                subscription.renew()
        except APIException:
            is_success = client.remove_subscriber_role(subscription.user_id)
            if is_success:
                subscription.status = SubscriptionType.CANCELED
                subscription.save()
        except ApiError:
            is_success = client.remove_subscriber_role(subscription.user_id)
            if is_success:
                subscription.status = SubscriptionType.WAITING_FOR_PAYMENT
                subscription.save()


@app.task
def remove_subscribe_role():
    today = timezone.now()
    subscriptions = Subscription.objects.filter(
        ended_at__lte=today, status=SubscriptionType.WITHOUT_AUTO
    )
    for subscription in subscriptions:
        is_success = client.remove_subscriber_role(subscription.user_id)
        if is_success:
            subscription.status = SubscriptionType.CANCELED
            subscription.save()

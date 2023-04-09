import uuid

from django.conf import settings
from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PeriodType(models.TextChoices):
    WEEK = "week", "week"
    MONTH = "month", "month"
    YEAR = "year", "year"


class ProviderType(models.TextChoices):
    UKASSA = "ukassa", "ukassa"


class Tariff(UUIDModel):
    title = models.CharField(
        max_length=255
    )
    cost = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    period_type = models.CharField(
        max_length=10,
        choices=PeriodType.choices,
        default=PeriodType.MONTH
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    trial_period = models.BooleanField(default=False)
    trial_period_type = models.CharField(
        max_length=10,
        choices=PeriodType.choices,
        blank=True,
        null=True
    )
    next_tariff_id = models.UUIDField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class PaymentMethod(UUIDModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="payment_methods",
        on_delete=models.CASCADE,
    )
    mask = models.CharField(max_length=4)
    payment_method_id = models.UUIDField()
    provider = models.CharField(
        max_length=10,
        choices=ProviderType.choices,
        default=ProviderType.UKASSA
    )

    def __str__(self):
        return f"* {self.mask}"


class Subscription(UUIDModel):
    ended_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_waiting = models.BooleanField(default=False)
    tariff = models.ForeignKey(
        to=Tariff,
        related_name="subscriptions",
        on_delete=models.SET_NULL,
        null=True
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="subscriptions",
        on_delete=models.CASCADE,
    )
    payment_method = models.ForeignKey(
        to=PaymentMethod,
        related_name="subscriptions",
        on_delete=models.SET_NULL,
        null=True
    )


class Bill(UUIDModel):
    subscription = models.ForeignKey(
        to=Subscription,
        related_name="bills",
        on_delete=models.CASCADE,
    )

import uuid

from django.conf import settings
from django.db import models
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PeriodType(models.TextChoices):
    WEEK = "week", "Неделя"
    MONTH = "month", "Месяц"
    YEAR = "year", "Год"


class BillType(models.TextChoices):
    SUCCEEDED = "succeeded", "Успешно"
    CANCELED = "canceled", "Отменено"
    WAITING = "waiting", "Ожидается подтверждение платежа"


class ProviderType(models.TextChoices):
    YOOKASSA = "yookassa", "ЮKassa"


class SubscriptionType(models.TextChoices):
    ACTIVE = "active", "Активная"
    WAITING_FOR_PAYMENT = "waiting", "Не удалось продлить (Попробуем еще раз)"
    CANCELED = "canceled", "Отменена"
    WITHOUT_AUTO = "no_auto_payment", "Отключено автопродление"


class Tariff(UUIDModel):
    title = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    period_type = models.CharField(
        max_length=10, choices=PeriodType.choices, default=PeriodType.MONTH
    )
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    trial_period = models.BooleanField(default=False)
    trial_period_type = models.CharField(
        max_length=10, choices=PeriodType.choices, blank=True, null=True
    )
    next_tariff_id = models.UUIDField(blank=True, null=True)  # If current tariff is_active=False

    def __str__(self):
        return self.title


class PaymentMethod(UUIDModel):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="payment_methods",
        on_delete=models.CASCADE,
    )
    card_type = models.CharField(max_length=20, null=True)  # For example, Mir
    expire = models.CharField(max_length=7, null=True)  # For example, 12/2023
    last4 = models.CharField(max_length=4)
    first6 = models.CharField(max_length=6, null=True)
    payment_method_id = models.UUIDField()
    provider = models.CharField(
        max_length=10, choices=ProviderType.choices, default=ProviderType.YOOKASSA
    )

    def __str__(self):
        return f"{self.first6}******{self.last4}"


class Subscription(UUIDModel):
    ended_at = models.DateTimeField()
    status = models.CharField(
        default=SubscriptionType.ACTIVE,
        choices=SubscriptionType.choices,
        max_length=20,
    )
    tariff = models.ForeignKey(
        to=Tariff, related_name="subscriptions", on_delete=models.SET_NULL, null=True
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
        null=True,
    )
    
    def save(self, *args, **kwargs) -> "Subscription":
        if not self.ended_at:
            if self.tariff.trial_period:
                # Trial is only for newcomers
                if not self.__class__.objects.filter(user=self.user):
                    period = self.tariff.trial_period_type
                else:
                    period = self.tariff.period_type
            else:
                period = self.tariff.period_type
            self.ended_at = timezone.now() + relativedelta(**{f"{period}s": 1})
        super(Subscription, self).save(*args, **kwargs)
        return self

    def renew(self):
        period = self.tariff.period_type
        self.ended_at = timezone.now() + relativedelta(**{f"{period}s": 1})
        self.save()


class Bill(UUIDModel):
    subscription = models.ForeignKey(
        to=Subscription,
        related_name="bills",
        on_delete=models.CASCADE,
    )
    payment_method = models.ForeignKey(
        to=PaymentMethod,
        related_name="bills",
        on_delete=models.SET_NULL,
        null=True
    )
    idempotency_key = models.UUIDField(null=True)
    payment_id = models.UUIDField()
    value = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=BillType.choices,
        default=BillType.SUCCEEDED
    )

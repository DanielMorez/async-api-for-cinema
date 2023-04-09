from django.contrib import admin
from billing import models


@admin.register(models.Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("title", "cost", "is_active", "period_type")


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "ended_at")


@admin.register(models.PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
    )

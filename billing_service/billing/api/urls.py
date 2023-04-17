from django.urls import path

from billing.api.views import (
    TariffListAPIView,
    SubscriptionAPIView,
    PaymentMethodAPIView,
    ApprovePaymentAPIView,
    CancelSubscriptionAPIView,
    SubscriptionPaymentAPIView,
    ApprovePaymentMethodAPIView,
)

urlpatterns = [
    path("tariffs", TariffListAPIView.as_view()),
    path("payment-method", PaymentMethodAPIView.as_view()),
    path("payment-method/<str:pk>", PaymentMethodAPIView.as_view()),
    path("approve-payment/<str:idempotency_key>", ApprovePaymentAPIView.as_view()),
    path("approve-payment-method/<str:idempotency_key>", ApprovePaymentMethodAPIView.as_view()),
    path("change-payment-method", SubscriptionPaymentAPIView.as_view()),
    path("cancel-subscription", CancelSubscriptionAPIView.as_view()),
    path("subscription", SubscriptionAPIView.as_view()),
]

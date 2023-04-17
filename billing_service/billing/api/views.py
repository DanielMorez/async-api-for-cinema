import uuid

from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions, response, status

from authentication.client import AuthClient
from payment.base import BasePayment
from payment.yookass import YooKassa
from billing.api.serializers import (
    TariffSerializer,
    PaymentMethodSerializer,
    SubscriptionSerializer,
)
from billing.models import Tariff, PaymentMethod, Subscription, Bill


class PaymentMixin:
    payment_provider: BasePayment = YooKassa
    auth_client: AuthClient = settings.AUTH_CLIENT


class TariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.filter(is_active=True)
    serializer_class = TariffSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PaymentMethodAPIView(
    generics.ListCreateAPIView, generics.DestroyAPIView, PaymentMixin
):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def post(self, request, *args, **kwargs):
        url = self.payment_provider.create_payment_url(
            2, "Привязка банковской карты", request.user.id
        )
        return response.Response({"confirmation_url": url})


class ApprovePaymentMethodAPIView(generics.GenericAPIView, PaymentMixin):
    permission_classes = [permissions.AllowAny]  # Change on IsAuthenticated

    def get(self, request, *args, **kwargs):
        self.payment_provider.check_payment_method(kwargs["idempotency_key"])
        return response.Response()


class SubscriptionAPIView(generics.CreateAPIView, generics.RetrieveAPIView, PaymentMixin):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    confirmation_url = None

    def perform_create(self, serializer):
        tariff: Tariff = serializer.validated_data["tariff"]
        payment_method: PaymentMethod = serializer.validated_data["payment_method"]

        subscription = Subscription(
            id=uuid.uuid4(),
            tariff=tariff,
            payment_method=payment_method,
            user_id=self.request.user.id
        )

        if tariff.trial_period:
            if not self.queryset.filter(user_id=self.request.user.id):
                return serializer.save(pk=subscription.id, user_id=self.request.user.id)

        self.confirmation_url = self.payment_provider.auto_payment(
            subscription
        )
        if not self.confirmation_url:
            self.auth_client.assign_subscriber_role(self.request.user.id)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return response.Response(
            {"confirmation_url": self.confirmation_url}
        )

    def get_object(self):
        return generics.get_object_or_404(
            self.queryset,
            user_id=self.request.user.id,
            status__in=("active", "waiting", "no_auto_payment")
        )


class SubscriptionPaymentAPIView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class ApprovePaymentAPIView(generics.GenericAPIView, PaymentMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        self.payment_provider.check_payment(kwargs["idempotency_key"])
        self.auth_client.assign_subscriber_role(self.request.user.id)
        return response.Response()


class CancelSubscriptionAPIView(generics.GenericAPIView, PaymentMixin):
    queryset = Subscription.objects.all()

    def put(self, request, *args, **kwargs):
        subscription = self.queryset.filter(
            user_id=request.user.id,
            status__in=("active", "waiting")
        ).first()

        if not subscription:
            return response.Response(
                "User does not have active subscription", status=status.HTTP_400_BAD_REQUEST
            )

        if subscription.status == "active":
            bill: Bill = subscription.bills.filter(status="waiting").order_by("-created_at").first()
            if bill:
                delta = timezone.now() - subscription.created_at
                if delta.days <= 2:
                    self.payment_provider.cancel_payment(bill)
                    subscription.status = "canceled"
                    subscription.save()
                    bill.status = "canceled"
                    bill.save()
                    self.auth_client.remove_subscriber_role(self.request.user.id)
                    return response.Response({"refund": True})

        subscription.status = "no_auto_payment"
        subscription.save()
        return response.Response({"refund": False})


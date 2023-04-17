from rest_framework import serializers

from billing.api.exceptions import ActiveSubscriptionExists, PaymentNotAvailable
from billing.models import Tariff, PaymentMethod, Subscription


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        exclude = ("next_tariff_id", "created_at", "modified_at")


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        exclude = ("user", "provider", "payment_method_id")


class SubscriptionSerializer(serializers.ModelSerializer):
    ended_at = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Subscription
        exclude = ("user",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if isinstance(instance, Subscription):
            data["tariff"] = TariffSerializer(instance.tariff).data
            data["payment_method"] = PaymentMethodSerializer(
                instance.payment_method
            ).data
        return data

    def is_valid(self, *args, **kwargs):
        is_valid = super().is_valid(*args, **kwargs)
        user = self.context["request"].user
        if Subscription.objects.filter(
            user_id=user.id,
            status="active"
        ):
            raise ActiveSubscriptionExists
        payment_method: PaymentMethod = self.validated_data["payment_method"]
        if str(payment_method.user_id) != user.id:
            raise PaymentNotAvailable
        return is_valid


class SubscriptionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        field = ("payment_method",)

    def is_valid(self, *args, **kwargs):
        is_valid = super().is_valid(*args, **kwargs)
        user = self.context["request"].user
        if Subscription.objects.filter(
            user_id=user.id,
            status="active"
        ):
            raise ActiveSubscriptionExists
        payment_method: PaymentMethod = self.validated_data["payment_method"]
        if str(payment_method.user_id) != user.id:
            raise PaymentNotAvailable
        return is_valid

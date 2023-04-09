from rest_framework import serializers

from billing.models import Tariff


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        exclude = ("next_tariff_id", "create_at", "modified_at")

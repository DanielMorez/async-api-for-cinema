from rest_framework import generics

from billing.api.serializers import TariffSerializer
from billing.models import Tariff


class TariffListAPIView(generics.ListAPIView):
    queryset = Tariff.objects.filter(is_active=True)
    serializer_class = TariffSerializer

from django.urls import path

from billing.api.views import TariffListAPIView

urlpatterns = [
    path("tariffs", TariffListAPIView.as_view()),
]

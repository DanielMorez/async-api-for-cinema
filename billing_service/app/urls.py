from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("billing/admin/", admin.site.urls),
    path("api/v1/billing/", include("billing.api.urls")),
]

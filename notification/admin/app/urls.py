from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("notification/admin/", admin.site.urls),
]

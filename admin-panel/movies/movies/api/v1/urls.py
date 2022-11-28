from django.urls import path

from .views import FilmWorkListAPIView, FilmWorkRetrieveAPIView

urlpatterns = [
    path('movies/', FilmWorkListAPIView.as_view()),
    path('movies/<uuid:pk>', FilmWorkRetrieveAPIView.as_view()),
]

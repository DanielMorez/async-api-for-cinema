from django.db.models import Prefetch

from rest_framework import generics

from movies.models import FilmWork, PersonFilmWork, RoleType

from .serializers import FilmWorkSerializer


class MoviesMixinAPIView(generics.GenericAPIView):
    queryset = FilmWork.objects.all()
    serializer_class = FilmWorkSerializer

    def get_queryset(self):
        qs = super(MoviesMixinAPIView, self).get_queryset()
        qs = qs.prefetch_related(
            'genres',
            Prefetch(
                'persons',
                PersonFilmWork.objects.filter(
                    role=RoleType.ACTOR
                ),
                to_attr='actors'
            ),
            Prefetch(
                'persons',
                PersonFilmWork.objects.filter(
                    role=RoleType.WRITER
                ),
                to_attr='writers'
            ),
            Prefetch(
                'persons',
                PersonFilmWork.objects.filter(
                    role=RoleType.DIRECTOR
                ),
                to_attr='directors'
            ),
        )
        return qs


class FilmWorkListAPIView(MoviesMixinAPIView, generics.ListAPIView):
    pass


class FilmWorkRetrieveAPIView(MoviesMixinAPIView, generics.RetrieveAPIView):
    pass

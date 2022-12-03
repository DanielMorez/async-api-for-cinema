from rest_framework import serializers

from movies.models import FilmWork, PersonFilmWork, GenreFilmWork


class PersonSerializer(serializers.ModelSerializer):
    # Можно использовать так, но...
    full_name = serializers.CharField(source='person.full_name')

    class Meta:
        model = PersonFilmWork
        fields = ('full_name',)

    def to_representation(self, instance) -> str:
        # Я сделал так, потому что в openapi.yaml
        # персона представлена в виде строки, а не словаря
        return instance.person.full_name


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='genre.name')

    class Meta:
        model = GenreFilmWork
        fields = ('name',)

    def to_representation(self, instance) -> str:
        return instance.genre.name


class FilmWorkSerializer(serializers.ModelSerializer):
    actors = PersonSerializer(many=True)
    writers = PersonSerializer(many=True)
    directors = PersonSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = FilmWork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'writers',
            'directors',
        )

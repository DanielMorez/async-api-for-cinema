from django.contrib import admin

from .models import (
    Genre,
    Person,
    FilmWork,
    GenreFilmWork,
    PersonFilmWork,
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender')
    search_fields = ('full_name',)
    list_filter = ('gender',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    autocomplete_fields = ('genre',)
    extra = 0


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    autocomplete_fields = ('person',)
    extra = 0


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'type', 'creation_date', 'rating', 'created', 'modified'
    )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

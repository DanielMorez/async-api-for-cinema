import uuid

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'content"."genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    certificate = models.CharField(
        _('certificate'),
        max_length=512,
        blank=True,
        null=True
    )
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )
    title = models.TextField(_('title'))
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(
        _('creation date'),
        blank=True,
        null=True,
        db_index=True
    )
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    type = models.CharField(
        _('type'),
        max_length=7,
        choices=Type.choices
    )

    class Meta:
        managed = True
        db_table = 'content"."film_work'
        indexes = [
            models.Index(
                fields=['creation_date'],
                name='film_work_creation_date_idx'
            ),
        ]
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name='genres'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'content"."genre_film_work'
        constraints = [
            models.UniqueConstraint(
                fields=['film_work_id', 'genre_id'],
                name='genre_film_work_idx_unique'
            ),
        ]
        indexes = [
            models.Index(
                fields=['film_work_id', 'genre_id'],
                name='genre_film_work_idx'
            ),
        ]


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full name'))
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        managed = True
        db_table = 'content"."person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name='persons'
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    role = models.TextField(_('role'), null=True, choices=RoleType.choices)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'content"."person_film_work'
        indexes = [
            models.Index(
                fields=['film_work_id', 'person_id'],
                name='film_work_person_idx'
            ),
        ]
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    name = models.CharField(_('name'), max_length=16)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = "content\".\"genre"

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    full_name = models.CharField(_('full name'), max_length=64)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = "content\".\"person"

    def __str__(self):
        return self.full_name


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_index=False)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, db_index=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre')
        ]


class PersonRole(models.TextChoices):
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')
    ACTOR = 'actor', _('actor')


class FilmworkPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_index=False)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, db_index=False)
    role = models.CharField(_('role'), max_length=16, choices=PersonRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='film_work_person_role')
        ]


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')


class Filmwork(TimeStampedModel):
    title = models.CharField(_('title'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.URLField(_('url'), blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('type'), max_length=16, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    persons = models.ManyToManyField(Person, through='FilmworkPerson')

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "content\".\"film_work"

    def __str__(self):
        return self.title

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        models.UniqueConstraint(fields=['name'], name='unique_genre_name')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('fullname'), max_length=128)
    birth_date = models.DateField(null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('actor')
        verbose_name_plural = _('actors')
        models.UniqueConstraint(fields=['full_name', 'birth_date'], name='unique_full_name_birth_date')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkType(models.TextChoices):
        MOVIE = 'MOVIE', _('Movie')
        TV_SHOW = 'TV_SHOW', _('TV-Show')

    title = models.CharField(_('title'), max_length=255, blank=False)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                               MaxValueValidator(100)])
    type = models.CharField(_('filmwork type'),
                            max_length=32,
                            choices=FilmworkType.choices,)
    certificate = models.CharField(_('certificate'), max_length=512, null=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        models.UniqueConstraint(fields=['title', 'creation_date', 'type'], name='unique_title_creation_date_type')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, blank=False)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        models.UniqueConstraint(fields=['film_work_id', 'genre_id'], name='unique_film_work_genre')
        indexes = [
            models.Index(fields=['film_work_id']),
            models.Index(fields=['genre_id']),
        ]


class PersonFilmwork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = 'actor', _('Actor')
        DIRECTOR = 'director', _('Director')
        WRITER = 'writer', _('Writer')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, blank=False)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, blank=False)
    role = models.CharField(_('role'), 
                            blank=False,
                            max_length=32,
                            choices=RoleType.choices,)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='unique_film_work_person_role')
        indexes = [
            models.Index(fields=['film_work_id']),
            models.Index(fields=['person_id']),
        ]
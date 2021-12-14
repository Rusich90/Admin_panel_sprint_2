from django.contrib import admin
from .models import Filmwork, Genre, Person


class GenreInline(admin.TabularInline):
    model = Filmwork.genres.through


class PersonInline(admin.TabularInline):
    model = Filmwork.persons.through


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating',)

    list_filter = ('type', 'creation_date', 'rating')

    search_fields = ('title', 'description', 'id',)

    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating',
    )

    inlines = [
        GenreInline,
        PersonInline,
    ]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date',)

    list_filter = ('birth_date',)

    search_fields = ('full_name', 'id',)

    fields = ('full_name', 'birth_date',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

    search_fields = ('name', 'id',)

    fields = ('name', 'description',)


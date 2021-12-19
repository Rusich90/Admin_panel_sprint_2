from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse

from movies.models import Filmwork, PersonRole


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        fields = ('id', 'title', 'description', 'creation_date', 'rating', 'type')
        genres = ArrayAgg('genres__name', distinct=True)
        actors = ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=PersonRole.ACTOR))
        directors = ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=PersonRole.DIRECTOR))
        writers = ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=PersonRole.WRITER))
        return Filmwork.objects.values(*fields).annotate(
            genres=genres,
            actors=actors,
            directors=directors,
            writers=writers,
        )

    def render_to_response(self, context):
        return JsonResponse(context)

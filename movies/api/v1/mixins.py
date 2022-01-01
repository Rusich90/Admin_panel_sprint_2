from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse

from movies.models import Filmwork, PersonRole


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        fields = ('id', 'title', 'description', 'creation_date', 'rating', 'type')
        qs = super().get_queryset()
        return qs.values(*fields).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self._aggregate_person(role=PersonRole.ACTOR),
            directors=self._aggregate_person(role=PersonRole.DIRECTOR),
            writers=self._aggregate_person(role=PersonRole.WRITER),
        )

    def render_to_response(self, context):
        return JsonResponse(context)

    def _aggregate_person(self, role):
        return ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role=role))

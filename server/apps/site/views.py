from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from server.apps.site.logic.data_processing import get_family_composition
from .models import Family, Person


def index(request: HttpRequest) -> HttpResponse:
    """
    Main (or index) view.

    Returns rendered default page to the user.
    """
    families: QuerySet = Family.objects.order_by('surname').distinct('surname').exclude(surname='Нет данных')
    return render(request, 'site/index.html', {'families': families})


def _get_family_list(id_family: int) -> QuerySet:
    person_list = Person.objects.filter(parent_id=id_family)
    return person_list


def detail_family(request: HttpRequest, id_family: int) -> HttpResponse:
    """
    Family page of the same family
    Returns rendered hierarchical family list
    """
    family = get_object_or_404(Family, id=id_family)
    return render(request, 'site/detail_family.html', {'family': family})


@require_GET
def family_composition(request: HttpRequest, id_person: int) -> JsonResponse:
    families = get_family_composition(id_person)
    return JsonResponse({'families': families})

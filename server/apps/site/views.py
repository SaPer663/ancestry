from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Family


def index(request: HttpRequest) -> HttpResponse:
    """
    Main (or index) view.

    Returns rendered default page to the user.
    """
    families: Family = Family.objects.all()
    return render(request, 'site/index.html', {'families': families})

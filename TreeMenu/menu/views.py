from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """ Home page with menus."""
    INDEX = 'index.html'

    return render(request, INDEX)

from django.shortcuts import render
from django.http import Http404


def home(request):
    return render(request, 'home.html')

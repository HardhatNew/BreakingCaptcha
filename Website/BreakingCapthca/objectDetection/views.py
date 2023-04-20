from django.shortcuts import render
from django.http import Http404


def home(request):
    return render(request, 'home.html')


def objectDetection(request):
    return render(request, 'objectDetection.html')


def textDetection(request):
    return render(request, 'textDetection.html')


def voiceDetection(request):
    return render(request, 'voiceDetection.html')

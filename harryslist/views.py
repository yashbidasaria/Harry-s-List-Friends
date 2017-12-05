from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


# Create your views here.

def index(request):
    return render(request, 'index.html')

def top_artists(request):
    return render(request, 'top_artists.html')

def top_albums(request):
    return render(request, 'top_albums.html')

def top_songs(request):
    return render(request, 'top_songs.html')

def about(request):
    return render(request, 'about.html')

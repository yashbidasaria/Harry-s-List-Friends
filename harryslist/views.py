from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Song

# Create your views here.

def index(request):
    song = Song.objects.all()
    l = [];
    for p in Song.objects.raw('Select Song_ID, Name, Plays from Song'):
        l.append(p)
    return render(request, 'index.html', {'song': l})

def top_artists(request):
    return render(request, 'top_artists.html')

def top_albums(request):
    return render(request, 'top_albums.html')

def top_songs(request):
    return render(request, 'top_songs.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

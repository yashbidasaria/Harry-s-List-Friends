from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Song, Album, Artist

# Create your views here.
def index(request):
	tuples = []
  for t in Song.objects.raw('Select Song_ID, Name, Plays from Song'):
      tuples.append(t)
  return render(request, 'index.html', {'song': tuples})

def top_artists(request):
    return render(request, 'top_artists.html')

def artists_otd(request):
	tuples = []
	for t in Artist.objects.raw('SELECT Artist.User_ID, Artist.Name, Artist.Location FROM Artist ORDER BY RANDOM() LIMIT 15'):
		tuples.append(t)
	return render(request, 'artists_otd.html', {'artist': tuples})

def top_albums(request):
	tuples = []
	for t in Album.objects.raw('SELECT Album.User_ID, RateAlbums.Name, Artist.Name, RateAlbums.Stars FROM Album, Artist, RateAlbums WHERE RateAlbums.Stars = 5 AND Artist.User_ID = RateAlbums.Owner_User_ID LIMIT 15'):
		tuples.append(t)
	return render(request, 'top_albums.html')

def top_songs(request):
	tuples = []
	for t in Song.objects.raw('SELECT Song.Song_ID, Song.Name, Song.Album_Name, Artist.Name, RateSongs.Stars FROM Song, Artist, RateSongs WHERE RateSongs.stars = 5 AND Song.Song_ID = RateSongs.Song_ID AND Artist.User_ID = Song.User_ID LIMIT 15'):
		tuples.append(t)
    return render(request, 'top_songs.html', {'song': tuples})

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

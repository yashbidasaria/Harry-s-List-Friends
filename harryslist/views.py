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
from django.db import connection

# Create your views here.
def index(request):
	tuples = []
	for t in Song.objects.raw('Select Song_ID, Name, Plays from Song'):
		tuples.append(t)
	return render(request, 'index.html', {'song': tuples})

def top_artists(request):
	cursor = connection.cursor()
	cursor.execute('SELECT Artist.Name, Artist.Location FROM Artist WHERE Artist.User_ID IN (SELECT Song.User_ID FROM Song, RateSongs WHERE RateSongs.Stars = 5 and Song.Song_ID = RateSongs.Song_ID) AND Artist.User_ID IN (SELECT Owner_User_ID FROM RateAlbums WHERE Stars = 5) LIMIT 15')
	tuples = cursor.fetchall()
	return render(request, 'top_artists.html', {'artist': tuples})

def artists_otd(request):
	cursor = connection.cursor()
	cursor.execute('SELECT Artist.Name, Artist.Location FROM Artist ORDER BY RANDOM() LIMIT 15')
	tuples = cursor.fetchall()
	return render(request, 'artists_otd.html', {'artist': tuples})

def top_albums(request):
	cursor = connection.cursor()
	cursor.execute('SELECT Album.Name, Artist.Name, RateAlbums.Stars FROM Album, Artist, RateAlbums WHERE RateAlbums.Stars = 5 AND Artist.User_ID = RateAlbums.Owner_User_ID AND Album.USER_ID = Artist.User_ID LIMIT 15')
	tuples = cursor.fetchall()
	return render(request, 'top_albums.html', {'album': tuples})

def top_songs(request):
	cursor = connection.cursor()
	cursor.execute('SELECT Song.Name, Song.Album_Name, Artist.Name, RateSongs.Stars FROM Song, Artist, RateSongs WHERE RateSongs.stars = 5 AND Song.Song_ID = RateSongs.Song_ID AND Artist.User_ID = Song.User_ID LIMIT 15')
	tuples = cursor.fetchall()
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

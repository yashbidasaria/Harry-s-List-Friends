import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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
	return render(request, 'homepage.html', {'song': tuples})

def homepage(request):
	return render(request, 'homepage.html')

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

def search(request):
	if request.method == 'GET': # this will be GET now
		search_input =  request.GET['q'] # do some research what it does
		#print(str(song_name))
		cursor = connection.cursor()
		query = "SELECT DISTINCT Song.Name, Song.Album_Name, Artist.Name, RateSongs.Stars, Song.Song_ID FROM Song, Artist, RateSongs WHERE Song.User_ID=Artist.User_ID AND Song.Song_ID = RateSongs.Song_ID AND Song.Name LIKE "+"'%" + str(search_input) + "%' LIMIT 15"
		cursor.execute(query)
		song_tuples = cursor.fetchall()

		query = "SELECT DISTINCT Artist.Name, Artist.Location FROM Artist WHERE Artist.Name LIKE "+"'%" + str(search_input) + "%' LIMIT 15"
		cursor.execute(query)
		artist_tuples = cursor.fetchall()

		query = "SELECT DISTINCT Album.Name, Artist.Name, RateAlbums.Stars FROM Album, Artist, RateAlbums WHERE Album.User_ID=Artist.User_ID AND Album.User_ID = RateAlbums.Owner_User_ID AND Album.Name LIKE "+"'%" + str(search_input) + "%' LIMIT 15"
		cursor.execute(query)
		album_tuples = cursor.fetchall()
		#print(tuples)
		return render(request,"search.html",{"song":song_tuples, "artists":artist_tuples, "albums":album_tuples })
	else:
		return render(request,"search.html",{})

def flag_song(request):
	if request.method == 'GET':
		song_id = request.GET['song_id']
		print(song_id)
		cursor = connection.cursor()
		query = "SELECT * FROM Review WHERE Song_ID="+ "'" + str(song_id) + "'"
		cursor.execute(query)
		tuples = cursor.fetchall()
		print(tuples)
		if len(tuples) == 0:
			# case where we add to reviewed table
			review_tuple = (str(song_id), str(0), str(0), str(datetime.datetime.now()))
			new_query = "INSERT INTO Review (Song_ID, Deleted, Reviewed, Flagged_Date) Values ( "+"'"+song_id+"',"+str(0)+","+str(0)+ ",'"+ str(datetime.datetime.now()) + "')"
			print (new_query)
			cursor.execute(new_query)

			data = {
				'exists': 0
			}
			return JsonResponse(data)
		else:
			data = {
				'exists': 1,
				'error': "Song is already flagged"
			}
			return JsonResponse(data)

def rate_song(request):
	if request.method == 'GET':
		song_id = request.GET['song_id']
		rating = request.GET['rating']
		userid = User.objects.get(username=request.user).pk
		cursor = connection.cursor()
		query = "SELECT * FROM RateSongs WHERE Song_ID="+ "'" + str(song_id) + "'" + "AND Rater_User_ID=" +  "'" + str(userid) + "'"
		cursor.execute(query)
		tuples = cursor.fetchall()
		if len(tuples) == 0:
			# case where user hasn't rated yet so insert into table
			review_tuple = (str(song_id), str(0), str(0), str(datetime.datetime.now()))
			new_query = "INSERT INTO RateSongs (Rater_User_ID, Song_ID, Stars, Rate_Date) Values ( "+"'"+str(userid)+"','"+str(song_id)+"',"+str(rating)+ ",'"+ str(datetime.datetime.now()) + "')"
			print (new_query)
			cursor.execute(new_query)

			data = {
				'exists': 0
			}
			return JsonResponse(data)
		else:
			data = {
				'exists': 1,
				'error': "You have already rated the song!!!!!!!"
			}
			return JsonResponse(data)

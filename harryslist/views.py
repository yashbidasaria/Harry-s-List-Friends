import datetime, pandas, logging
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import TemplateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Song, Album, Artist, Review
from django.contrib.auth.decorators import permission_required
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

def admin_page(request):

	if request.method == 'GET': # this will be GET now
		#print(str(song_name))
		cursor = connection.cursor()
		review_tuples = []
		#query = "SELECT DISTINCT Song.Name, Song.Album_Name, Artist.Name, Review.Flagged_Date, Review.Reviewed, Review.Deleted FROM Song, Artist, Review WHERE Song.User_ID=Artist.User_ID AND Song.Song_ID = Review.Song_ID"
		#cursor.execute(query)
		#review_tuples = cursor.fetchall()
		#for r in Review.objects.raw('SELECT Review_ID, Flagged_Date from Review'):
		#	print (r.Flagged_Date)
			#review_tuples.append(r)
		#user table
		user_query = "SELECT id, username, password, is_staff FROM auth_user"
		cursor.execute(user_query)
		user_tuples = cursor.fetchall()

		#artist table
		artist_query = "SELECT Image_Src, User_ID, Name, Location FROM Artist"
		#cursor.execute(artist_query)
		artist_tuples = cursor.fetchall()

		#song table
		song_query = "SELECT Song_ID, User_ID, Album_Name, Name, Plays FROM Song"
		#cursor.execute(song_query)
		song_tuples = cursor.fetchall()

		#album table
		album_query = "SELECT User_ID, Name, Year FROM Album"
		#cursor.execute(album_query)
		album_tuples = cursor.fetchall()

		#admin table
		admin_query = "SELECT Admin_ID, Admin_Email, Name FROM Admin"
		#cursor.execute(admin_query)
		admin_tuples = cursor.fetchall()

		#review table
		review_query = "SELECT Review_ID, Song_ID, Admin_ID, Deleted, Reviewed, Flagged_Date, Review_Date FROM Review"
		cursor.execute(review_query)
		review_tuples = cursor.fetchall()


		#rate albums table
		ratealbums_query = "SELECT Rate_Album_ID, Rater_User_ID, Owner_User_ID, Name, Stars, Rate_Date FROM RateAlbums"
		#cursor.execute(ratealbums_query)
		ratealbums_tuples = cursor.fetchall()


		#rate songs table
		#ratesongs_query = "SELECT Rate_Song_ID, Rater_User_ID, Name, Stars, Rate_Date FROM RateSongs"
		ratesongs_query = "SELECT * FROM RateSongs"
		#cursor.execute(ratesongs_query)
		ratesongs_tuples = cursor.fetchall()

		return render(request,"admin_page.html",{"user":user_tuples, "artist":artist_tuples, "song":song_tuples, "album":album_tuples, "admin":admin_tuples,"review":review_tuples, "ratealbum":ratealbums_tuples, "ratesong":ratesongs_tuples})

def search(request):
	if request.method == 'GET': # this will be GET now
		search_input =  request.GET['q'] # do some research what it does
		#print(str(song_name))
		cursor = connection.cursor()
		query = "SELECT DISTINCT Song.Name, Song.Album_Name, Artist.Name, RateSongs.Stars, Song.Song_ID FROM Song, Artist, RateSongs WHERE Song.User_ID=Artist.User_ID AND Song.Song_ID = RateSongs.Song_ID AND Song.Name LIKE "+"'%" + str(search_input) + "%' LIMIT 15"
		cursor.execute(query)
		song_tuples = cursor.fetchall()

		query = "SELECT DISTINCT Artist.Image_Src, Artist.Name, Artist.Location FROM Artist WHERE Artist.Name LIKE "+"'%" + str(search_input) + "%' LIMIT 15"
		cursor.execute(query)
		artist_tuples = cursor.fetchall()

		query = "SELECT DISTINCT Album.Name, Artist.Name, RateAlbums.Stars, Artist.User_ID FROM Album, Artist, RateAlbums WHERE Album.User_ID=Artist.User_ID AND Album.User_ID = RateAlbums.Owner_User_ID AND Album.Name LIKE "+"'%" + str(search_input) + "%' LIMIT 15"
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

def rate_album(request):
	if request.method == 'GET':
		album_name = request.GET['album_name']
		artist_id = request.GET['artist_id']
		rating = request.GET['rating']
		userid = User.objects.get(username=request.user).pk
		cursor = connection.cursor()
		query = "SELECT * FROM RateAlbums WHERE Owner_User_ID="+ "'" + str(artist_id) + "'" + "AND Rater_User_ID=" +  "'" + str(userid) + "'" + " AND Name='"+str(album_name)+"'"
		print(query)
		cursor.execute(query)
		tuples = cursor.fetchall()
		if len(tuples) == 0:
			new_query = "INSERT INTO RateAlbums (Rater_User_ID, Owner_User_ID, Name, Stars, Rate_Date) Values ( "+"'"+str(userid)+"','"+str(artist_id)+"','"+str(album_name)+"',"+str(rating)+ ",'"+ str(datetime.datetime.now()) + "')"
			print (new_query)
			cursor.execute(new_query)
			data = {
				'exists': 0
			}
			return JsonResponse(data)
		else:
			data = {
				'exists': 1,
				'error': "You have already rated this album."
			}
			return JsonResponse(data)

def upload_content(request):
	# do all the csv uploading
	try:
		print("in try")
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			#messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("upload_csv"))
        #if file is too large, return
		if csv_file.multiple_chunks():
			#messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("upload_csv"))

		df = pandas.read_csv(csv_file, encoding = "latin1")
		c = connection.cursor()
        #lines = file_data.split("\n")
		print(len(df))
		# need to change this to insert into db instead
		for i in range(0, len(df.index)):
	        # get songID and userID
			songID = df['SongID'][i]
			artistID = df['ArtistID'][i]
			# get song, album and artist names
			songName = df['Title'][i]
			artistName = df['ArtistName'][i]
			albumName = df['AlbumName'][i]
			# get artist location
			location = df['ArtistLocation'][i]
			# get year made
			year = df['Year'][i]
			plays = 20*(i%5 + 1)
			# insert into song, artist and album tables
			song_tuple = (str(songID), str(artistID), str(albumName), str(songName), str(plays))
			artist_tuple = (artistID, artistName, location)
			album_tuple = (artistID, albumName, int(year))
			rateAlbums_tuple = (artistID, artistID, albumName, 5, datetime.datetime.now(), albumName)
			rateSongs_tuple = (artistID, songID, 5, datetime.datetime.now())

			user_query = "INSERT OR IGNORE INTO auth_user (username, first_name, Password) Values "+"('"+str(artistID)+"','"+str(artistName)+"','"+str(location)+ "')"
			c.execute(user_query)
			print ("added user")
			# artist first
			artist_query = "INSERT OR IGNORE INTO Artist (User_ID, Name, Location) Values "+"('"+str(artistID)+"','"+str(artistName)+"','"+str(location)+ "')"
			print(artist_query)

			c.execute(artist_query)
			print("after artist query")

			#album second
			#only allowing one time uploads for albums
			#query = "INSERT INTO Album (User_ID, Name, Year) SELECT "+"'"+artistID+"','"+albumName+"',"+str(year)+ " WHERE NOT EXISTS (SELECT 1 FROM Album WHERE Name = '"+albumName+"')"
			album_query = "INSERT OR IGNORE INTO Album (User_ID, Name, Year) Values "+"('"+str(artistID)+"','"+str(albumName)+"','"+str(year)+ "')"
			c.execute(album_query)
			print("after album query")

			# song third
			song_query = "INSERT OR IGNORE INTO Song (Song_ID, User_ID, Album_Name, Name, Plays) Values "+"('"+str(songID)+"','"+str(artistID)+"','"+str(albumName)+"','" +str(songName)+"','"+ str(plays) + "')"
			c.execute(song_query)
			print("after song query")
			# rate song after the songs exist
			#c.execute('INSERT OR IGNORE INTO RateSongs (Rater_User_ID, Song_ID, Stars, Rate_Date) VALUES (?,?,?,?)', rateSongs_tuple)

			rate_song_query = "INSERT OR IGNORE INTO RateSongs (Rater_User_ID, Song_ID, Stars, Rate_Date) VALUES ("+"'"+str(artistID)+"','"+str(songID)+"',"+str(5)+",'"+str(datetime.datetime.now())+"')"
			print(rate_song_query)
			c.execute(rate_song_query)

			# rate album
			query = "INSERT INTO RateAlbums (Rater_User_ID, Owner_User_ID, Name, Stars, Rate_Date) SELECT "+"'"+str(artistID)+"','"+str(artistID)+"','"+str(albumName)+"',"+str(5)+",'"+str(datetime.datetime.now())+ "' WHERE NOT EXISTS (SELECT 1 FROM RateAlbums WHERE Name = '"+albumName+"')"
			c.execute(query)
			'''
			try:
				form = EventsForm(data_dict)
				if form.is_valid():
					form.save()
				else:
					logging.getLogger("error_logger").error(form.errors.as_json())
			except Exception as e:
				logging.getLogger("error_logger").erro2r(form.errors.as_json())
				pass
				'''
	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		#messages.error(request,"Unable to upload file. "+repr(e))
	#return HttpResponseRedirect(reverse("homepage"))
	return render(request, 'upload_content.html')

def upload_csv(request):
	data = {}
	if "GET" == request.method:
		print("test")
		return render(request, "upload_csv.html", data)

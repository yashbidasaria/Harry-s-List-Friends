from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Users(models.Model):
    User_ID = models.CharField(max_length= 32, primary_key = True)
    Email = models.CharField(max_length=32)
    Name = models.CharField(max_length=32)
    Password = models.CharField(max_length=32)
    Is_Artist = models.IntegerField()

    class meta:
        db_table = 'Users'

class Basic(models.Model):
    User_ID = models.ForeignKey('Users',on_delete=models.CASCADE)
    DOB = models.DateField()

    class meta:
        db_table = 'Basic'

class Artist(models.Model):
    User_ID = models.ForeignKey('Users',on_delete=models.CASCADE)
    Location = models.CharField(max_length=32)
    Most_Popular_Album_Name = models.IntegerField()
    Most_Popular_Song_ID = models.CharField(max_length=32)

    class meta:
        db_table = 'Artist'

class Song(models.Model):
    Song_ID = models.CharField(max_length=32, primary_key = True)
    User_ID = models.ForeignKey('Users',on_delete=models.CASCADE)
    Album_Name = models.ForeignKey('Album', on_delete=models.CASCADE)
    Name = models.CharField(max_length=32)
    Plays = models.IntegerField()

    class meta:
        db_table = 'Song'

class Album(models.Model):
    User_ID = models.ForeignKey('Users', on_delete=models.CASCADE)
    Name = models.CharField(max_length=32)
    Year = models.IntegerField()

    class meta:
        db_table = 'Album'

class Admin(models.Model):
    Admin_ID = models.IntegerField(primary_key = True)
    Admin_Email = models.CharField(max_length=32)
    Name = models.CharField(max_length=32)
    Password = models.CharField(max_length=32)

    class meta:
        db_table = 'Admin'

class Review(models.Model):
    Review_ID = models.IntegerField(primary_key = True)
    Song_ID = models.ForeignKey('Song', on_delete=models.CASCADE)
    Admin_ID = models.ForeignKey('Admin')
    Deleted = models.IntegerField()
    Reviewed = models.IntegerField()
    Flagged_Date = models.DateField()
    Review_Date = models.DateField()

    class meta:
        db_table = 'Review'

class RateAlbums(models.Model):
    Rate_Album_ID = models.IntegerField(primary_key = True)
    Rater_User_ID = models.ForeignKey('Users')
    Owner_User_ID = models.ForeignKey('Artist', on_delete=models.CASCADE)
    Name = models.ForeignKey('Album', on_delete=models.CASCADE)
    Stars = models.IntegerField()
    Rate_Date = models.DateField()

    class meta:
        db_table = 'RateAlbums'

class RateSongs(models.Model):
    Rate_Song_ID = models.IntegerField(primary_key = True)
    Rater_User_ID = models.ForeignKey('Users')
    Song_ID = models.ForeignKey('Song', on_delete=models.CASCADE)
    Stars = models.IntegerField()
    Rate_Date = models.DateField()

    class meta:
        db_table = 'RateSongs'

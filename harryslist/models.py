from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Users(models.Model):
    User_ID = models.CharField(primary_key = True)
    Email = models.CharField()
    Name = models.CharField()
    Password = models.CharField()
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
    Location = models.CharField()
    Most_Popular_Album_Name = models.IntegerField()
    Most_Popular_Song_ID = models.CharField()
	
    class meta:
        db_table = 'Artist'

class Song(models.Model):
    Song_ID = models.CharField(primary_key = True)
    User_ID = models.ForeignKey('Users',on_delete=models.CASCADE)
    Album_Name = models.ForeignKey('Album', on_delete=models.CASCASE,)
    Name = models.CharField()
    Plays = models.IntegerField()

    class meta:
        db_table = 'Song'

class Album(models.Model):
    User_ID = models.ForeignKey('Users', on_delete=model.CASCADE)
    Name = models.CharField()
    Year = models.IntegerField()

    class meta:
        db_table = 'Album'

class Admin(models.Model):
    Admin_ID = models.IntegerField(primary_key = True)
    Admin_Email = models.CharField()
    Name = models.CharField()
    Password = models.CharField()

    class meta:
        db_table = 'Admin'

class Review(models.Model):
    Review_ID = models.IntegerField(primary_key = True)
    Song_ID = models.ForeignKey('Song', on_delete=model.CASCADE)
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
    Owner_User_ID = models.ForeignKey('Users', on_delete=model.CASCADE)
    Name = models.ForeignKey('Album', on_delete=model.CASCADE_
    Stars = models.IntegerKey()
    Rate_Date = models.DateField()
    
    class meta:
        db_table = 'RateAlbums'

class RateSongs(models.Model):
    Rate_Song_ID = models.IntegerField(primary_key = True)
    Rater_User_ID = models.ForeignKey('Users')
    Song_ID = models.ForeignKey('Song', on_delete=model.CASCADE_
    Stars = models.IntegerKey()
    Rate_Date = models.DateField()
    
    class meta:
        db_table = 'RateSongs'



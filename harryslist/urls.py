from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from harryslist import views as core_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^top_artists/$', views.top_artists, name='top_artists'),
    url(r'^artists_otd/$', views.artists_otd, name='artists_otd'),
    url(r'^top_albums/$', views.top_albums, name='top_albums'),
    url(r'^top_songs/$', views.top_songs, name='top_songs'),
    url(r'^search/$', views.search, name='search'),
    url(r'^about/$', views.about, name='about'),
    url(r'^upload/csv/$', views.upload_csv, name='upload_csv'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^ajax/flag_song/$', views.flag_song, name='flag_song'),
    url(r'^ajax/rate_song/$', views.rate_song, name='rate_song'),
    url(r'^ajax/rate_album/$', views.rate_album, name='rate_album')
]

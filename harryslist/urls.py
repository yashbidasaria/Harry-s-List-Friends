from django.conf.urls import url
#from mysite.core import views as core_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^top_artists/$', views.top_artists, name='top_artists'),
    url(r'^top_albums/$', views.top_albums, name='top_albums'),
    url(r'^top_songs/$', views.top_songs, name='top_songs'),
    url(r'^about/$', views.about, name='about'),
    url(r'^singup/$', views.signup, name='signup'),
]

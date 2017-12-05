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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=rawpassword)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

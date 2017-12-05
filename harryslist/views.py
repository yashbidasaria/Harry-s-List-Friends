from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView


# Create your views here.

def index(request):
    return render(request, 'index.html')

class HomeView(TemplateView):

    template_name = 'index.html'

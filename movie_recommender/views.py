from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse

from project_1.settings import env
import tmdbsimple as tmdb

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):
    response = tmdb.Movies(603).keywords()

    return TemplateResponse(request, "index.html", {'response':response})
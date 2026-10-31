from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse

from project_1.settings import env
import tmdbsimple as tmdb

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):
    responseA = str(tmdb.Search().movie(query="Parasite", year=2019))
    responseA = responseA.split("'id': ")[1]
    responseA = responseA.split(", 'title'")[0]

    response = tmdb.Movies(responseA).keywords()

    return TemplateResponse(request, "index.html", {'response':response})
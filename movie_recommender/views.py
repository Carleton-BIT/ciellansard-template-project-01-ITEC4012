from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse

from movie_recommender.models import Movie
from project_1.settings import env
import tmdbsimple as tmdb

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):

    movie_title = "T2 Trainspotting"
    movie_year = 2017

    movie_id = str(tmdb.Search().movie(query=movie_title, year=movie_year))
    movie_id = movie_id.split("'id': ")[1]
    movie_id = movie_id.split(", 'title'")[0]

    #movie_link_letterboxd = f'https://letterboxd.com/film/{movie_title}{"-" + movie_year}/'

    movie_info = tmdb.Movies(movie_id).info()

    new_movie = Movie.create(

        tmdb_id = movie_id,
        title = movie_title,
        year = movie_year,
        # keywords=movie_keywords,
        # genres=movie_genres,
        rating = round(tmdb.Movies(movie_id).info()['vote_average'], 1),
        votes = tmdb.Movies(movie_id).info()['vote_count'],
        length = tmdb.Movies(movie_id).info()['runtime'],
        tmdb_link = f'https://www.themoviedb.org/movie/{movie_id}',
        poster_path = tmdb.Movies(movie_id).info()['poster_path'],
    ).save()



    return TemplateResponse(request, "index.html", {
        'movies': Movie.objects.all()
    })
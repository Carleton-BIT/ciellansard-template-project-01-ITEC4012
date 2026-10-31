from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse

from project_1.settings import env
import tmdbsimple as tmdb

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):
    movie_title = "Hackers"
    movie_year = 1995

    movie_id = str(tmdb.Search().movie(query=movie_title, year=movie_year))
    movie_id = movie_id.split("'id': ")[1]
    movie_id = movie_id.split(", 'title'")[0]

    movie_keywords = tmdb.Movies(movie_id).keywords()
    movie_genres = tmdb.Movies(movie_id).info()['genres']
    movie_rating = round(tmdb.Movies(movie_id).info()['vote_average'], 1)
    movie_votes = tmdb.Movies(movie_id).info()['vote_count']
    movie_length = tmdb.Movies(movie_id).info()['runtime']
    movie_link_tmdb = f'https://www.themoviedb.org/movie/{movie_id}'
    movie_poster_path = tmdb.Movies(movie_id).info()['poster_path']
    #movie_link_letterboxd = f'https://letterboxd.com/film/{movie_title}{"-" + movie_year}/'

    movie_info = tmdb.Movies(movie_id).info()

    return TemplateResponse(request, "index.html", {
        'title':movie_title,
        'year': movie_year,
        'id': movie_id,
        'keywords': movie_keywords,
        'genres': movie_genres,
        'rating': movie_rating,
        'votes': movie_votes,
        'length': movie_length,
        'link': movie_link_tmdb,
        'poster_path': movie_poster_path,
        'info': movie_info,
    })
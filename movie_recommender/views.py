from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse

from movie_recommender.models import Movie, Keyword
from project_1.settings import env
import tmdbsimple as tmdb

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):

    movie_title = "Coraline"
    movie_year = 2009

    movie_id = str(tmdb.Search().movie(query=movie_title, year=movie_year))
    movie_id = movie_id.split("'id': ")[1]
    movie_id = movie_id.split(", 'title'")[0]

    movie_keywords = str(tmdb.Movies(movie_id).keywords())
    num_keywords = movie_keywords.count(', \'name\': ')
    keywords = []

    for i in range(1, num_keywords + 1):
        keyword_id = movie_keywords.split('\'id\': ')[i + 1]
        keyword_id = keyword_id.split(',')[0]

        keyword_name = movie_keywords.split('\'name\': \'')[i]
        keyword_name = keyword_name.split('\'')[0]

        keywords.append(keyword_id)

        new_keyword = Keyword.create(
            keyword_id=keyword_id,
            keyword_name=keyword_name
        )
        new_keyword.save()

    # movie_genres = tmdb.Movies(movie_id).info()['genres']
    #movie_link_letterboxd = f'https://letterboxd.com/film/{movie_title}{"-" + movie_year}/'

    Movie.create(
        tmdb_id = movie_id,
        title = movie_title,
        year = movie_year,
        # genres=movie_genres,
        rating = round(tmdb.Movies(movie_id).info()['vote_average'], 1),
        votes = tmdb.Movies(movie_id).info()['vote_count'],
        length = tmdb.Movies(movie_id).info()['runtime'],
        tmdb_link = f'https://www.themoviedb.org/movie/{movie_id}',
        poster_path = tmdb.Movies(movie_id).info()['poster_path'],
    ).save()

    Movie.set_keywords(Movie.objects.get(id=movie_id), keywords)

    return TemplateResponse(request, "index.html", {
        'movies': Movie.objects.all(),
        'keywords': Movie.objects.get(id = movie_id).keywords.all(),
    })
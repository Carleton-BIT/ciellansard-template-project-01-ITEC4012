from django.contrib.sites import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse


from movie_recommender.models import Movie, Keyword
from project_1.settings import env, TMDB_API_KEY, TMDB_BEARER_TOKEN
import tmdbsimple as tmdb
from .utils import get_movies_matching_keywords, get_data_from_submitted_file, add_movie_if_new

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):

    mvs = []

    keywords_to_search = ["3335", "1576", "4344"]

    titles, years, ratings = get_data_from_submitted_file()

    for title in titles:
        title_idx = titles.index(title)

        movie_title = title
        movie_year = years[title_idx]

        movie_id = str(tmdb.Search().movie(query=movie_title, year=movie_year))
        if movie_id.count("id") == 0 or movie_id.count("title") == 0:
            continue
        movie_id = movie_id.split("'id': ")[1]
        movie_id = movie_id.split(", 'title'")[0]

        new_movie = add_movie_if_new(movie_id, movie_title, movie_year, ratings[title_idx], title_idx)

        if new_movie is not None:
            mvs.append(new_movie)


    return TemplateResponse(request, "index.html", {
        'movies': mvs,
        'results' : get_movies_matching_keywords(["1"])#(keywords_to_search)
    })
from django.contrib.sites import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse
import requests

from movie_recommender.models import Movie, Keyword
from project_1.settings import env, TMDB_API_KEY, TMDB_BEARER_TOKEN
import tmdbsimple as tmdb
import csv

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):
    titles = []
    years = []
    ratings = []

    mvs = []
    # kws = []
    rts = []

    keywords_to_search = ["2187", "295702"]

    rt = requests.get(
        f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_count.desc&api_key={TMDB_API_KEY}&with_keywords={",".join(keywords_to_search)}',
        headers={
            'Authorization' : f'Bearer {TMDB_BEARER_TOKEN}',
            #'accept': 'application/json'
        }
    ).json()

    # with open(env('CSV_PATH'), "r") as file:
    #     data = csv.reader(file)
    #     row_idx = 0
    #     for row in data:
    #         if row_idx != 0:
    #             titles.append(row[1])
    #             years.append(row[2])
    #             ratings.append(row[4])
    #         row_idx += 1

    # for title in titles:
    #     movie_title = title
    #     movie_year = years[titles.index(title)]
    #
    #     movie_id = str(tmdb.Search().movie(query=movie_title, year=movie_year))
    #
    #     if movie_id.count("id") == 0 or movie_id.count("title") == 0:
    #         continue
    #
    #     movie_id = movie_id.split("'id': ")[1]
    #     movie_id = movie_id.split(", 'title'")[0]
    #
    #     if not Movie.objects.filter(id=movie_id).exists():
    #         movie = tmdb.Movies(movie_id)
    #
    #         movie_keywords = str(movie.keywords())
    #         num_keywords = movie_keywords.count(', \'name\': ')
    #         if num_keywords == 0 or movie_keywords.count("id") == 0:
    #             continue
    #
    #         keywords = []
    #
    #         for i in range(1, num_keywords):
    #             keyword_id = movie_keywords.split('\'id\': ')[i + 1]
    #             keyword_id = keyword_id.split(',')[0]
    #
    #             if movie_keywords.count('\'name\': \'') == 0:
    #                 break
    #             keyword_name = movie_keywords.split('\'name\': \'')[i]
    #             keyword_name = keyword_name.split('\'')[0]
    #
    #             keywords.append(keyword_id)
    #
    #             new_keyword = Keyword.create(
    #                 keyword_id=keyword_id,
    #                 keyword_name=keyword_name
    #             )
    #             if new_keyword is not None:
    #                 new_keyword.save()
    #
    #         # movie_genres = movie.info()['genres']
    #         #movie_link_letterboxd = f'https://letterboxd.com/film/{movie_title}{"-" + movie_year}/'
    #
    #         new_movie = Movie.create(
    #             title = movie_title,
    #             year = movie_year,
    #             tmdb_id=movie_id,
    #             # genres=movie_genres,
    #             audience_rating = round(movie.info()['vote_average'], 1),
    #             user_rating = ratings[titles.index(title)],
    #             votes = movie.info()['vote_count'],
    #             length = movie.info()['runtime'],
    #             tmdb_link = f'https://www.themoviedb.org/movie/{movie_id}',
    #             poster_path = movie.info()['poster_path'],
    #         )
    #
    #         if new_movie is not None:
    #             new_movie.save()
    #             Movie.set_keywords(Movie.objects.get(id=movie_id), keywords)
    #
    #     mvs.append(Movie.objects.get(id=movie_id))
    #     kws.append(Movie.objects.get(id=movie_id).keywords)

    return TemplateResponse(request, "index.html", {
        'movies': mvs,
        # 'keywords': kws,
        # 'list' : zip(titles, years)
        'results' : rt
    })
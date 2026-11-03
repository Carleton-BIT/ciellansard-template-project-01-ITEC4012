import csv

from django.contrib.sites import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import response
from django.template.response import TemplateResponse


from movie_recommender.models import Movie, Keyword
from project_1.settings import env, os, MEDIA_ROOT, TMDB_API_KEY, TMDB_BEARER_TOKEN
import tmdbsimple as tmdb
from .utils import get_and_save_movies_matching_keywords, get_data_from_submitted_file, add_movie_if_new
import random
from .forms import FileUploadForm

tmdb.API_KEY = env('TMDB_API_KEY')

def index(request):

    movies = []

    titles, years, ratings = get_data_from_submitted_file()

    # for title in titles:
    #     title_idx = titles.index(title)
    #
    #     movie_title = title
    #     movie_year = years[title_idx]
    #
    #     movie_id = str(tmdb.Search().movie(query=movie_title, year=movie_year))
    #     if movie_id.count("id") == 0 or movie_id.count("title") == 0:
    #         continue
    #     movie_id = movie_id.split("'id': ")[1]
    #     movie_id = movie_id.split(", 'title'")[0]
    #
    #     new_movie = add_movie_if_new(movie_id, movie_title, movie_year, ratings[title_idx])
    #
    #     if new_movie is not None:
    #         movies.append(new_movie)


    all_keywords = []
    all_keyword_weights = []

    keywords = []
    keyword_weights = []

    positivity_threshold = 3.0 # Any movie rated higher than this is 'good'; de-value keywords from lower-rated movies
    weight_modifier = 1.0 # Lower = less bias, higher = bias towards favourite keywords

    # for movie in movies:
    #     m = Movie.objects.filter(id=movie.id).first()
    #     if m is not None:
    #         new_keywords = m.keywords.all()
    #
    #         w = (float(m.user_rating) - positivity_threshold) * weight_modifier
    #
    #         for keyword in new_keywords:
    #             if keyword not in all_keywords:
    #                 all_keywords.append(keyword)
    #                 all_keyword_weights.append(w)
    #             else:
    #                 all_keyword_weights[all_keywords.index(keyword)] += w
    #
    # for keyword in all_keywords:
    #     if all_keyword_weights[all_keywords.index(keyword)] > 0:
    #         keywords.append(keyword)
    #         keyword_weights.append(all_keyword_weights[all_keywords.index(keyword)])

    num_keywords_to_search = 5
    selected_keywords = []#selected_keyword = random.choices(keywords, weights=keyword_weights, k=num_keywords_to_search)

    # while len(selected_keywords) < num_keywords_to_search:
    #     selected_keyword = random.choices(keywords, weights=keyword_weights, k=1)[0]
    #     if selected_keyword not in selected_keywords:
    #         selected_keywords.append(selected_keyword)
    #
    # keywords_to_search = []
    # for keyword in selected_keywords:
    #     keywords_to_search.append(str(keyword.id))


    # results = get_and_save_movies_matching_keywords(keywords_to_search)

    num_results_to_pick = 10

    # results.sort(key=lambda x: x.match_strength, reverse=True)

    results_to_show = []

    # for result in results:
    #     if num_results_to_pick == 0:
    #         break
    #     if result not in movies and result not in results_to_show:
    #         results_to_show.append(result)
    #         num_results_to_pick -= 1


    return TemplateResponse(request, "index.html", {
        'movies': [],
        'keywords_to_search': [],
        'keywords': zip([], []),
        'results' : []
    })


# Based on https://medium.com/@brahim_idbendriss/how-to-upload-and-store-a-file-using-htmx-in-a-django-project-9e82cf3bb4b8
def file_submission(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Make sure new file is valid
            # uploaded_file = form.cleaned_data['upload_your_letterboxd_ratings']
            # if uploaded_file.content_type != 'text/csv': # check formatting?
            #     return render(request, 'file_submission.html',{'form': form, 'error_message': 'Uploaded file must be .csv'})

            # # Delete old uploaded files
            # upload_dir = os.path.join(MEDIA_ROOT, 'uploads')
            # for file in os.listdir(upload_dir):
            #     os.remove(os.path.join(upload_dir, file))
            #
            # Save new file to uploads directory
            #os.makedirs("../media/uploads", exist_ok=True)
            # file_path = os.path.join("../media/uploads", str(uploaded_file.name))
            #
            # with open("../media/uploads", str(uploaded_file.name)) as csv_file:
            #     csv_writer = csv.writer(csv_file, delimiter=',',
            #                                  quotechar='"',
            #                                  quoting=csv.QUOTE_MINIMAL)
            #     for row in csv_file:
            #         csv_writer.writerow(row)

            return render(request, 'index.html', {
                'form': form,
                'success_message': 'File uploaded successfully'
            })
    else:
        form = FileUploadForm()

    return TemplateResponse(request, "index.html", {'form': form})
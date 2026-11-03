import requests, csv
from project_1.settings import env, TMDB_API_KEY, TMDB_BEARER_TOKEN
from movie_recommender.models import Movie, Keyword
import tmdbsimple as tmdb



# Given a list of keywords, find the most voted movies with n, n-1, n-2 ... 1 matching keywords
def get_and_save_movies_matching_keywords(keywords_to_search):
    num_keywords = len(keywords_to_search)
    results = [""]

    # Search for movies that meet ALL keywords
    results[0] = requests.get(
        f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_count.desc&api_key={TMDB_API_KEY}&with_keywords={",".join(keywords_to_search)}',
        headers={
            'Authorization' : f'Bearer {TMDB_BEARER_TOKEN}'
        }
    ).json()

    # Then, search for movies that meet n - 1, n - 2 ... 1 keywords
    for i in reversed(range(1, num_keywords)):
        results.append("")

        for j in range(num_keywords):
            keyword_subset = []

            for k in range(i):
                keyword_subset.append(keywords_to_search[(k + j)%(i + 1)])

            result_subset = requests.get(
                                f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_count.desc&api_key={TMDB_API_KEY}&with_keywords={",".join(keyword_subset)}',
                                headers={
                                    'Authorization': f'Bearer {TMDB_BEARER_TOKEN}'
                                }
                            ).json()

            results[num_keywords - i] += str(result_subset)


    movies = []

    for result in results:
        result = str(result)

        num_movies = result.count('\'id\': ')
        if num_movies == 0 or result.count('\'title\': \'') < 1 or result.count('\'release_date\': \'') < 1 or result.count('\'release_date\': \'') < 1:
            continue

        movie_idx = 0

        for i in range(num_movies):
            movie_id = ""
            movie_title = ""
            movie_year = ""
            try:
                movie_id = result.split('\'id\': ')[movie_idx + 1]
                movie_id = movie_id.split(',')[0]

                movie_title = result.split('\'title\': \'')[movie_idx + 1]
                movie_title = movie_title.split('\',')[0]

                movie_year = result.split('\'release_date\': \'')[movie_idx + 1]
                movie_year = movie_year.split('-')[0]
            except IndexError:
                continue

            new_movie = add_movie_if_new(movie_id, movie_title, movie_year, 0.0)
            Movie.objects.filter(id=movie_id).update(match_strength=len(results) - results.index(result))

            if new_movie is not None:
                movies.append(new_movie)

            movie_idx += 1

    return movies



# Check if string can be converted to float
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False



# Extract the title, year, and user's rating of each movie (row in csv file)
def get_data_from_submitted_file():
    titles = []
    years = []
    ratings = []

    with (open(env('CSV_PATH'), "r") as file):
        data = csv.reader(file)
        row_idx = 0
        for row in data:
            if row_idx != 0:
                title = row[1]
                year = row[2]
                rating = row[4]

                if len(title) > 0 and year.isnumeric() and is_float(rating) and 0.5 <= float(rating) <= 5.0:
                    titles.append(title)
                    years.append(year)
                    ratings.append(rating)
                else:
                   continue
            row_idx += 1

    return titles, years, ratings



# Given a movie, get its keywords and save new ones in the DB
def get_and_save_movie_keywords(movie):
    movie_keywords = str(movie.keywords())
    num_keywords = movie_keywords.count(', \'name\': ')
    if num_keywords == 0 or movie_keywords.count("id") == 0:
        return None

    keywords = []

    for i in range(1, num_keywords):
        keyword_id = movie_keywords.split('\'id\': ')[i + 1]
        keyword_id = keyword_id.split(',')[0]

        if movie_keywords.count('\'name\': \'') == 0:
            break

        keyword_name = ""
        try:
            keyword_name = movie_keywords.split('\'name\': \'')[i]
        except IndexError:
            continue
        keyword_name = keyword_name.split('\'')[0]

        keywords.append(keyword_id)

        new_keyword = Keyword.create(
            keyword_id=keyword_id,
            keyword_name=keyword_name
        )
        if new_keyword is not None:
            new_keyword.save()

    return keywords



# Create a movie and create/set related keywords if a movie at the same id does not exist
def add_movie_if_new(movie_id, movie_title, movie_year, movie_rating):
    if not Movie.objects.filter(id=movie_id).exists():
        movie = tmdb.Movies(movie_id)
        info = movie.info()

        # movie_genres = movie.info()['genres']
        # movie_link_letterboxd = f'https://letterboxd.com/film/{movie_title}{"-" + movie_year}/'

        new_movie = Movie.create(
            title=movie_title,
            year=movie_year,
            tmdb_id=movie_id,
            # genres=movie_genres,
            audience_rating=round(movie.info()['vote_average'], 1),
            user_rating=movie_rating,
            votes=info['vote_count'],
            length=info['runtime'],
            tmdb_link=f'https://www.themoviedb.org/movie/{movie_id}',
            poster_path=info['poster_path'],
        )

        if new_movie is not None:
            new_movie.save()
            keywords = get_and_save_movie_keywords(movie)
            if keywords is not None:
                Movie.set_keywords(Movie.objects.get(id=movie_id), keywords)

    else:
        Movie.objects.filter(id=movie_id).update(user_rating=movie_rating)

    return Movie.objects.get(id=movie_id)
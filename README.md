# Project 1

This project is a movie recommender that recommends unwatched movies with the same keywords as the user's favourite movies. It looks at the user's Letterboxd ratings, finds these movies and their associated keywords on TMDB, then searches for & presents similar movies. Letterboxd data is given in the form of a .csv file (no API use/web scraping) and the TMDB data is retrieved using the TMDB API (https://developer.themoviedb.org/docs/getting-started). 

https://github.com/user-attachments/assets/a5177aa5-d802-48a6-840c-283f8b12b66e

_Video taken of the app in action (locally)._

## Setup to run locally
1. Clone the repository and open it in Pycharm
2. Add a new Python 3.14 interpreter of type 'Virtualenv', if one is not already set up.
3. Open a terminal in Pycharm and paste in the following commands: 
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
4. If you do not have a TMDB account or TMDB API key/Bearer token, [create an account and request API access]([url](https://www.themoviedb.org/settings/api/request)) for personal use: https://www.themoviedb.org/settings/api/request
5. Find your API key at the bottom of [this page.]([url](https://www.themoviedb.org/settings/api)): https://www.themoviedb.org/settings/api
6. Find your bearer token by going to https://developer.themoviedb.org/reference/account-details and, on the right side, click `CREDENTIALS > Header` and hit the lock icon to reveal the token.
7. Create a file named `.env` and paste in the following. Replace the blanks with your TMDB API key and bearer token respectively.
```
# Used by some security features. This value is fine for local development
# only; the production server generates its own key.
SECRET_KEY=django-insecure-local-development-only

# Credentials required to use the TMDB API
TMDB_API_KEY="__________"
TMDB_BEARER_TOKEN="__________"

# Show detailed error pages. Must never be True on a public server.
DEBUG=False

# Domains the server can run on, comma-separated.
ALLOWED_HOSTS=localhost,127.0.0.1

# Addresses that are allowed to submit forms to the server, comma-separated,
# including http:// or https://.
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Location of the application database.
DATABASE_URL=sqlite:///db.sqlite3

# Location of static files (e.g. css, images) gathered by collectstatic.
STATIC_ROOT=staticfiles

# Location of uploaded files.
MEDIA_ROOT=media
```
8. Run the following commands and say "yes" if asked to confirm your actions. These should prepare the database and static files (images, css).
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```
9. Start the server using `python manage.py runserver`, then access it at http://localhost:8000.
10. You will need to give the site a .csv file containing a Letterboxd user's movie ratings. If you have a Letterboxd account find this by going to `Settings > Data > Export Your Data`, unzipping the folder it produces, and looking for the 'ratings.csv' file. If not, feel free to use this sample [ratings.csv](https://github.com/user-attachments/files/34306987/ratings.csv). 

Note that the longer the .csv file, the more keywords to search, and more recommendations desired, the longer the loading time will be. 

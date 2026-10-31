from django.db import models

class Keyword(models.Model):
    keyword_id = models.IntegerField()
    keyword_name = models.CharField(max_length=100)

class Genre(models.Model):
    genre_id = models.IntegerField()
    genre_name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    tmdb_id = models.IntegerField()
    keywords = models.ManyToManyField(Keyword)
    genres = models.ManyToManyField(Genre)
    rating = models.FloatField()
    votes = models.IntegerField()
    length = models.IntegerField()
    tmdb_link = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)

    @classmethod
    def create(cls, title, year, tmdb_id, rating, votes, length, tmdb_link, poster_path):
        Movie.objects.filter(title=title, year=year).delete()
        movie = cls(
            title=title,
            year=year,
            tmdb_id=tmdb_id,
            # keywords=keywords,
            # genres=genres,
            rating=rating,
            votes=votes,
            length=length,
            tmdb_link=tmdb_link,
            poster_path=poster_path
        )
        return movie
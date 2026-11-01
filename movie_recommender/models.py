from django.db import models

class Keyword(models.Model):
    #keyword_id = models.IntegerField()
    keyword_name = models.CharField(max_length=100)

    @classmethod
    def create(cls, keyword_id, keyword_name):
        if Keyword.objects.filter(id=keyword_id).exists():
            return None
        keyword = cls(
            id = keyword_id,
            #keyword_id=keyword_id,
            keyword_name=keyword_name
        )
        return keyword


class Genre(models.Model):
    genre_id = models.IntegerField()
    genre_name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    #tmdb_id = models.IntegerField()
    keywords = models.ManyToManyField(Keyword, related_name='movies')
    #genres = models.ManyToManyField(Genre)
    audience_rating = models.FloatField()
    user_rating = models.FloatField()
    votes = models.IntegerField()
    length = models.IntegerField()
    tmdb_link = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100)

    @classmethod
    def create(cls, title, year, tmdb_id, audience_rating, user_rating, votes, length, tmdb_link, poster_path):
        if Movie.objects.filter(id=tmdb_id).exists():
            return None
        movie = cls(
            title=title,
            year=year,
            id = tmdb_id,
            #tmdb_id=tmdb_id,
            # genres=genres,
            #keywords=Keyword.create(keyword_id=0, keyword_name=""),
            audience_rating=audience_rating,
            user_rating=user_rating,
            votes=votes,
            length=length,
            tmdb_link=tmdb_link,
            poster_path=poster_path
        )
        return movie

    def set_keywords(self, keyword_ids):
        keywords = []
        for keyword_id in keyword_ids:
            keywords.append(Keyword.objects.get(id=keyword_id))

        self.keywords.set(keywords)
        return self
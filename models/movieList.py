from peewee import *

db = SqliteDatabase('MovieNight.db')


class Tag(Model):
    genre_id = IntegerField(primary_key=True)

    class Meta:
        database = db


class Movie(Model):
    tmdb_id = IntegerField(primary_key=True)
    name = CharField(primary_key=False)
    genre_tags = ForeignKeyField(Tag, backref='movies', default=None)

    class Meta:
        database = db


class MovieList(Model):
    guild = IntegerField(primary_key=True)
    tmdb_id = ForeignKeyField(Movie, backref="movie_lists", default=None)

    class Meta:
        database = db



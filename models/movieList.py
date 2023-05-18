from peewee import *

db = SqliteDatabase('MovieNight.db')


class MovieList(Model):
    guild = IntegerField(primary_key=True)

    class Meta:
        database = db


class MovieListItem(Model):
    tmdb_id = IntegerField()
    name = CharField()
    movie_list = ForeignKeyField(MovieList, backref='movie_list_item', default=None)

    class Meta:
        database = db
        primary_key = CompositeKey('tmdb_id', 'movie_list')


class Watched(Model):
    guild = ForeignKeyField(MovieList, backref='watched', default=None)
    movie = ForeignKeyField(MovieListItem, backref='watched', default=None)
    user = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('guild', 'movie', 'user')

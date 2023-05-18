from peewee import *

db = SqliteDatabase('MovieNight.db')


class BaseModel(Model):
    class Meta:
        database = db


class MovieList(BaseModel):
    guild = IntegerField(primary_key=True)
    library_channel_id = IntegerField()


class MovieListItem(BaseModel):
    id = AutoField()
    tmdb_id = IntegerField()
    name = CharField()
    guild = ForeignKeyField(MovieList, backref='movie_list_item')

    class Meta:
        indexes = (
            (('tmdb_id', 'guild'), True),
        )


class Watched(BaseModel):
    id = AutoField()
    guild = ForeignKeyField(MovieList, backref='watched')
    movie = ForeignKeyField(MovieListItem, backref='watched')
    user = IntegerField()

    class Meta:
        indexes = (
            (('guild', 'movie', 'user'), True),
        )

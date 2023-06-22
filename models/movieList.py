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
    guild = ForeignKeyField(MovieList, backref='movie_list_item', on_delete="CASCADE")

    class Meta:
        indexes = (
            (('tmdb_id', 'guild'), True),
        )


class Watched(BaseModel):
    id = AutoField()
    guild = ForeignKeyField(MovieList, backref='watched', on_delete="CASCADE")
    movie = ForeignKeyField(MovieListItem, backref='watched', on_delete="CASCADE")
    user = IntegerField()

    class Meta:
        indexes = (
            (('guild', 'movie', 'user'), True),
        )


class VoteList(BaseModel):
    id = AutoField()
    guild = ForeignKeyField(MovieList, backref='vote', on_delete="CASCADE")
    created_by_user = IntegerField()

    class Meta:
        indexes = (
            (('guild', 'created_by_user'), True),
        )


class VoteListItem(BaseModel):
    id = AutoField()
    vote_list = ForeignKeyField(VoteList, backref='vote', on_delete="CASCADE")
    movie = ForeignKeyField(MovieListItem, backref='vote', on_delete="CASCADE")
    movie_title = CharField()

    class Meta:
        indexes = (
            (('vote_list', 'movie'), True),
        )


class UserRanking(BaseModel):
    vote_movie = ForeignKeyField(VoteListItem, backref='user_rankings', on_delete="CASCADE")
    user = IntegerField()
    ranking = IntegerField()

    class Meta:
        indexes = (
            (('vote_movie', 'user'), True),
        )

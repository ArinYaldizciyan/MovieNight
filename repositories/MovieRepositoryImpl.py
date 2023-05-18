import abc
from models.movieList import MovieList, MovieListItem
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class MovieRepository:
    def __init__(self):
        pass

    def create_movie_list(self, movie_list_data: MovieListData):
        MovieList.get_or_create(guild=movie_list_data.guild, library_channel_id=movie_list_data.library_channel_id)
        return True

    def add_to_list(self, movie_data: MovieListItemData):
        MovieListItem.get_or_create(tmdb_id=movie_data.tmdb_id, guild=movie_data.guild, name=movie_data.name)
        return True

    def add_to_watched(self, movie_data: MovieListItemData):
        movie_list = MovieList.get_or_create(guild=movie_data.guild)
        MovieListItem.get_or_create(tmdb_id=movie_data.tmdb_id, movie_list=movie_data.guild, name=movie_data.name)
        return True


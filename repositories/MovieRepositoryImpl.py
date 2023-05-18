import abc
from models.movieList import MovieList, MovieListItem
from data import MovieListItemData


class MovieRepository:
    def __init__(self):
        pass

    def add_to_list(self, movie_data: MovieListItemData):
        movie_list = MovieList.get_or_create(guild=movie_data.guild)
        MovieListItem.get_or_create(tmdb_id=movie_data.tmdb_id, movie_list=movie_data.guild, name=movie_data.name)
        return True


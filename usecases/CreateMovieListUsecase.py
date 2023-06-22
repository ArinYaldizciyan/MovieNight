import interactions
from injector import inject
from typing import Optional
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class CreateMovieListUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, guild, library_channel_id: int):
        # Check if movie list exists and channel is created
        movie_list_data = MovieListData(guild=guild, library_channel_id=library_channel_id)
        self.movie_repository.create_movie_list(movie_list_data)

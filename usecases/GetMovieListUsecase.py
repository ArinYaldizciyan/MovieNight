import interactions
from injector import inject
from typing import Optional
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class GetMovieListUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, guild: int) -> Optional[MovieListData]:
        return self.movie_repository.get_movie_list(guild)

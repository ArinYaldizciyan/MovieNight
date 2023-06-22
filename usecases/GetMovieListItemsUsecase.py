import interactions
from injector import inject
from typing import Optional, List
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class GetMovieListItemsUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, guild: int, movie_id: int) -> List[MovieListItemData]:
        return self.movie_repository.get_movie_list_items(guild, movie_id)

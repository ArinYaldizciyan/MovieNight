import interactions
from injector import inject
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class GetListDetailsUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, movie_data: MovieListItemData, movie_list_data: MovieListData):
        pass
    
import interactions
from injector import inject
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class AddToMovieListUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, movie_data: MovieListItemData, movie_list_data: MovieListData):
        # Check if movie list exists and channel is created
        self.movie_repository.create_movie_list(movie_list_data)
        self.movie_repository.add_to_list(movie_data)

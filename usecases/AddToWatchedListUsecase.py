import interactions
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData


class AddToMovieListUsecase:
    def __init__(self):
        self.movie_repository = MovieRepository()

    def execute(self, movie_data: MovieListItemData):
        self.movie_repository.add_to_list(movie_data)

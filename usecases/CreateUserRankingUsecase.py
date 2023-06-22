import interactions
from injector import inject
from typing import Optional
from repositories.MovieRepositoryImpl import MovieRepository
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData


class CreateUserRankingUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, vote_list_item_id: int, user: int, ranking: int):
        # Check if movie list exists and channel is created
        return self.movie_repository.add_to_ranking(
            vote_list_item_id=vote_list_item_id,
            user=user,
            ranking=ranking)

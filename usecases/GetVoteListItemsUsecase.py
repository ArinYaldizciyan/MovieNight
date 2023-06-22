from injector import inject
from typing import List
from repositories.MovieRepositoryImpl import MovieRepository
from data.VoteListItemData import VoteListItemData


class GetVoteListItemsUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, vote_list_id: int) -> List[VoteListItemData]:
        return self.movie_repository.get_vote_list_items(vote_list_id)

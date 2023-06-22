from injector import inject
from repositories.MovieRepositoryImpl import MovieRepository
from data.VoteListItemData import VoteListItemData


class AddToVoteListUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, vote_list_item_data: VoteListItemData):
        self.movie_repository.add_to_vote_list(vote_list_item_data)

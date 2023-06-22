from injector import inject
from repositories.MovieRepositoryImpl import MovieRepository
from data.VoteListData import VoteListData


class GetVoteListUsecase:

    @inject
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    def execute(self, vote_list: VoteListData) -> VoteListData:
        return self.movie_repository.get_vote_list(vote_list)

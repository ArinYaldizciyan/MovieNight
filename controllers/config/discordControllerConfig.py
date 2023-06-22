from interactions import Client, Intents
from injector import inject
from appCore.ParamManager import ParamManager
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from usecases.MovieAutocompleteUsecase import MovieAutocompleteUsecase
from usecases.SearchMoviesUsecase import SearchMovieUsecase
from usecases.GetWatchSourceUsecase import GetWatchSourceUsecase
from usecases.GetMovieListUsecase import GetMovieListUsecase
from usecases.CreateMovieListUsecase import CreateMovieListUsecase
from usecases.GetVoteListUsecase import GetVoteListUsecase
from usecases.AddToVoteListUsecase import AddToVoteListUsecase
from usecases.GetVoteListItemsUsecase import GetVoteListItemsUsecase
from usecases.GetMovieListItemsUsecase import GetMovieListItemsUsecase
from usecases.CreateUserRankingUsecase import CreateUserRankingUsecase


class DiscordControllerConfig:
    @inject
    def __init__(self,
                 add_to_movie_list: AddToMovieListUsecase,
                 movie_autocomplete: MovieAutocompleteUsecase,
                 search_movie: SearchMovieUsecase,
                 get_source: GetWatchSourceUsecase,
                 create_movie_list: CreateMovieListUsecase,
                 get_movie_list: GetMovieListUsecase,
                 get_vote_list: GetVoteListUsecase,
                 add_to_vote_list: AddToVoteListUsecase,
                 get_vote_list_items: GetVoteListItemsUsecase,
                 get_movie_list_items: GetMovieListItemsUsecase,
                 create_user_ranking: CreateUserRankingUsecase):
        self.p = ParamManager()
        self.bot: Client = Client(intents=Intents.ALL,
                                  asyncio_debug=True, sync_interactions=True)
        self.key = self.p.get_parameter('DISCORD_BOT_KEY', from_environment=True)

        self.bot.load_extension('controllers.DiscordController',
                                add_to_movie_list=add_to_movie_list,
                                movie_autocomplete=movie_autocomplete,
                                search_movie=search_movie,
                                get_source=get_source,
                                create_movie_list=create_movie_list,
                                get_movie_list=get_movie_list,
                                get_vote_list=get_vote_list,
                                add_to_vote_list=add_to_vote_list,
                                get_vote_list_items=get_vote_list_items,
                                get_movie_list_items=get_movie_list_items,
                                create_user_ranking=create_user_ranking)
        self.bot.start(self.key)

        print("loaded", self.__class__.__name__)

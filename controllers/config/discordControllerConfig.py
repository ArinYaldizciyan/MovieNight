from interactions import Client, Intents
from injector import inject
from appCore.ParamManager import ParamManager
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from usecases.MovieAutocompleteUsecase import MovieAutocompleteUsecase
from usecases.SearchMoviesUsecase import SearchMovieUsecase


class DiscordControllerConfig:
    @inject
    def __init__(self, add_to_movie_list: AddToMovieListUsecase, movie_autocomplete: MovieAutocompleteUsecase,
                 search_movie: SearchMovieUsecase):
        self.p = ParamManager()
        self.bot: Client = Client(intents=Intents.ALL, debug_scope=833127429853806592,
                                  asyncio_debug=True, sync_interactions=True)
        self.key = self.p.get_parameter('DISCORD_BOT_KEY', from_environment=True)

        self.add_movie = add_to_movie_list
        self.movie_autocomplete = movie_autocomplete
        self.search_movie = search_movie

        self.bot.load_extension('controllers.DiscordController', add_to_movie_list=self.add_movie,
                                movie_autocomplete=self.movie_autocomplete, search_movie=self.search_movie)
        self.bot.start(self.key)

        print("loaded", self.__class__.__name__)

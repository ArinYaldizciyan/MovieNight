import interactions, datetime
from interactions import Extension
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from usecases.MovieAutocompleteUsecase import MovieAutocompleteUsecase
from usecases.SearchMoviesUsecase import SearchMovieUsecase
from interactions import listen, slash_command, slash_option, OptionType, \
    SlashContext, AutocompleteContext, InteractionContext, ComponentCommand


class MovieController(Extension):
    def __init__(self, bot, key, tmdb_key):
        self.key = key
        self.tmdb_key = tmdb_key
        self.bot = bot
        self.add_to_movie_list = AddToMovieListUsecase()
        self.movie_autocomplete = MovieAutocompleteUsecase()
        self.search_movie = SearchMovieUsecase()

        print("loaded", self.__class__.__name__)

    @slash_command(
        name="about",
        description="Get Information about a Movie!"
    )
    @slash_option(
        name="movie",
        description="Movie to lookup",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    async def search(self, ctx: InteractionContext, movie: int):
        await ctx.defer(ephemeral=False)

        send = await self.search_movie.execute(movie_id=movie, tmdb_key=self.tmdb_key)
        embeds = send[0]
        message = await ctx.send(embeds=[send[0]], components=send[1])

    @search.autocomplete("movie")
    async def autocomplete(self, ctx: AutocompleteContext):
        await self.movie_autocomplete.execute(ctx, self.tmdb_key)


def setup(bot, **kwargs):
    MovieController(bot, **kwargs)

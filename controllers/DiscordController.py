import interactions
from interactions import Extension, component_callback, ComponentContext
from interactions import listen, slash_command, slash_option, OptionType, \
    SlashContext, AutocompleteContext, InteractionContext, ComponentCommand
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from data.MovieListItemData import MovieListItemData

class DiscordController(Extension):
    def __init__(self, bot, key, tmdb_key):
        self.key = key
        self.tmdb_key = tmdb_key
        self.bot = bot

        self.add_movie = AddToMovieListUsecase()

        print("loaded", self.__class__.__name__)

    @listen()
    async def on_ready(self):
        print("Ready")

    @component_callback("add_to_list")
    async def add_to_list(self, ctx: ComponentContext):
        movie_list_data = MovieListItemData(guild=ctx.guild.id, name=ctx.message.embeds[0].title,
                                            tmdb_id=int(ctx.message.embeds[0].footer.text))
        self.add_movie.execute(movie_data=movie_list_data)
        await ctx.send("Added to theoretical list")

    @component_callback("add_to_watched")
    async def add_to_watched(self, ctx: ComponentContext):
        await ctx.send("Theoretically watched movie")


def setup(bot, key, tmdb_key):
    DiscordController(bot, key, tmdb_key)

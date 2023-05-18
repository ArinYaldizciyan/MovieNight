import interactions
from interactions import Extension, component_callback, ComponentContext
from interactions import listen, slash_command, slash_option, OptionType, \
    SlashContext, AutocompleteContext, InteractionContext, ComponentCommand
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData

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
        # bot.fetch_channel(channel_id) will get the correct channel. -> .create_post()
        # bot.guild.create_forum_channel()
        message_embed = ctx.message.embeds[0]
        message_components = ctx.message.components[0]
        message_genres = [genre.strip() for genre in message_embed.fields[2].value.split(',')]
        movie_list_item_data = MovieListItemData(guild=ctx.guild.id, name=message_embed.title,
                                            tmdb_id=int(message_embed.footer.text))
        # Todo: Channel id is hardcoded. Fix that
        movie_list_data = MovieListData(guild=ctx.guild.id, library_channel_id=1108610636725882900)
        await ctx.guild.channels[4].create_post(embeds=[message_embed], components=message_components,
                                                name=message_embed.title,content=f"Added by: <@{ctx.user.id}>",
                                                applied_tags=message_genres)
        self.add_movie.execute(movie_data=movie_list_item_data, movie_list_data=movie_list_data)
        await ctx.send("Added!", ephemeral=True)

    @component_callback("add_to_watched")
    async def add_to_watched(self, ctx: ComponentContext):
        await ctx.send("Theoretically watched movie")


def setup(bot, key, tmdb_key):
    DiscordController(bot, key, tmdb_key)

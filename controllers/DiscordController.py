import interactions
from interactions import Extension, Client, Intents, component_callback, ComponentContext, Embed, Message, Member
from interactions import listen, slash_command, slash_option, OptionType, \
    SlashContext, AutocompleteContext, InteractionContext, ComponentCommand
from appCore.ParamManager import ParamManager
from injector import inject
from interactions import AutocompleteContext, Button, ButtonStyle, PartialEmoji
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from usecases.MovieAutocompleteUsecase import MovieAutocompleteUsecase
from usecases.SearchMoviesUsecase import SearchMovieUsecase
from data.MovieListItemData import MovieListItemData
from data.MovieListData import MovieListData
from .discordUtil.EmbedUtil import create_embed

# pyright: reportOptionalMemberAccess=false, reportOptionalSubscript=false, reportGeneralTypeIssues=false


class DiscordController(Extension):

    def __init__(self, bot: Client, add_to_movie_list: AddToMovieListUsecase,
                 movie_autocomplete: MovieAutocompleteUsecase, search_movie: SearchMovieUsecase):
        self.p = ParamManager()
        self.bot: Client = bot
        self.add_movie = add_to_movie_list
        self.movie_autocomplete = movie_autocomplete
        self.search_movie = search_movie
        print("loaded", self.__class__.__name__)

    @listen()
    async def on_ready(self):
        print("Ready")

    @component_callback("add_to_list")
    async def add_to_list(self, ctx: ComponentContext):
        # bot.fetch_channel(channel_id) will get the correct channel. -> .create_post()
        # bot.guild.create_forum_channel()
        # Todo: Move this to add_to_list usecase. Return a dictionary of kwargs to pass into ctx.send()

        message_embed = ctx.message.embeds[0]
        message_components = ctx.message.components[0]
        message_genres = [genre.strip() for genre in message_embed.fields[2].value.split(',')]
        movie_list_item_data = MovieListItemData(guild=ctx.guild.id, name=message_embed.title,
                                                 tmdb_id=int(message_embed.footer.text))
        # Todo: Channel id is hardcoded. Fix that
        movie_list_data = MovieListData(guild=ctx.guild.id, library_channel_id=1108610636725882900)
        await ctx.guild.channels[4].create_post(embeds=[message_embed], components=message_components,
                                                name=message_embed.title, content=f"Added by: <@{ctx.user.id}>",
                                                applied_tags=message_genres)

        self.add_movie.execute(movie_data=movie_list_item_data, movie_list_data=movie_list_data)
        await ctx.send("Added!", ephemeral=True)

    @component_callback("add_to_watched")
    async def add_to_watched(self, ctx: ComponentContext):
        await ctx.send("Theoretically watched movie", ephemeral=True)

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
        search_data = await self.search_movie.execute(movie_id=movie)
        embed = create_embed(search_data)

        add_emoji = PartialEmoji(name="➕")
        add = interactions.Button(style=interactions.ButtonStyle.GREEN, custom_id='add_to_list', emoji=add_emoji)
        eye_emoji = PartialEmoji(name="👁️")
        watched = interactions.Button(style=interactions.ButtonStyle.BLUE, custom_id='add_to_watched', emoji=eye_emoji)
        action_row = interactions.ActionRow(add, watched)
        message = await ctx.send(embeds=[embed], components=action_row)

    @search.autocomplete("movie")
    async def autocomplete(self, ctx: AutocompleteContext):
        choices = await self.movie_autocomplete.execute(ctx.args[0] if ctx.args else None)
        await ctx.send(
            choices=choices.movies
        )


def setup(bot, add_to_movie_list, movie_autocomplete, search_movie):
    DiscordController(bot=bot, add_to_movie_list=add_to_movie_list, movie_autocomplete=movie_autocomplete,
                      search_movie=search_movie)

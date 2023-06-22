import re
from interactions import Extension, Client, Intents, \
    component_callback, ComponentContext, Embed, Message, Member, StringSelectMenu, StringSelectOption
from interactions import listen, slash_command, slash_option, OptionType, \
    SlashContext, AutocompleteContext, InteractionContext, ComponentCommand, ForumLayoutType, ChannelType
from interactions.client.errors import HTTPException

from appCore.ParamManager import ParamManager
from interactions import AutocompleteContext, Button, ButtonStyle, PartialEmoji
from usecases.AddToMovieListUsecase import AddToMovieListUsecase
from usecases.MovieAutocompleteUsecase import MovieAutocompleteUsecase
from usecases.SearchMoviesUsecase import SearchMovieUsecase
from usecases.GetWatchSourceUsecase import GetWatchSourceUsecase
from usecases.CreateMovieListUsecase import CreateMovieListUsecase
from usecases.GetMovieListUsecase import GetMovieListUsecase
from usecases.GetVoteListUsecase import GetVoteListUsecase
from usecases.AddToVoteListUsecase import AddToVoteListUsecase
from usecases.GetVoteListItemsUsecase import GetVoteListItemsUsecase
from usecases.GetMovieListItemsUsecase import GetMovieListItemsUsecase
from usecases.CreateUserRankingUsecase import CreateUserRankingUsecase
from data.MovieListItemData import MovieListItemData
from data.VoteListItemData import VoteListItemData
from data.VoteListData import VoteListData
from .discordUtil.EmbedUtil import *
from .discordUtil.ActionRowUtil import *
from .discordUtil.ModalUtil import *
from .discordUtil.MoviePaginator import Paginator

from injector import inject


# pyright: reportOptionalMemberAccess=false, reportOptionalSubscript=false, reportGeneralTypeIssues=false


class DiscordController(Extension):

    @inject
    def __init__(self, bot: Client,
                 add_to_movie_list: AddToMovieListUsecase,
                 movie_autocomplete: MovieAutocompleteUsecase,
                 search_movie: SearchMovieUsecase,
                 get_source: GetWatchSourceUsecase,
                 create_movie_list: CreateMovieListUsecase,
                 get_movie_list: GetMovieListUsecase,
                 get_movie_list_items: GetMovieListItemsUsecase,
                 get_vote_list: GetVoteListUsecase,
                 add_to_vote_list: AddToVoteListUsecase,
                 get_vote_list_items: GetVoteListItemsUsecase,
                 create_user_ranking: CreateUserRankingUsecase):
        self.p = ParamManager()
        self.bot: Client = bot
        self.add_movie = add_to_movie_list
        self.movie_autocomplete = movie_autocomplete
        self.search_movie = search_movie
        self.get_source = get_source
        self.create_movie_list = create_movie_list
        self.get_movie_list = get_movie_list
        self.get_vote_list = get_vote_list
        self.add_to_vote_list = add_to_vote_list
        self.get_vote_list_items = get_vote_list_items
        self.get_movie_list_items = get_movie_list_items
        self.create_user_ranking = create_user_ranking
        print("loaded", self.__class__.__name__)

    @listen()
    async def on_ready(self):
        print("Ready")
        for guild in self.bot.guilds:
            if self.get_movie_list.execute(guild=guild.id) is None:
                print(guild.name)
                try:
                    forum_channel = await guild.create_forum_channel(
                        name="movie-library",
                        position=0,
                        layout=ForumLayoutType.LIST)
                except HTTPException:
                    print(guild.name, " is likely not a community server.")
                    continue
                self.create_movie_list.execute(guild=guild.id, library_channel_id=forum_channel.id)

    @component_callback("add_to_list")
    async def add_to_list(self, ctx: ComponentContext):
        message_embed = ctx.message.embeds[0]
        tmdb_id = int(message_embed.footer.text.split('|')[0])
        imdb_id = message_embed.footer.text.split('|')[1]
        # message_components = ctx.message.components[0]
        message_genres = [genre.strip() for genre in message_embed.fields[2].value.split(',')]
        movie_list_item_data = MovieListItemData(id=None, guild=ctx.guild.id, name=message_embed.title,
                                                 tmdb_id=tmdb_id)

        source_list = await self.get_source.execute(imdb_id=imdb_id, tmdb_id=str(tmdb_id))
        source_list_buttons = create_source_buttons(source_list.torrents)

        provider_link = source_list.providers["results"].get("CA").get("link") \
            if source_list.providers["results"].get("CA") else None
        providers = source_list.providers["results"].get("CA").get("flatrate") \
            if source_list.providers["results"].get("CA") else None
        if providers:
            providers_list = ["- " + provider["provider_name"] for provider in providers]
            providers_formatted = "\n".join(providers_list)
        else:
            providers_formatted = "No Providers Found"

        library_channel = self.get_movie_list.execute(guild=ctx.guild.id).library_channel_id
        added_movie = self.add_movie.execute(movie_data=movie_list_item_data)

        link_text = f"[JustWatch CA]({provider_link})\n" if provider_link else ""
        channel = await ctx.guild.fetch_channel(library_channel)
        message_embed.add_field(name="Stream Providers",
                                value=link_text + providers_formatted,
                                inline=False)
        message_embed.set_footer(
            str(added_movie.id) + "|" + message_embed.footer.text if message_embed.footer else message_embed.footer)
        await channel.create_post(
            embeds=[message_embed],
            components=[create_movie_list_buttons(), source_list_buttons],
            name=message_embed.title, content=f"Added by: <@{ctx.user.id}>",
            applied_tags=message_genres)

        await ctx.defer(edit_origin=True)
        # await ctx.send("Added!", ephemeral=True)

    @component_callback("add_to_watched")
    async def add_to_watched(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        # await ctx.send("Theoretically watched movie", ephemeral=True)

    @component_callback("add_to_vote_list")
    async def add_to_vote_list(self, ctx: ComponentContext):
        vote_list_data = VoteListData(id=None, guild=ctx.guild.id, created_by_user=ctx.user.id)
        vote_list = self.get_vote_list.execute(vote_list=vote_list_data)
        vote_list_items = self.get_vote_list_items.execute(vote_list_id=vote_list.id)
        if len(vote_list_items) >= 10:
            await ctx.send("Vote list is full!", ephemeral=True)
            return
        vote_list_item = VoteListItemData(vote_list_item_id=None,
                                          vote_list_id=vote_list.id,
                                          movie_id=int(ctx.message.embeds[0].footer.text.split('|')[0]),
                                          movie_title=ctx.message.embeds[0].title)

        self.add_to_vote_list.execute(vote_list_item_data=vote_list_item)

        await ctx.send(ctx.message.embeds[0].title + " was added to vote list!", ephemeral=True)

    @slash_command(
        name="votelist",
        description="Get your current vote list!"
    )
    async def get_vote_list(self, ctx: InteractionContext):
        vote_list_data = VoteListData(id=None, guild=ctx.guild.id, created_by_user=ctx.user.id)
        vote_list = self.get_vote_list.execute(vote_list=vote_list_data)
        vote_list_items = self.get_vote_list_items.execute(vote_list_id=vote_list.id)
        formatted_list = ">>> " + ("\n".join(["- " + item.movie_title for item in vote_list_items]))
        await ctx.send("> **Vote List:** \n" + formatted_list, ephemeral=True)

    @slash_command(
        name="vote",
        description="Start a vote with your current vote list!"
    )
    async def start_vote(self, ctx: InteractionContext):
        vote_list = self.get_vote_list.execute(
            vote_list=VoteListData(id=None, guild=ctx.guild.id, created_by_user=ctx.user.id)
        )

        await ctx.send(**create_vote_starter_embed(vote_list.id))

    @component_callback(re.compile("^start_ranking\|"))
    async def start_ranking(self, ctx: ComponentContext):
        vote_list_id = int(ctx.custom_id.split('|')[1])
        vote_list_items = self.get_vote_list_items.execute(vote_list_id=vote_list_id)
        movie_list_items = [
            self.get_movie_list_items.execute(
                guild=ctx.guild.id,
                movie_id=item.movie_id) for item in vote_list_items
        ]
        vote_movies = [await self.search_movie.execute(tmdb_id=item[0].tmdb_id) for item in movie_list_items]

        vote_embeds = [create_about_movie_embed(movie) for movie in vote_movies]
        paginator = Paginator.create_from_movie_list \
            (self.bot, *vote_embeds,
             vote_list_id=vote_list_id,
             vote_list_movie_ids=[item.vote_list_item_id for item in vote_list_items],
             ranking_callback=self.ranking_callback,
             finished_callback=self.user_finished_ranking_callback
             )
        await paginator.send(ctx, ephemeral=True)

    async def ranking_callback(self, ctx: ComponentContext, vote_list_id: int, vote_list_item_id: int, ranking: int):
        vote_list_items = self.get_vote_list_items.execute(vote_list_id=vote_list_id)
        self.create_user_ranking.execute(vote_list_item_id=vote_list_item_id, user=ctx.user.id, ranking=ranking)
        print("Ranking: " + str(ranking) + " for movie: " + str(vote_list_item_id) + " by user: " + str(ctx.user.id))
        await ctx.defer(edit_origin=True)

    # Todo: Validate ranking responses. Do not allow duplicates, make sure all movies are ranked
    async def user_finished_ranking_callback(self, ctx: ComponentContext, rankings: List):
        valid_list = len([item for item in rankings if item is not None]) == len(set(rankings))
        if valid_list:
            await ctx.send(f"<@{ctx.user.id}> Finished Ranking!", ephemeral=False)
        else:
            await ctx.send(f"<@{ctx.user.id}>! Make sure you have ranked all movies, and have no duplicate rankings!",
                           ephemeral=True)

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
        search_data = await self.search_movie.execute(tmdb_id=movie)
        embed = create_about_movie_embed(search_data)
        action_row = create_movie_buttons()
        message = await ctx.send(embeds=[embed], components=action_row)

    @search.autocomplete("movie")
    async def autocomplete(self, ctx: AutocompleteContext):
        choices = await self.movie_autocomplete.execute(ctx.args[0] if ctx.args else None)
        await ctx.send(
            choices=choices.movies
        )


def setup(bot, *args, **kwargs):
    DiscordController(bot=bot, *args, **kwargs)

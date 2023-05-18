import interactions
from interactions import Client, Intents, listen, slash_command, slash_option, \
    OptionType, SlashContext, Modal, ShortText, ParagraphText, ModalContext, AutocompleteContext, InteractionContext, ComponentCommand
import parameters
from controllers.BaseController import BaseController
from datetime import datetime
from models.movieList import *


def initialize_db():
    with db:
        db.create_tables([MovieList, MovieListItem, Watched], safe=True)


class Application:
    def __init__(self):
        self.bot: Client = Client(intents=Intents.ALL, debug_scope=833127429853806592,
                                  asyncio_debug=True, sync_interactions=True)

        initialize_db()
        self.db = SqliteDatabase('movienight.db')
        self.p = parameters.Parameter()
        self.key = self.p.get_parameter(name='DISCORD_BOT_KEY', from_environment=True)
        self.tmdb_key = self.p.get_parameter(name='TMDB_API_KEY', from_environment=True)

        # self.baseController = BaseController(bot=self.bot, key=self.key, tmdb_key=self.tmdb_key)
        self.bot.load_extension('controllers.DiscordController', key=self.key, tmdb_key=self.tmdb_key)
        self.bot.load_extension('controllers.MovieController', key=self.key, tmdb_key=self.tmdb_key)
        self.bot.start(self.key)


app = Application()


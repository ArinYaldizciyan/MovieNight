import interactions
from injector import Injector
from appCore.ParamManager import ParamManager
from controllers.config.discordControllerConfig import DiscordControllerConfig
from datetime import datetime
from models.movieList import *


class Application:

    def initialize_db(self):
        with db:
            db.create_tables([MovieList, MovieListItem, Watched], safe=True)
            self.db = SqliteDatabase('movienight.db')

    def __init__(self):
        self.db = None
        self.p = ParamManager()
        self.initialize_db()

        injector = Injector()

        #Define controllers
        controller = injector.get(DiscordControllerConfig)


app = Application()

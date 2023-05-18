from interactions import Client


class BaseController:
    def __init__(self, bot: Client, key, tmdb_key):
        self.bot = bot
        self.key = key
        self.tmdb_key = tmdb_key




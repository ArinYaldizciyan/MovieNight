from appCore.ParamManager import ParamManager
from .ExternalRepository import ExternalRepository
import aiohttp
from models.movieList import MovieList, MovieListItem


class TMDBRepository(ExternalRepository):
    # Todo: Add all dependencies into constructor
    def __init__(self):
        super().__init__()
        self._api_url: str = self._p.get_parameter(name='TMDB_API_URL', from_environment=True)
        self._api_key: str = self._p.get_parameter(name='TMDB_API_KEY', from_environment=True)
        self.image_url: str = self._p.get_parameter(name='TMDB_IMAGE_URL', from_environment=True)
        self.default_image_size: str = self._p.get_parameter(name='TMDB_DEFAULT_IMAGE_SIZE', from_environment=True)

    async def get_image_url(self, movie_image_url: str):
        route_url = self.image_url + self.default_image_size + movie_image_url
        return route_url

    async def search(self, query: str):
        route_url = self._api_url + "/search/movie"
        params = {
            "api_key": self._api_key,
            "query": query,
            "include_adult": "true"
        }
        response = await self._fetch(url=route_url, params=params)
        return response

    async def get_credits(self, tmdb_id: int):
        route_url = self._api_url + "/movie/" + str(tmdb_id) + "/credits"
        params = {
            "api_key": self._api_key
        }
        response = await self._fetch(url=route_url, params=params)
        return response

    async def get_watch_sources(self, tmdb_id: str):
        route_url = self._api_url + "/movie/" + str(tmdb_id) + "/watch/providers"
        params = {
            "api_key": self._api_key
        }
        response = await self._fetch(url=route_url, params=params)
        return response

    async def get_info(self, tmdb_id: int):
        # Todo: Certain movies cause errors. Assuming it has to do with the format of the response,
        #  or maybe the type of movie
        route_url = self._api_url + "movie/" + str(tmdb_id)
        params = {
            "api_key": self._api_key
        }
        response = await self._fetch(url=route_url, params=params)
        return response


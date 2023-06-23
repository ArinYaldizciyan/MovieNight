from .ExternalRepository import ExternalRepository


class OMDBRepository(ExternalRepository):
    # Todo: Add all dependencies into constructor
    def __init__(self):
        super().__init__()
        self._api_url: str = self._p.get_parameter(name='OMDB_API_URL', from_environment=True)
        self._api_key: str = self._p.get_parameter(name='OMDB_API_KEY', from_environment=True)

    async def search(self, imdb_id: str):
        route_url = self._api_url
        params = {
            "apikey": self._api_key,
            "i": imdb_id,
        }
        response = await self._fetch(route_url, params=params)
        return response

    async def get_oscar_info(self, imdb_id: str):
        response = await self.search(imdb_id)
        return response["Awards"]

    async def get_imdb_rating(self, imdb_id: str):
        response = await self.search(imdb_id)
        return response["imdbRating"]



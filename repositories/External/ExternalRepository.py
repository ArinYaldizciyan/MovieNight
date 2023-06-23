import aiohttp
from appCore.ParamManager import ParamManager


class ExternalRepository:
    def __init__(self):
        self._p = ParamManager()

    async def _fetch(self, url, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

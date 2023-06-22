from injector import inject
from typing import List, Optional
from data.WatchSourceData import WatchSourceData
from repositories.External.YTSRepository import YTSRepository
from repositories.External.TMDBRepository import TMDBRepository


class GetWatchSourceUsecase:

    @inject
    def __init__(self,
                 yts_repository: YTSRepository,
                 tmdb_repository: TMDBRepository):
        self.yts_repository = yts_repository
        self.tmdb_repository = tmdb_repository

    async def execute(self, imdb_id: str, tmdb_id: str) -> WatchSourceData:
        torrents = self.yts_repository.get(imdb_id)
        providers = self.tmdb_repository.get_watch_sources(tmdb_id)

        result = WatchSourceData(torrents=torrents, providers=providers)

        return result

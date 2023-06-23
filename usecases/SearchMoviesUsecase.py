from injector import inject
from data.MovieData import MovieData
from repositories.External.TMDBRepository import TMDBRepository
from repositories.External.OMDBRepository import OMDBRepository
from appCore.ParamManager import ParamManager


class SearchMovieUsecase:

    @inject
    def __init__(self, tmdb_repository: TMDBRepository, omdb_repository: OMDBRepository):
        self.tmdb_repository = tmdb_repository
        self.omdb_repository = omdb_repository
        self.param_manager = ParamManager()

    async def execute(self, tmdb_id: int) -> MovieData:
        info = await self.tmdb_repository.get_info(tmdb_id)
        movie_credits = await self.tmdb_repository.get_credits(tmdb_id)
        director = [role for role in movie_credits["crew"] if role["job"] == "Director"][0]["name"]
        watch_sources = await self.tmdb_repository.get_watch_sources(str(tmdb_id))
        thumbnail_url = await self.tmdb_repository.get_image_url(info["poster_path"])
        awards_info = await self.omdb_repository.get_oscar_info(info["imdb_id"])
        imdb_rating = await self.omdb_repository.get_imdb_rating(info["imdb_id"])
        result = MovieData(title=info["original_title"], description=info["overview"],
                           release_date=info["release_date"], genres=info["genres"],
                           poster_path=info["poster_path"], imdb_id=info["imdb_id"],
                           thumbnail_url=thumbnail_url, tmdb_id=tmdb_id, director=director, awards_info=awards_info,
                           imdb_rating=imdb_rating)

        return result

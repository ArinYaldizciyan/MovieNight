from injector import inject
from data.MovieData import MovieData
from repositories.External.TMDBRepository import TMDBRepository


class SearchMovieUsecase:

    @inject
    def __init__(self, tmdb_repository: TMDBRepository):
        self.tmdb_repository = tmdb_repository

    async def execute(self, tmdb_id: int) -> MovieData:
        info = self.tmdb_repository.get_info(tmdb_id)
        credits = self.tmdb_repository.get_credits(tmdb_id)
        director = [role for role in credits["crew"] if role["job"] == "Director"][0]["name"]
        watch_sources = self.tmdb_repository.get_watch_sources(str(tmdb_id))
        thumbnail_url = self.tmdb_repository.get_image_url(info["poster_path"])
        result = MovieData(title=info["original_title"], description=info["overview"],
                           release_date=info["release_date"], genres=info["genres"],
                           poster_path=info["poster_path"], imdb_id=info["imdb_id"],
                           thumbnail_url=thumbnail_url, tmdb_id=tmdb_id, director=director)

        return result

from injector import inject
from data.MovieData import MovieData
from repositories.External.TMDBRepository import TMDBRepository


class SearchMovieUsecase:

    @inject
    def __init__(self, tmdb_repository: TMDBRepository):
        self.tmdb_repository = tmdb_repository

    # Todo: Abstract the embed creation into a view. I.E return an embed view,
    #  this should be based on some embed dataclass
    async def execute(self, movie_id: int) -> MovieData:
        info = self.tmdb_repository.get_info(movie_id)
        thumbnail_url = self.tmdb_repository.get_image_url(info["poster_path"])
        result = MovieData(title=info["original_title"], description=info["overview"],
                           release_date=info["release_date"], genres=info["genres"],
                           poster_path=info["poster_path"], imdb_id=info["imdb_id"],
                           thumbnail_url=thumbnail_url, tmdb_id=movie_id)

        return result

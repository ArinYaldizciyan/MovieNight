from interactions import AutocompleteContext
from injector import inject
from typing import Union
from repositories.External.TMDBRepository import TMDBRepository
from data.AutocompleteMovieData import AutocompleteMovieData


class MovieAutocompleteUsecase:

    @inject
    def __init__(self, tmdb_repository: TMDBRepository):
        self.tmdb_repository = tmdb_repository

    async def execute(self, search: Union[str, None]) -> AutocompleteMovieData:
        movies = []
        if search:
            raw_movies = self.tmdb_repository.search(query=search)["results"]
            for movie in raw_movies:
                movies.append({
                    "name": movie["original_title"],
                    "value": movie["id"]}
                )
        return AutocompleteMovieData(movies=movies)

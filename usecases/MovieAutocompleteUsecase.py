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
                filtered_title = movie["original_title"][:20]
                description_len = 90-len(filtered_title)
                name = filtered_title+": "+movie["overview"][:description_len]+"..."
                movies.append({
                    "name": name,
                    "value": movie["id"]}
                )
        return AutocompleteMovieData(movies=movies)

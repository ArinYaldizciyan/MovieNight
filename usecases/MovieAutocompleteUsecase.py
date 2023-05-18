from interactions import AutocompleteContext
from repositories.TMDB.TMDBRepository import TMDBRepository


class MovieAutocompleteUsecase:

    def __init__(self):
        self.tmdb_repository = TMDBRepository()

    async def execute(self, ctx: AutocompleteContext, tmdb_key: int, arg_index: int = 0):
        typed = ctx.args[arg_index]
        movies = []
        if typed:
            raw_movies = self.tmdb_repository.search(query=typed, key=tmdb_key)["results"]
            for movie in raw_movies:
                movies.append({
                    "name": movie["original_title"],
                    "value": movie["id"]}
                )
        await ctx.send(
            choices=movies
        )
